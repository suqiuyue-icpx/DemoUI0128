import csv
import re
from bs4 import BeautifulSoup
import os


def extract_elements_for_testcases(html_content, output_csv='testcases_elements.csv'):
	"""
	从HTML中提取UI元素并按照测试用例格式生成CSV

	Args:
		html_content (str): HTML内容
		output_csv (str): 输出CSV文件名
	"""

	soup = BeautifulSoup(html_content, 'html.parser')

	# 准备CSV数据 - 按照您提供的格式
	csv_rows = []

	# 添加表头
	csv_rows.append([
		'testinfo', '', '', '', 'testcase', '', '', '', '', '', 'check', '', '', ''
	])

	csv_rows.append([
		'id', 'title', 'info', 'filepath', 'element_info', 'find_type', 'operate_type',
		'info', 'index', 'element_name', 'element_info', 'find_type', 'info',
		'element_name', 'operate_type'
	])

	# 从HTML中提取关键UI元素
	test_id = 'test_userinfo001'
	test_title = '用户管理'
	test_info = '用户新增、删除、编辑、查询、登录等功能'
	filepath = '/OrganizationalManagement/userinfo/userinfo.yaml'

	element_index = 0

	# 1. 查找可能的登录相关元素
	login_elements = []

	# 查找输入框
	input_elements = soup.find_all(['input', 'textarea'])
	for input_elem in input_elements:
		elem_type = input_elem.get('type', '').lower()
		placeholder = input_elem.get('placeholder', '')
		elem_id = input_elem.get('id', '')
		elem_name = input_elem.get('name', '')

		# 根据属性判断元素类型
		if elem_id or elem_name:
			element_name = ''
			element_info = ''
			find_type = 'ID' if elem_id else 'NAME'
			operate_type = 'send_keys'
			description = ''

			if 'user' in (elem_id + elem_name + placeholder).lower():
				if 'name' in (elem_id + elem_name + placeholder).lower():
					element_name = 'login_username'
					description = '输入用户名'
				elif 'password' in (elem_id + elem_name + placeholder).lower() or elem_type == 'password':
					element_name = 'login_password'
					description = '输入密码'
				elif 'code' in (elem_id + elem_name).lower():
					element_name = 'usercode'
					description = '输入用户账号'
				elif 'pwd' in (elem_id + elem_name).lower():
					element_name = 'userpassword'
					description = '输入用户密码'

				element_info = elem_id if elem_id else elem_name
				login_elements.append({
					'element_info': element_info,
					'find_type': find_type,
					'operate_type': operate_type,
					'description': description,
					'index': element_index,
					'element_name': element_name
				})
				element_index += 1

	# 2. 查找按钮元素
	button_elements = soup.find_all(['button', 'input', 'a'],
	                                attrs={'type': ['button', 'submit']})
	button_elements.extend(soup.find_all(class_=re.compile(r'btn|button|submit|login|save', re.I)))

	for button in button_elements[:15]:  # 限制数量
		button_text = button.get_text(strip=True)
		button_class = ' '.join(button.get('class', []))
		button_id = button.get('id', '')
		button_type = button.get('type', '')

		element_name = ''
		description = ''

		if any(word in button_text.lower() for word in ['登录', 'login', 'sign in']):
			element_name = 'login_button'
			description = '点击登录按钮'
		elif any(word in button_text.lower() for word in ['保存', 'save', 'submit']):
			element_name = 'save_button'
			description = '点击保存按钮'
		elif any(word in button_text.lower() for word in ['新增', 'add', 'create', '新建']):
			element_name = 'add_user_button'
			description = '点击新增按钮'
		elif any(word in button_text.lower() for word in ['退出', 'logout', 'exit']):
			element_name = 'login_exit'
			description = '退出登录'
		elif any(word in button_text.lower() for word in ['确定', 'confirm', 'ok']):
			element_name = 'confirm_button'
			description = '点击确认按钮'
		elif button_text:
			element_name = f'button_{element_index}'
			description = f'点击{button_text}按钮'

		if element_name:
			# 尝试用不同的定位方式
			if button_id:
				element_info = button_id
				find_type = 'ID'
			elif 'ant-btn' in button_class:
				# 对于Ant Design按钮，使用XPath
				element_info = f"//button[contains(@class, 'ant-btn') and contains(text(), '{button_text}')]"
				find_type = 'XPATH'
			else:
				element_info = f"//button[contains(text(), '{button_text}')]"
				find_type = 'XPATH'

			login_elements.append({
				'element_info': element_info,
				'find_type': find_type,
				'operate_type': 'click',
				'description': description,
				'index': element_index,
				'element_name': element_name
			})
			element_index += 1

	# 3. 查找菜单和链接元素
	menu_elements = soup.find_all(['a', 'div', 'span'],
	                              class_=re.compile(r'menu|nav|tab|link', re.I))

	for menu in menu_elements[:10]:
		menu_text = menu.get_text(strip=True)
		menu_class = ' '.join(menu.get('class', []))
		menu_title = menu.get('title', '')

		if menu_text and len(menu_text) < 20:  # 限制文本长度
			element_name = ''
			description = ''

			if any(word in (menu_text + menu_title).lower() for word in ['用户管理', 'user', '用户']):
				element_name = 'open_UserMan_button'
				description = '点击用户管理菜单'
			elif any(word in (menu_text + menu_title).lower() for word in ['平台管理', 'platform']):
				element_name = 'open_platForm_button'
				description = '点击平台管理菜单'
			elif any(word in (menu_text + menu_title).lower() for word in ['组织管理', 'organization']):
				element_name = 'open_OrgMan_button'
				description = '点击组织管理菜单'
			elif '退出登录' in menu_text:
				element_name = 'login_exit'
				description = '点击退出登录'
			elif '账户' in menu_text or 'account' in menu_text.lower():
				element_name = 'account_menu'
				description = '点击账户菜单'

			if element_name:
				if menu_title:
					element_info = f"//*[@title='{menu_title}']"
				elif 'menu-custom-title' in menu_class:
					element_info = f"//span[@class='menu-custom-title' and @title='{menu_text}']"
				else:
					element_info = f"//*[contains(text(), '{menu_text}')]"

				login_elements.append({
					'element_info': element_info,
					'find_type': 'XPATH',
					'operate_type': 'click',
					'description': description,
					'index': element_index,
					'element_name': element_name
				})
				element_index += 1

	# 4. 查找下拉选择框
	select_elements = soup.find_all(['select', 'div'],
	                                class_=re.compile(r'select|dropdown', re.I))

	for select in select_elements[:5]:
		select_id = select.get('id', '')
		select_class = ' '.join(select.get('class', []))

		if 'select' in select_class.lower() or select.name == 'select':
			element_name = ''
			description = ''

			if 'status' in select_id.lower() or 'state' in select_id.lower():
				element_name = 'userState_button'
				description = '点击用户状态下拉框'

			if element_name:
				if select_id:
					element_info = select_id
					find_type = 'ID'
				else:
					element_info = f"//select[contains(@class, 'select')]"
					find_type = 'XPATH'

				login_elements.append({
					'element_info': element_info,
					'find_type': find_type,
					'operate_type': 'click',
					'description': description,
					'index': element_index,
					'element_name': element_name
				})
				element_index += 1

	# 5. 组织数据到CSV格式
	# 添加测试用例的基本信息行
	for i, elem in enumerate(login_elements):
		row = [''] * 15  # 创建空行

		if i == 0:
			# 第一行包含测试用例基本信息
			row[0] = test_id
			row[1] = test_title
			row[2] = test_info
			row[3] = filepath

		# 填充元素操作信息
		row[4] = elem['element_info']
		row[5] = elem['find_type']
		row[6] = elem['operate_type']
		row[7] = elem['description']
		row[8] = elem['index']
		row[9] = elem['element_name']

		# 添加检查点（这里简单添加一些示例检查点）
		if i == 0:  # 第一个元素后的检查点
			row[10] = "//div[@class='ant-pro-header-account-name']//div[@class='username']"
			row[11] = "XPATH"
			row[12] = "检查登录是否成功"
			row[13] = "user_login_success"
			row[14] = "title"
		elif i == 1:  # 第二个元素后的检查点
			row[10] = "//button[@type='submit' and contains(@class, 'login-button')]"
			row[11] = "XPATH"
			row[12] = "检查退出登录是否成功"
			row[13] = "exit_login_success"
			row[14] = "text"
		elif i == 2:  # 第三个元素后的检查点
			row[10] = "//span[contains(@class, 'ant-pro-multi-tab-title') and contains(text(), '用户管理')]"
			row[11] = "XPATH"
			row[12] = "检查打开用户管理页面"
			row[13] = "userinfo_open_success"
			row[14] = "text"

		csv_rows.append(row)

	# 写入CSV文件
	with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv_rows)

	print(f"测试用例元素已提取并保存到 {output_csv}")
	print(f"共提取了 {len(login_elements)} 个UI元素")

	# 显示提取的元素摘要
	print("\n提取的元素摘要:")
	print("-" * 80)
	print(f"{'索引':<5} {'元素名称':<20} {'定位方式':<10} {'操作类型':<12} {'描述'}")
	print("-" * 80)

	for elem in login_elements[:15]:  # 只显示前15个
		print(
			f"{elem['index']:<5} {elem['element_name']:<20} {elem['find_type']:<10} {elem['operate_type']:<12} {elem['description']}")

	if len(login_elements) > 15:
		print(f"... 还有 {len(login_elements) - 15} 个元素未显示")


def generate_comprehensive_testcases(html_content, output_csv='comprehensive_testcases.csv'):
	"""
	生成更全面的测试用例，包含用户管理的完整流程

	Args:
		html_content (str): HTML内容
		output_csv (str): 输出CSV文件名
	"""

	soup = BeautifulSoup(html_content, 'html.parser')

	# 预定义的测试用例步骤
	test_steps = [
		# 登录流程
		{
			'element_info': 'form_item_username',
			'find_type': 'ID',
			'operate_type': 'send_keys',
			'description': '输入用户名',
			'element_name': 'login_username',
			'checkpoint': {
				'element_info': "//div[@class='ant-pro-header-account-name']//div[@class='username']",
				'find_type': 'XPATH',
				'info': '检查登录是否成功',
				'element_name': 'user_login_success',
				'operate_type': 'title'
			}
		},
		{
			'element_info': 'form_item_password',
			'find_type': 'ID',
			'operate_type': 'send_keys',
			'description': '输入密码',
			'element_name': 'login_password',
			'checkpoint': {
				'element_info': "//button[@type='submit' and contains(@class, 'login-button')]",
				'find_type': 'XPATH',
				'info': '检查退出登录是否成功',
				'element_name': 'exit_login_success',
				'operate_type': 'text'
			}
		},
		{
			'element_info': "//button[@type='submit' and contains(@class, 'login-button')]",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击登录按钮',
			'element_name': 'login_button',
			'checkpoint': {
				'element_info': "//span[contains(@class, 'ant-pro-multi-tab-title') and contains(text(), '用户管理')]",
				'find_type': 'XPATH',
				'info': '检查打开用户管理页面',
				'element_name': 'userinfo_open_success',
				'operate_type': 'text'
			}
		},
		# 导航到用户管理
		{
			'element_info': "//div[@class='ant-pro-header-account-name']//div[@class='username']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击账户菜单',
			'element_name': 'account_menu'
		},
		{
			'element_info': "//span[@title='平台管理' and @class='menu-custom-title']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击平台管理菜单',
			'element_name': 'open_platForm_button'
		},
		{
			'element_info': "//span[@title='组织管理' and @class='menu-custom-title']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击组织管理菜单',
			'element_name': 'open_OrgMan_button'
		},
		{
			'element_info': "//div[text()='用户管理']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击用户管理菜单',
			'element_name': 'open_UserMan_button'
		},
		# 用户新增操作
		{
			'element_info': "//button[@title='新增']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击新增按钮',
			'element_name': 'add_user_button'
		},
		{
			'element_info': "//input[@placeholder='请输入' and @id='use_USER_ALL_NAME']",
			'find_type': 'XPATH',
			'operate_type': 'send_keys',
			'description': '输入用户姓名',
			'element_name': 'username'
		},
		{
			'element_info': "//input[@placeholder='请输入' and @id='use_USER_NAME']",
			'find_type': 'XPATH',
			'operate_type': 'send_keys',
			'description': '输入用户账号',
			'element_name': 'usercode'
		},
		{
			'element_info': 'use_USER_PWD',
			'find_type': 'ID',
			'operate_type': 'send_keys',
			'description': '输入用户密码',
			'element_name': 'userpassword'
		},
		{
			'element_info': "//div[@compentfield='USER_SYS_STATUS']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击用户状态下拉框',
			'element_name': 'userState_button'
		},
		{
			'element_info': "//span[@class='h-select-show-value-item-value' and text()='1']/ancestor::div[@label='启用']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '选择启用状态',
			'element_name': 'userState_button_true'
		},
		{
			'element_info': "//span[@class='h-select-show-value-item-value' and text()='2']/ancestor::div[@label='禁用']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '选择禁用状态',
			'element_name': 'userState_button_false'
		},
		{
			'element_info': "//button[@type='button' and contains(@class, 'ant-btn .h-b-custom-select-button .ant-btn-icon-only')]",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击选择用户组织',
			'element_name': 'userOrg_button'
		},
		{
			'element_info': "//button[@type='button' and contains(@class, 'ant-btn-primary') and text()='保 存']",
			'find_type': 'XPATH',
			'operate_type': 'click',
			'description': '点击保存按钮',
			'element_name': 'save_button'
		}
	]

	# 构建CSV数据
	csv_rows = []

	# 添加表头
	csv_rows.append([
		'testinfo', '', '', '', 'testcase', '', '', '', '', '', 'check', '', '', ''
	])

	csv_rows.append([
		'id', 'title', 'info', 'filepath', 'element_info', 'find_type', 'operate_type',
		'info', 'index', 'element_name', 'element_info', 'find_type', 'info',
		'element_name', 'operate_type'
	])

	# 添加测试步骤
	test_id = 'test_userinfo001'
	test_title = '用户管理'
	test_info = '用户新增、删除、编辑、查询、登录等功能'
	filepath = '/OrganizationalManagement/userinfo/userinfo.yaml'

	for i, step in enumerate(test_steps):
		row = [''] * 15

		if i == 0:
			# 第一行包含测试用例基本信息
			row[0] = test_id
			row[1] = test_title
			row[2] = test_info
			row[3] = filepath

		# 填充步骤信息
		row[4] = step['element_info']
		row[5] = step['find_type']
		row[6] = step['operate_type']
		row[7] = step['description']
		row[8] = i
		row[9] = step['element_name']

		# 添加检查点（如果有）
		if 'checkpoint' in step:
			row[10] = step['checkpoint']['element_info']
			row[11] = step['checkpoint']['find_type']
			row[12] = step['checkpoint']['info']
			row[13] = step['checkpoint']['element_name']
			row[14] = step['checkpoint']['operate_type']

		csv_rows.append(row)

	# 写入CSV文件
	with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv_rows)

	print(f"\n完整的测试用例已生成并保存到 {output_csv}")
	print(f"共包含 {len(test_steps)} 个测试步骤")


# 主程序
def main():
	html_file = 'CMMP微服务平台.html'

	try:
		with open(html_file, 'r', encoding='utf-8') as f:
			html_content = f.read()
	except FileNotFoundError:
		print(f"错误: 找不到文件 {html_file}")
		print("请确保HTML文件在当前目录下")
		return

	print("=" * 60)
	print("HTML UI元素提取工具 - 测试用例生成")
	print("=" * 60)

	print("\n请选择生成方式:")
	print("1. 从HTML自动提取元素生成测试用例")
	print("2. 生成完整的预定义用户管理测试用例")
	print("3. 两种方式都执行")

	choice = input("\n请输入选项 (1-3): ").strip()

	if choice == '1':
		extract_elements_for_testcases(html_content, 'auto_extracted_testcases.csv')
	elif choice == '2':
		generate_comprehensive_testcases(html_content, 'predefined_testcases.csv')
	elif choice == '3':
		extract_elements_for_testcases(html_content, 'auto_extracted_testcases.csv')
		generate_comprehensive_testcases(html_content, 'predefined_testcases.csv')
		print("\n两种测试用例都已生成完成!")
	else:
		print("无效选项，默认执行方式1")
		extract_elements_for_testcases(html_content)


if __name__ == "__main__":
	main()