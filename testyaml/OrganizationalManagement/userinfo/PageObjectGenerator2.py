import csv
import os
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

		return '/OrganizationalManagement/userinfo/userinfo.yaml'  # 默认值

	@staticmethod
	def get_page_info(testinfo_row: List) -> Dict[str, str]:
		"""获取页面信息"""
		page_info = {
			'class_name': 'userinfo',
			'page_title': '用户登录页面',
			'url': '/'
		}

		if testinfo_row:
			title = testinfo_row[1] if len(testinfo_row) > 1 else ''
			info = testinfo_row[2] if len(testinfo_row) > 2 else ''

			# 根据title设置类名
			if title and '用户管理' in title:
				page_info['class_name'] = 'userinfo'
				page_info['page_title'] = '用户登录页面'
			elif title and '登录' in title:
				page_info['class_name'] = 'login'
				page_info['page_title'] = '登录页面'

			# 根据info设置URL
			if info and '首页' in info:
				page_info['url'] = '/'

		return page_info

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
			# 第4列开始是testcase（索引4-9）
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
			# 第10列开始是check（索引10-13）
			if len(row) > 10 and row[10]:  # element_info不为空
				check_item = {
					'element_info': row[10] if len(row) > 10 else '',
					'find_type': row[11] if len(row) > 11 else '',
					'info': row[12] if len(row) > 12 else '',
					'element_name': row[13] if len(row) > 13 else ''
				}
				if any(check_item.values()):
					data['check'].append(check_item)

		return data

	@staticmethod
	def generate_locator_code(testcase_item: Dict, index: int) -> str:
		"""生成定位器代码行"""
		element_name = testcase_item.get('element_name', f'element_{index}')
		find_type = testcase_item.get('find_type', '')
		info = testcase_item.get('info', '')

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

		return f"    # {info}\n    {var_name} = ({by_type}, testData.get_elementinfo({index}))"

	@staticmethod
	def generate_check_locator_code(check_item: Dict, index: int) -> str:
		"""生成检查定位器代码行"""
		element_name = check_item.get('element_name', f'check_element_{index}')
		find_type = check_item.get('find_type', '')
		info = check_item.get('info', '')

		# 映射find_type
		by_mapping = {
			'ID': 'By.ID',
			'XPATH': 'By.XPATH',
			'CLASS_NAME': 'By.CLASS_NAME'
		}

		by_type = by_mapping.get(find_type.upper(), 'By.XPATH')

		# 根据info生成变量名
		if '登录成功' in info:
			var_name = "user_login_success_loc"
		elif '退出登录' in info:
			var_name = "exit_login_success_loc"
		else:
			var_name = f"{element_name}_loc"

		return f"    {var_name} = ({by_type}, testData.get_CheckElementinfo({index}))"

	@staticmethod
	def generate_method_code(testcase_item: Dict, index: int) -> str:
		"""生成方法代码"""
		element_name = testcase_item.get('element_name', f'element_{index}')
		operate_type = testcase_item.get('operate_type', '').lower()
		info = testcase_item.get('info', '')

		if operate_type == 'click':
			# 特殊处理dig_login
			if '首页登录' in info or index == 0:
				return f'''    def dig_login(self):
        """
        首页登录
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''
			else:
				return f'''    def {element_name}(self):
        """
        {info}
        :return:
        """
        self.find_element(*self.{element_name}_loc).click()
        sleep(1)
'''

		elif operate_type == 'send_keys':
			param_name = 'username' if '用户' in info else 'password'
			method_name = 'login_username' if param_name == 'username' else 'login_password'

			return f'''    def {method_name}(self, {param_name}):
        """
        {info}
        :param {param_name}:
        :return:
        """
        self.find_element(*self.{element_name}_loc).clear()
        self.find_element(*self.{element_name}_loc).send_keys({param_name})
'''

		return ''

	@staticmethod
	def generate_check_method(check_item: Dict, index: int) -> str:
		"""生成检查方法"""
		info = check_item.get('info', '')

		if '登录成功' in info:
			return '''    # 登录成功用户名
    def user_login_success_hint(self):
        return self.find_element(*self.user_login_success_loc).get_attribute("title")
'''
		elif '退出登录' in info:
			return '''    # 退出登录
    def exit_login_success_hint(self):
        return self.find_element(*self.exit_login_success_loc).text
'''

		return ''

	@staticmethod
	def generate_composite_methods() -> str:
		"""生成组合方法"""
		return '''    def user_login(self,username,password):
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
'''

	@staticmethod
	def csv_to_page_object(csv_file_path: str, output_file_path: str = None) -> str:
		"""从CSV生成Page Object Python文件"""
		# 提取filepath
		filepath = PageObjectGenerator.extract_filepath(csv_file_path)

		# 解析CSV数据
		data = PageObjectGenerator.parse_csv_data(csv_file_path)

		# 获取页面信息
		page_info = PageObjectGenerator.get_page_info(
			list(data['testinfo'].values()) if data['testinfo'] else []
		)

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

		# 生成testData初始化
		testdata_line = f"testData = getyaml(setting.TEST_Element_YAML + '{filepath}')\n\n"

		# 生成类定义
		class_def = f'''class {page_info['class_name']}(Page):
    """
    {page_info['page_title']}
    """
    url = '{page_info['url']}'
    # 定位器，通过元素属性定位元素对象
'''

		# 生成定位器代码
		locators = []
		for i, testcase in enumerate(data['testcase']):
			locator_code = PageObjectGenerator.generate_locator_code(testcase, i)
			locators.append(locator_code)

		# 生成check定位器代码
		check_locators = []
		for i, check in enumerate(data['check']):
			check_locator = PageObjectGenerator.generate_check_locator_code(check, i)
			check_locators.append(check_locator)

		# 添加空行
		if locators:
			locators.append("")

		# 生成方法代码
		methods = []
		for i, testcase in enumerate(data['testcase']):
			method_code = PageObjectGenerator.generate_method_code(testcase, i)
			if method_code:
				methods.append(method_code)

		# 生成检查方法代码
		for i, check in enumerate(data['check']):
			check_method = PageObjectGenerator.generate_check_method(check, i)
			if check_method:
				methods.append(check_method)

		# 添加组合方法
		composite_methods = PageObjectGenerator.generate_composite_methods()
		methods.append(composite_methods)

		# 组合所有代码
		full_code = header + testdata_line + class_def

		if locators:
			full_code += "\n".join(locators) + "\n"

		if check_locators:
			full_code += "\n".join(check_locators) + "\n\n"

		if methods:
			full_code += "\n".join(methods)

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
	python_code = PageObjectGenerator.csv_to_page_object(csv_file, 'generated_userinfo_page2.py')

	print("\n📝 生成的Python文件内容:")
	print("=" * 80)
	print(python_code)
	print("=" * 80)

if __name__ == "__main__":
	main()