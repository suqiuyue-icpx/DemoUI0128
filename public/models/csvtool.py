# csv_toolkit.py
import csv

import pandas as pd
import chardet
import os
import re

import yaml
from tabulate import tabulate


class CSVToolkit:
	"""CSV文件处理工具包"""

	@staticmethod
	def detect_encoding(file_path):
		"""检测文件编码"""
		with open(file_path, 'rb') as f:
			result = chardet.detect(f.read())
		return result['encoding']

	@staticmethod
	def read_csv_smart(file_path, **kwargs):
		"""智能读取CSV文件"""
		# 自动检测编码
		encoding = kwargs.pop('encoding', None)
		if encoding is None:
			encoding = CSVToolkit.detect_encoding(file_path)

		# 读取文件
		return pd.read_csv(file_path, encoding=encoding, **kwargs)

	@staticmethod
	def preview_csv(file_path, n_rows=10):
		"""预览CSV文件"""
		df = CSVToolkit.read_csv_smart(file_path, nrows=n_rows)

		print(f"文件: {file_path}")
		print(f"编码: {CSVToolkit.detect_encoding(file_path)}")
		print(f"大小: {os.path.getsize(file_path) / 1024:.2f} KB")
		print(f"行数: 未知（预览前{n_rows}行）")
		print(f"列数: {len(df.columns)}")
		print("\n列名:")
		for i, col in enumerate(df.columns, 1):
			print(f"  {i:2d}. {col}")

		print(f"\n前{n_rows}行数据:")
		print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

		return df

	@staticmethod
	def validate_csv(file_path):
		"""验证CSV文件"""
		try:
			df = CSVToolkit.read_csv_smart(file_path)

			issues = []
			# 检查空值
			null_counts = df.isnull().sum()
			if null_counts.any():
				issues.append(f"存在空值: {null_counts[null_counts > 0].to_dict()}")

			# 检查重复行
			duplicates = df.duplicated().sum()
			if duplicates > 0:
				issues.append(f"存在 {duplicates} 行重复数据")

			# 检查数据类型
			dtypes = df.dtypes.astype(str).to_dict()

			return {
				'valid': len(issues) == 0,
				'issues': issues,
				'stats': {
					'rows': len(df),
					'columns': len(df.columns),
					'size_kb': os.path.getsize(file_path) / 1024,
					'dtypes': dtypes
				}
			}

		except Exception as e:
			return {
				'valid': False,
				'issues': [f"读取失败: {str(e)}"],
				'stats': {}
			}

	@staticmethod
	def convert_encoding(file_path, target_encoding='utf-8'):
		"""转换文件编码"""
		# 检测当前编码
		current_encoding = CSVToolkit.detect_encoding(file_path)

		if current_encoding.lower() == target_encoding.lower():
			#打印内容太多了，暂时注释
			#print(f"文件已经是 {target_encoding} 编码")
			return

		# 读取并重新保存
		df = pd.read_csv(file_path, encoding=current_encoding)

		# 备份原文件
		backup_path = file_path + '.bak'
		os.rename(file_path, backup_path)

		# 保存为新编码
		df.to_csv(file_path, encoding=target_encoding, index=False)

		print(f"已将文件从 {current_encoding} 转换为 {target_encoding}")
		print(f"原文件已备份为: {backup_path}")

	@staticmethod
	def _format_yaml_value(value: str) -> str:
		"""格式化YAML值，处理特殊字符"""
		if not value:
			return ""

		# 特殊字符列表
		special_chars = [':', '[', ']', '{', '}', '&', '*', '?', '|', '-', '>', '%', '@', '`', '#']

		# 检查是否需要引号
		needs_quotes = False
		for char in special_chars:
			if char in value:
				needs_quotes = True
				break

		# 检查是否包含空格
		if ' ' in value or '\t' in value:
			needs_quotes = True

		# 如果是空字符串或只包含空格
		if not value.strip():
			return '""'

		# 处理布尔值和数字
		if value.lower() in ['true', 'false']:
			return value.lower()
		elif value.isdigit():
			return value

		if needs_quotes:
			# 转义双引号
			escaped_value = value.replace('"', '\\"')
			return f'"{escaped_value}"'
		else:
			return value

	@staticmethod
	def csv_to_yamldata_code(csv_file_path, yaml_output_path):
		"""
		将特定格式的CSV文件转换为指定的YAML格式
		CSV格式: id,detail,data,check,screenshot
		data字段格式: "key1:value1;key2:value2"

		转换为YAML格式:
		- id: xxx
		  detail: xxx
		  screenshot: xxx
		  data:
		    key1: value1
		    key2: value2
		  check:
		    - xxx
		"""

		# 读取CSV文件
		df = pd.read_csv(csv_file_path)

		# 检查必要的列是否存在
		required_columns = ['id', 'detail', 'data', 'check', 'screenshot']
		for col in required_columns:
			if col not in df.columns:
				raise ValueError(f"CSV文件中缺少必要的列: {col}")

		# 生成YAML字符串
		yaml_lines = []

		for index, row in df.iterrows():
			# 获取基础字段
			test_id = str(row['id']).strip()
			detail = str(row['detail']).strip()
			screenshot = str(row['screenshot']).strip()

			# 解析data字段 (格式: "username:test1;password:A1")
			data_str = str(row['data']).strip()
			data_dict = {}

			if data_str and data_str != 'nan':
				# 按分号分割键值对
				pairs = [pair.strip() for pair in data_str.split(';') if pair.strip()]

				for pair in pairs:
					if ':' in pair:
						# 按第一个冒号分割
						key_value = pair.split(':', 1)
						if len(key_value) == 2:
							key = key_value[0].strip()
							value = key_value[1].strip()

							# 清理value（去除可能的引号）
							value = value.strip('"\'')

							# 添加到字典
							data_dict[key] = value

			# 解析check字段
			check_str = str(row['check']).strip()
			check_list = []

			if check_str and check_str != 'nan':
				# 按逗号分割多个检查项
				check_items = [item.strip() for item in check_str.split(';') if item.strip()]
				check_list = check_items

			# 生成YAML条目
			yaml_lines.append(f"- id : {test_id}")
			yaml_lines.append(f"  detail : {detail}")

			# 根据你的需求，使用固定的screenshot值或从CSV读取
			# 这里使用固定的值 "username_pawd_success"
			# yaml_lines.append(f"  screenshot : username_pawd_success")
			# 如果要用CSV中的值，用下面这行：
			yaml_lines.append(f"  screenshot : {screenshot}")

			# 添加data部分
			yaml_lines.append(f"  data :")

			if data_dict:
				for key, value in data_dict.items():
					yaml_lines.append(f"    {key} : {value}")
			else:
				yaml_lines.append(f"    # 无data参数")

			# 添加check部分
			yaml_lines.append(f"  check :")

			if check_list:
				for check_item in check_list:
					yaml_lines.append(f"    - {check_item}")
			else:
				yaml_lines.append(f"    - ''")

			# # 在每个测试用例之间添加空行（除了最后一个）
			# if index < len(df) - 1:
			# 	yaml_lines.append("")

		# 组合所有行
		yaml_content = "\n".join(yaml_lines)

		# 确定输出文件路径
		if yaml_output_path is None:
			# 默认使用同目录下的同名yaml文件
			base_name = os.path.splitext(csv_file_path)[0]
			yaml_output_path = base_name + '.yaml'

		# 写入文件
		with open(yaml_output_path, 'w', encoding='utf-8') as f:
			f.write(yaml_content)

		# 打印日志太多了，暂时注释
		# print(f"✅ YAML文件已生成: {yaml_output_path}")
		# print(f"📊 转换了 {len(df)} 条测试用例")

		# 预览结果
		# print("\n📝 生成的YAML内容预览:")
		# print("=" * 50)
		# print(yaml_content)

		return yaml_content

	@staticmethod
	def csv_to_yamlelement_code(csv_file_path , yaml_output_path):
		"""
		    解析复杂格式的CSV文件并转换为指定的YAML格式

		    CSV结构说明:
		    - 第一行: 列标题（包含testinfo, testcase, check等）
		    - 第二行: 子标题
		    - 后续行: 数据

		    转换为YAML格式:
		    testinfo:
		      - id: xxx
		        title: xxx
		        info: xxx
		    testcase:
		      - element_info: xxx
		        find_type: xxx
		        operate_type: xxx
		        info: xxx
		    check:
		      - element_info: xxx
		        find_type: xxx
		        info: xxx
		    """

		if not os.path.exists(csv_file_path):
			raise FileNotFoundError(f"CSV文件不存在: {csv_file_path}")

		# 读取CSV文件
		with open(csv_file_path, 'r', encoding='utf-8') as f:
			reader = csv.reader(f)
			rows = list(reader)

		if len(rows) < 2:
			raise ValueError("CSV文件至少需要2行数据（标题行和子标题行）")

		# 解析列结构
		header_row1 = rows[0]  # 第一行标题
		header_row2 = rows[1]  # 第二行子标题

		# 找出各个区域的列索引
		yaml_data = {
			'testinfo': [],
			'testcase': [],
			'check': []
		}

		# 解析testinfo区域（第0-3列）
		# testinfo_start = 0
		# testinfo_columns = 4   根据你的数据，testinfo有4列，只取前3列信息即可

		for i in range(2, len(rows)):
			row = rows[i]

			# 跳过空行
			if not any(cell and str(cell).strip() for cell in row):
				continue

			# 提取testinfo数据
			if row[0]:  # id不为空
				testinfo_item = {
					'id': row[0].strip(),
					'title': row[1].strip() if len(row) > 1 and row[1] else '',
					'info': row[2].strip() if len(row) > 2 and row[2] else ''
				}

				# 只添加非空的数据
				if any(testinfo_item.values()):
					yaml_data['testinfo'].append(testinfo_item)

		# 解析testcase区域（第4-9列）
		# 根据你的数据，testcase在row[4]到row[9]
		# testcase_fields = ['element_info', 'find_type', 'operate_type', 'info', 'index', 'element_name']

		for i in range(2, len(rows)):
			row = rows[i]

			# 跳过空行
			if not any(cell and str(cell).strip() for cell in row):
				continue

			# 检查是否有testcase数据（第3列不为空）
			if len(row) > 4 and row[4]:
				testcase_item = {
					'element_info': row[4].strip() if len(row) > 4 and row[4] else '',
					'find_type': row[5].strip() if len(row) > 5 and row[5] else '',
					'operate_type': row[6].strip() if len(row) > 6 and row[6] else '',
					'info': row[7].strip() if len(row) > 7 and row[7] else '',
					'index': row[8].strip() if len(row) > 8 and row[8] else '',
					'element_name': row[9].strip() if len(row) > 9 and row[9] else ''
				}

				# 只添加非空的数据
				if any(testcase_item.values()):
					yaml_data['testcase'].append(testcase_item)

		# 解析check区域（第10-13列）
		# check_fields = ['element_info', 'find_type', 'info', 'element_name']

		for i in range(2, len(rows)):
			row = rows[i]

			# 跳过空行
			if not any(cell and str(cell).strip() for cell in row):
				continue

			# 检查是否有check数据（第8列不为空）
			if len(row) > 8 and row[8]:
				check_item = {
					'element_info': row[10].strip() if len(row) > 10 and row[10] else '',
					'find_type': row[11].strip() if len(row) > 11 and row[11] else '',
					'info': row[12].strip() if len(row) > 12 and row[12] else '',
					'element_name': row[13].strip() if len(row) > 13 and row[13] else ''
				}

				# 只添加非空的数据
				if any(check_item.values()):
					yaml_data['check'].append(check_item)

		# 如果没有指定输出路径，使用默认路径
		if yaml_output_path is None:
			base_name = os.path.splitext(csv_file_path)[0]
			yaml_output_path = base_name + '.yaml'

		# 写入YAML文件
		with open(yaml_output_path, 'w', encoding='utf-8') as f:
			# 写入testinfo部分
			if yaml_data.get('testinfo'):
				f.write("testinfo:\n")
				for item in yaml_data['testinfo']:
					f.write("    - id: " + CSVToolkit._format_yaml_value(item.get('id', '')) + "\n")
					f.write("      title: " + CSVToolkit._format_yaml_value(item.get('title', '')) + "\n")
					f.write("      info: " + CSVToolkit._format_yaml_value(item.get('info', '')) + "\n")
				f.write("\n")  # 空行分隔

			# 写入testcase部分
			if yaml_data.get('testcase'):
				f.write("testcase:\n")
				for i, item in enumerate(yaml_data['testcase']):
					if i > 0:
						f.write("\n")  # 在每个testcase项之间添加空行

					f.write("    - element_info: " + CSVToolkit._format_yaml_value(
						item.get('element_info', '')) + "\n")
					f.write(
						"      find_type: " + CSVToolkit._format_yaml_value(item.get('find_type', '')) + "\n")
					f.write("      operate_type: " + CSVToolkit._format_yaml_value(
						item.get('operate_type', '')) + "\n")
					f.write("      info: " + CSVToolkit._format_yaml_value(item.get('info', '')) + "\n")
					f.write("      index: " + CSVToolkit._format_yaml_value(item.get('index', '')) + "\n")
				f.write("\n")  # 空行分隔

			# 写入check部分
			if yaml_data.get('check'):
				f.write("check:\n")
				for i, item in enumerate(yaml_data['check']):
					if i > 0:
						f.write("\n")  # 在每个check项之间添加空行

					f.write("    - element_info: " + CSVToolkit._format_yaml_value(
						item.get('element_info', '')) + "\n")
					f.write(
						"      find_type: " + CSVToolkit._format_yaml_value(item.get('find_type', '')) + "\n")
					f.write("      info: " + CSVToolkit._format_yaml_value(item.get('info', '')) + "\n")

		# print(f"✅ YAML文件已生成: {yaml_output_path}")

		# 显示统计信息，打印日志过多，暂时注释
		# print(f"📊 转换统计:")
		# print(f"  testinfo: {len(yaml_data['testinfo'])} 条")
		# print(f"  testcase: {len(yaml_data['testcase'])} 条")
		# print(f"  check: {len(yaml_data['check'])} 条")

		# """
		# 增强版的CSV到YAML转换，更智能地解析数据
		# """
		# # 智能识别数据结构
		# sections = {}
		# current_section = None
		# section_headers = {}
		#
		# # 分析第一行，找出所有section
		# for col_idx, header in enumerate(rows[0]):
		# 	if header and header not in ['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6',
		# 	                             'Unnamed: 8', 'Unnamed: 9']:
		# 		current_section = header
		# 		sections[current_section] = []
		# 		section_headers[current_section] = []
		#
		# # 收集第二行的字段名
		# for col_idx, sub_header in enumerate(rows[1]):
		# 	# 找到这个列属于哪个section
		# 	for section in sections.keys():
		# 		# 简单分配：根据列的位置分配
		# 		if section == 'testinfo' and col_idx < 3:
		# 			if sub_header:
		# 				section_headers[section].append(sub_header)
		# 		elif section == 'testcase' and 3 <= col_idx < 7:
		# 			if sub_header:
		# 				section_headers[section].append(sub_header)
		# 		elif section == 'check' and col_idx >= 7:
		# 			if sub_header:
		# 				section_headers[section].append(sub_header)
		#
		# # 处理数据行
		# for row_idx in range(2, len(rows)):
		# 	row = rows[row_idx]
		#
		# 	# 跳过完全空的行
		# 	if not any(cell.strip() if cell else False for cell in row):
		# 		continue
		#
		# 	# 处理testinfo
		# 	if row[0]:  # id不为空
		# 		testinfo_item = {}
		# 		for i, field in enumerate(section_headers['testinfo']):
		# 			if i < len(row) and row[i]:
		# 				testinfo_item[field] = row[i].strip()
		# 		if testinfo_item:
		# 			sections['testinfo'].append(testinfo_item)
		#
		# 	# 处理testcase
		# 	testcase_item = {}
		# 	for i in range(3, 7):  # testcase在3-6列
		# 		if i < len(row) and row[i]:
		# 			field_idx = i - 3
		# 			if field_idx < len(section_headers['testcase']):
		# 				testcase_item[section_headers['testcase'][field_idx]] = row[i].strip()
		#
		# 	if testcase_item:
		# 		sections['testcase'].append(testcase_item)
		#
		# 	# 处理check
		# 	check_item = {}
		# 	for i in range(7, min(10, len(row))):  # check在7-9列
		# 		if i < len(row) and row[i]:
		# 			field_idx = i - 7
		# 			if field_idx < len(section_headers['check']):
		# 				check_item[section_headers['check'][field_idx]] = row[i].strip()
		#
		# 	if check_item:
		# 		sections['check'].append(check_item)
		#
		# # 如果指定了输出路径，写入文件
		# if yaml_output_path:
		# 	with open(yaml_output_path, 'w', encoding='utf-8') as f:
		# 		yaml.dump(sections, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
		#
		# 	print(f"✅ YAML文件已生成: {yaml_output_path}")

		return yaml_data



# 使用示例
if __name__ == "__main__":
	# 预览文件
	CSVToolkit.preview_csv('G:/DemoUI-master/testdata/login_data.csv')

	# 验证文件
	result = CSVToolkit.validate_csv('G:/DemoUI-master/testdata/login_data.csv')
	print(f"验证结果: {'通过' if result['valid'] else '失败'}")
	if result['issues']:
		print("问题:", result['issues'])

	# 转换编码（如果需要）
	CSVToolkit.convert_encoding('G:/DemoUI-master/testdata/login_data.csv', 'utf-8-sig')
	yaml_code = CSVToolkit.csv_to_yamldata_code('G:/DemoUI-master/testdata/login_data.csv', 'G:/DemoUI-master/testdata/login_data.yaml')
	print("生成的YAML代码已保存")

	# 转换编码（如果需要）
	CSVToolkit.convert_encoding('G:/DemoUI-master/testyaml/login.csv', 'utf-8-sig')
	yaml_code = CSVToolkit.csv_to_yamlelement_code('G:/DemoUI-master/testyaml/login.csv',
	                                        'G:/DemoUI-master/testyaml/login.yaml')
	print("生成的YAML代码已保存")