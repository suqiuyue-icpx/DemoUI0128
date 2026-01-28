import csv
from typing import Dict, List, Any


class PageObjectGenerator:
	@staticmethod
	def extract_filepath(csv_file_path: str) -> str:
		"""从CSV提取filepath字段"""
		with open(csv_file_path, 'r', encoding='utf-8') as f:
			reader = csv.reader(f)
			rows = list(reader)

		# 第3行第4列是filepath
		if len(rows) >= 3:
			filepath = rows[2][3] if len(rows[2]) > 3 else ''
			if filepath:
				return filepath.strip()

		return '/OrganizationalManagement/userinfo/userinfo.yaml'

	@staticmethod
	def parse_csv_data(csv_file_path: str) -> Dict[str, Any]:
		"""解析CSV数据"""
		with open(csv_file_path, 'r', encoding='utf-8') as f:
			reader = csv.reader(f)
			rows = list(reader)

		data = {
			'testinfo': {},
			'testcase': [],
			'check': []
		}

		# 提取testinfo
		if len(rows) >= 3:
			testinfo_row = rows[2]
			data['testinfo'] = {
				'id': testinfo_row[0] if len(testinfo_row) > 0 else '',
				'title': testinfo_row[1] if len(testinfo_row) > 1 else '',
				'info': testinfo_row[2] if len(testinfo_row) > 2 else '',
				'filepath': testinfo_row[3] if len(testinfo_row) > 3 else ''
			}

		# 提取testcase数据
		for i in range(2, len(rows)):
			row = rows[i]
			if len(row) > 4 and row[4]:  # element_info不为空
				testcase_item = {
					'element_info': row[4] if len(row) > 4 else '',
					'find_type': row[5] if len(row) > 5 else '',
					'operate_type': row[6] if len(row) > 6 else '',
					'info': row[7] if len(row) > 7 else '',
					'index': row[8] if len(row) > 8 else '',
					'element_name': row[9] if len(row) > 9 else ''
				}
				if any(testcase_item.values()):
					data['testcase'].append(testcase_item)

		# 提取check数据
		for i in range(2, len(rows)):
			row = rows[i]
			if len(row) > 10 and row[10]:  # element_info不为空
				check_item = {
					'element_info': row[10] if len(row) > 10 else '',
					'find_type': row[11] if len(row) > 11 else '',
					'info': row[12] if len(row) > 12 else '',
					'element_name': row[13] if len(row) > 13 else '',
					'operate_type': row[14] if len(row) > 14 else ''
				}
				if any(check_item.values()):
					data['check'].append(check_item)

		return data

	@staticmethod
	def generate_locators(testcase_data: List[Dict]) -> List[str]:
		"""生成定位器代码"""
		locators = []

		for i, item in enumerate(testcase_data):
			element_name = item.get('element_name', f'element_{i}')
			find_type = item.get('find_type', '')
			info = item.get('info', '')

			if not element_name:
				element_name = f'element_{i}'

			# 映射find_type
			by_mapping = {
				'ID': 'By.ID',
				'XPATH': 'By.XPATH',
				'CLASS_NAME': 'By.CLASS_NAME',
				'CSS_SELECTOR': 'By.CSS_SELECTOR',
				'NAME': 'By.NAME'
			}

			by_type = by_mapping.get(find_type.upper(), 'By.ID')
			var_name = f"{element_name}_loc"

			locator_line = f"    # {info}\n    {var_name} = ({by_type}, testData.get_elementinfo({i}))"
			locators.append(locator_line)

		return locators

	@staticmethod
	def generate_check_locators(check_data: List[Dict]) -> List[str]:
		"""生成检查定位器代码"""
		check_locators = []

		for i, item in enumerate(check_data):
			find_type = item.get('find_type', '')
			info = item.get('info', '')
			element_name = item.get('element_name', f'check_{i}')

			# 映射find_type
			by_mapping = {
				'ID': 'By.ID',
				'XPATH': 'By.XPATH',
				'CLASS_NAME': 'By.CLASS_NAME',
				'CSS_SELECTOR': 'By.CSS_SELECTOR',
				'NAME': 'By.NAME'
			}

			by_type = by_mapping.get(find_type.upper(), 'By.XPATH')

			# 根据info生成变量名
			var_name = f"{element_name}_loc"

			check_locator = f"    {var_name} = ({by_type}, testData.get_CheckElementinfo({i}))"
			check_locators.append(check_locator)

		return check_locators

	@staticmethod
	def generate_methods(testcase_data: List[Dict]) -> List[str]:
		"""生成方法代码"""
		methods = []

		for i, item in enumerate(testcase_data):
			element_name = item.get('element_name', f'element_{i}')
			operate_type = item.get('operate_type', '').lower()
			info = item.get('info', '')

			if not element_name:
				element_name = f'element_{i}'

			# 根据操作类型生成方法
				method_code = f'''    def {element_name}(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''
			elif operate_type == 'send_keys':
				# 生成参数名
				param_name = 'text'
				if 'login' not in element_name:
					param_name = element_name
					method_name = 'input_' + element_name
				else:
					method_name = element_name

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
				method_code = f'''    def {element_name}(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''

			methods.append(method_code)

		return methods

	@staticmethod
	def generate_check_methods(check_data: List[Dict]) -> List[str]:
		"""生成检查方法代码 - element_name + '_hint'"""
		check_methods = []

		for i, item in enumerate(check_data):
			element_name = item.get('element_name', f'check_{i}')
			info = item.get('info', '')
			operate_type = item.get('operate_type', '')  # 这里获取值

			# 方法名 = element_name + '_hint'
			method_name = f"{element_name}_hint"

			# 判断应该获取什么属性
			if operate_type == 'title' :
				return_line = f'return self.find_element(*self.{element_name}_loc).get_attribute("title")'
			else:
				return_line = f'return self.find_element(*self.{element_name}_loc).text'

			method_code = f'''    # {info}
    def {method_name}(self):
        {return_line.format(element_name=element_name)}
'''

			check_methods.append(method_code)

		return check_methods

	@staticmethod
	def generate_open_methods(testcase_data: List[Dict]) -> List[str]:
		"""生成方法代码"""
		open_element = []
		for item in testcase_data:
			element_name = item.get('element_name', '')
			if element_name and 'open' in element_name:
				if element_name not in open_element:
					open_element.append(element_name)
		# 如果没有找到open元素，返回空字符串
		if not open_element:
			return ""
		open_methods = [
			'    def page_open(self):',
			'        """',
			'        打开操作页面',
			'        :return:',
			'        """'
		]
		for i, item in enumerate(testcase_data):
			element_name = item.get('element_name', f'element_{i}')
			if 'open'  in element_name:
				# 只选择打开open页面的方法组装
				method_code =  f'        self.{element_name}()'
				open_methods.append(method_code)
			else:
				continue

		# 添加sleep调用
		open_methods.append('        sleep(1)\n')

		return open_methods

	@staticmethod
	def generate_composite_methods() -> str:
		"""生成组合方法"""
		return '''    def user_login(self, username, password):
        """
        登录入口
        :param username: 用户名
        :param password: 密码
        :return:
        """
        self.open()
        self.find_element(*self.login_username_loc).click()
        sleep(3)
        self.login_username(username)
        self.login_password(password)
        sleep(1)
        self.login_button()
        sleep(1)

    def user_exit(self):
        """
        退出系统
        :return:
        """
        above = self.find_element(*self.login_username_check_loc)
        ActionChains(self.driver).move_to_element(above).perform()
        sleep(2)
        self.find_element(*self.login_exit_loc).click()
        sleep(2)
        self.find_element(*self.login_exit_button_loc).click()
        sleep(2)
'''

	@staticmethod
	def csv_to_page_object(csv_file_path: str, output_file_path: str = None) -> str:
		"""从CSV生成Page Object文件"""
		# 提取filepath
		filepath = PageObjectGenerator.extract_filepath(csv_file_path)

		# 解析数据
		data = PageObjectGenerator.parse_csv_data(csv_file_path)

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

'''

		# 生成testData行
		testdata_line = f"testData = getyaml(setting.TEST_Element_YAML + '{filepath}')\n\n"

		# 生成类定义
		class_def = '''class userinfo(Page):
    """
    用户登录页面
    """
    url = '/'
    # 定位器，通过元素属性定位元素对象
'''

		# 生成定位器
		locators = PageObjectGenerator.generate_locators(data['testcase'])
		check_locators = PageObjectGenerator.generate_check_locators(data['check'])

		# 生成方法
		methods = PageObjectGenerator.generate_methods(data['testcase'])
		check_methods = PageObjectGenerator.generate_check_methods(data['check'])
		composite_methods = PageObjectGenerator.generate_composite_methods()
		open_methods = PageObjectGenerator.generate_open_methods(data['testcase'])

		# 组合所有代码
		full_code = header + testdata_line + class_def + "\n".join(locators) + "\n\n"

		if check_locators:
			full_code += "\n".join(check_locators) + "\n\n"

		all_methods = methods + check_methods + open_methods
		if all_methods:
			full_code += "\n".join(all_methods) + "\n"

		full_code += composite_methods

		# 写入文件
		if output_file_path:
			with open(output_file_path, 'w', encoding='utf-8') as f:
				f.write(full_code)
			print(f"✅ Page Object文件已生成: {output_file_path}")

		return full_code


# 使用示例
def main():
	csv_file = 'userinfo.csv'
	# 生成Page Object文件
	print("\n🔄 正在生成Page Object文件...")
	python_code = PageObjectGenerator.csv_to_page_object(csv_file, 'generated_userinfo_page3.py')

	print("\n📝 生成的Python文件内容:")
	print("=" * 80)
	print(python_code)
	print("=" * 80)


if __name__ == "__main__":
	main()