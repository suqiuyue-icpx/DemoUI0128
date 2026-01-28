import csv
import os
from typing import Dict, List, Any


class PageObjectGenerator:
	@staticmethod
	def get_testinfo_from_csv(testinfo_data: List[Dict]) -> Dict[str, str]:
		"""从testinfo数据获取页面信息"""
		page_info = {
			'class_name': 'userinfo',
			'page_title': '用户登录页面',
			'url': '/',
			'yaml_path': '/OrganizationalManagement/userinfo/userinfo.yaml'
		}

		if testinfo_data and len(testinfo_data) > 0:
			info = testinfo_data[0].get('info', '')
			title = testinfo_data[0].get('title', '')
			id_val = testinfo_data[0].get('id', '')

			# 根据title设置class_name
			if title:
				# 提取英文或拼音作为类名
				if '用户' in title:
					page_info['class_name'] = 'userinfo'
				elif '登录' in title:
					page_info['class_name'] = 'login'

			# 根据info设置页面标题
			if info:
				if '登录' in info:
					page_info['page_title'] = '用户登录页面'
				elif '首页' in info:
					page_info['page_title'] = '首页页面'
					page_info['url'] = '/'

			# 根据id设置yaml路径
			if id_val and 'userinfo' in id_val:
				page_info['yaml_path'] = '/OrganizationalManagement/userinfo/userinfo.yaml'
			elif id_val and 'login' in id_val:
				page_info['yaml_path'] = '/OrganizationalManagement/login/login.yaml'

		return page_info

	@staticmethod
	def generate_locators_code(testcase_data: List[Dict], check_data: List[Dict]) -> str:
		"""生成定位器代码部分"""
		code_lines = []

		# 生成testcase定位器
		for i, item in enumerate(testcase_data):
			element_name = item.get('element_name', '')
			find_type = item.get('find_type', '')
			info = item.get('info', '')

			if not element_name or not find_type:
				continue

			# 映射find_type到By常量
			by_mapping = {
				'ID': 'By.ID',
				'XPATH': 'By.XPATH',
				'CLASS_NAME': 'By.CLASS_NAME',
				'CSS_SELECTOR': 'By.CSS_SELECTOR',
				'NAME': 'By.NAME',
				'TAG_NAME': 'By.TAG_NAME',
				'LINK_TEXT': 'By.LINK_TEXT',
				'PARTIAL_LINK_TEXT': 'By.PARTIAL_LINK_TEXT'
			}

			by_type = by_mapping.get(find_type.upper(), 'By.ID')

			# 生成代码行
			comment = f"    # {info}" if info else ""
			var_name = f"{element_name}_loc"
			code_line = f"{comment}\n    {var_name} = ({by_type}, testData.get_elementinfo({i}))"

			code_lines.append(code_line)

		# 添加空行分隔
		if code_lines:
			code_lines.append("")

		# 生成check定位器
		check_index = 0
		for i, item in enumerate(check_data):
			element_info = item.get('element_info', '')
			find_type = item.get('find_type', '')
			info = item.get('info', '')

			if not element_info:
				continue

			# 映射find_type到By常量
			by_mapping = {
				'ID': 'By.ID',
				'XPATH': 'By.XPATH',
				'CLASS_NAME': 'By.CLASS_NAME',
				'CSS_SELECTOR': 'By.CSS_SELECTOR',
				'NAME': 'By.NAME',
				'TAG_NAME': 'By.TAG_NAME',
				'LINK_TEXT': 'By.LINK_TEXT',
				'PARTIAL_LINK_TEXT': 'By.PARTIAL_LINK_TEXT'
			}

			by_type = by_mapping.get(find_type.upper(), 'By.XPATH')

			# 根据info生成变量名
			var_name = ""
			if '登录成功' in info or '检查登录是否成功' in info:
				var_name = "user_login_success_loc"
			elif '退出登录' in info:
				var_name = "exit_login_success_loc"
			elif '异常提示' in info:
				var_name = "phone_pawd_error_hint_loc"
			else:
				var_name = f"check_{check_index}_loc"
				check_index += 1

			code_line = f"    {var_name} = ({by_type}, testData.get_CheckElementinfo({i}))"
			code_lines.append(code_line)

		return "\n".join(code_lines)

	@staticmethod
	def generate_methods_code(testcase_data: List[Dict], check_data: List[Dict]) -> str:
		"""生成方法代码部分"""
		method_lines = []

		# 生成testcase相关方法
		for i, item in enumerate(testcase_data):
			element_name = item.get('element_name', '')
			operate_type = item.get('operate_type', '').lower()
			info = item.get('info', '')

			if not element_name:
				continue

			method_name = element_name

			# 根据操作类型生成不同的方法
			if operate_type == 'click':
				# 特殊处理dig_login方法
				if '登录' in info and '首页' in info:
					method_code = f'''    def dig_login(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''
				else:
					method_code = f'''    def {method_name}(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''
			elif operate_type == 'send_keys':
				# 获取参数名
				param_name = 'text'
				if '用户' in info or 'username' in element_name.lower():
					param_name = 'username'
					method_name = 'login_username'
				elif '密码' in info or 'password' in element_name.lower():
					param_name = 'password'
					method_name = 'login_password'

				method_code = f'''    def {method_name}(self, {param_name}):
        """
        {info}
        :param {param_name}:
        :return:
        """
        self.find_element(*self.{element_name}_loc).clear()
        self.find_element(*self.{element_name}_loc).send_keys({param_name})
'''
			else:
				# 默认方法
				method_code = f'''    def {method_name}(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc)
'''

			method_lines.append(method_code)

		# 生成check相关方法
		for i, item in enumerate(check_data):
			info = item.get('info', '')

			if not info:
				continue

			# 根据info生成方法名
			if '登录成功' in info or '检查登录是否成功' in info:
				method_name = "user_login_success_hint"
				attr = 'get_attribute("title")'
			elif '退出登录' in info:
				method_name = "exit_login_success_hint"
				attr = 'text'
			elif '异常提示' in info:
				method_name = "phone_pawd_error_hint"
				attr = 'text'
			else:
				method_name = f"check_{i}_hint"
				attr = 'text'

			method_code = f'''    # {info}
    def {method_name}(self):
        return self.find_element(*self.{method_name.replace('_hint', '_loc')}).{attr}
'''
			method_lines.append(method_code)

		return "\n".join(method_lines)

	@staticmethod
	def csv_to_page_object_full(csv_file_path: str, output_file_path: str = None) -> str:
		"""
		从CSV文件生成完整的Page Object Python文件
		生成格式完全符合示例要求
		"""
		if not os.path.exists(csv_file_path):
			raise FileNotFoundError(f"CSV文件不存在: {csv_file_path}")

		# 读取CSV文件
		with open(csv_file_path, 'r', encoding='utf-8') as f:
			reader = csv.reader(f)
			rows = list(reader)

		if len(rows) < 3:
			raise ValueError("CSV文件至少需要3行数据")

		# 解析数据
		testinfo_data = []
		testcase_data = []
		check_data = []

		# 解析testinfo（第3行，第0-3列）
		if len(rows) >= 4:
			testinfo_row = rows[2]
			if testinfo_row[0]:
				testinfo_data.append({
					'id': testinfo_row[0],
					'title': testinfo_row[1] if len(testinfo_row) > 1 else '',
					'info': testinfo_row[2] if len(testinfo_row) > 2 else '',
					'filepath': testinfo_row[3] if len(testinfo_row) > 3 else ''
				})

		# 解析testcase区域（从第3行开始，第4-9列）
		for i in range(2, len(rows)):
			row = rows[i]

			# 跳过空行
			if not any(cell and str(cell).strip() for cell in row):
				continue

			# 检查是否有testcase数据（第4列不为空）
			if len(row) > 4 and row[4] and str(row[4]).strip():
				testcase_item = {
					'element_info': str(row[4]).strip() if len(row) > 4 else '',
					'find_type': str(row[5]).strip() if len(row) > 5 else '',
					'operate_type': str(row[6]).strip() if len(row) > 6 else '',
					'info': str(row[7]).strip() if len(row) > 7 else '',
					'index': str(row[8]).strip() if len(row) > 8 else '',
					'element_name': str(row[9]).strip() if len(row) > 9 else ''
				}

				if any(testcase_item.values()):
					testcase_data.append(testcase_item)

		# 解析check区域（从第3行开始，第10-13列）
		check_index = 0
		for i in range(2, len(rows)):
			row = rows[i]

			# 跳过空行
			if not any(cell and str(cell).strip() for cell in row):
				continue

			# 检查是否有check数据（第9列不为空）
			if len(row) > 10 and row[10] and str(row[10]).strip():
				check_item = {
					'element_info': str(row[10]).strip() if len(row) > 10 else '',
					'find_type': str(row[11]).strip() if len(row) > 11 else '',
					'info': str(row[12]).strip() if len(row) > 12 else '',
					'element_name': str(row[13]).strip() if len(row) > 13 else ''
				}

				if any(check_item.values()):
					check_data.append(check_item)

		# 确定输出文件路径
		if output_file_path is None:
			base_name = os.path.splitext(csv_file_path)[0]
			output_file_path = base_name + '_page.py'

		# 获取页面信息
		page_info = PageObjectGenerator.get_testinfo_from_csv(testinfo_data)

		# 生成文件头部
		header = '''#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'tina'

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import setting
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from public.page_obj.base import Page
from time import sleep
from public.models.GetYaml import getyaml

testData = getyaml(setting.TEST_Element_YAML + '{yaml_path}')

'''

		header = header.format(yaml_path=page_info['yaml_path'])

		# 生成类定义
		class_def = f'''class {page_info['class_name']}(Page):
    """
    {page_info['page_title']}
    """
    url = '{page_info['url']}'
    # 定位器，通过元素属性定位元素对象
'''

		# 生成定位器代码
		locators_code = PageObjectGenerator.generate_locators_code(testcase_data, check_data)

		# 生成方法代码
		methods_code = PageObjectGenerator.generate_methods_code(testcase_data, check_data)

		# 组合所有代码
		full_code = header + class_def

		if locators_code:
			full_code += locators_code + "\n"

		if methods_code:
			full_code += methods_code

		# 写入文件
		with open(output_file_path, 'w', encoding='utf-8') as f:
			f.write(full_code)

		print(f"✅ Page Object文件已生成: {output_file_path}")
		print(f"📊 生成统计:")
		print(f"  类名: {page_info['class_name']}")
		print(f"  定位器: {len(testcase_data) + len(check_data)} 个")
		print(f"  方法: {len(testcase_data) + len(check_data)} 个")

		return full_code



def main():
	csv_file = 'userinfo.csv'
	# 生成Page Object文件
	print("\n🔄 正在生成Page Object文件...")
	python_code = PageObjectGenerator.csv_to_page_object_full(csv_file, 'generated_userinfo_page1.py')

	print("\n📝 生成的Python文件内容:")
	print("=" * 80)
	print(python_code)
	print("=" * 80)


if __name__ == "__main__":
	main()