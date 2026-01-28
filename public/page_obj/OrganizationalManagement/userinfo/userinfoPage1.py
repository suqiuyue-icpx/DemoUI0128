#!/usr/bin/env python
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

testData = getyaml(setting.TEST_Element_YAML + '/OrganizationalManagement/userinfo/userinfo.yaml')

class userinfo(Page):
    """
    用户登录页面
    """
    url = '/'
    # 定位器，通过元素属性定位元素对象
    # 输入用户信息
    login_username_loc = (By.ID, testData.get_elementinfo(0))
    # 输入密码
    login_password_loc = (By.ID, testData.get_elementinfo(1))
    # 点击登录按钮
    login_button_loc = (By.XPATH, testData.get_elementinfo(2))
    # 鼠标悬停账户菜单
    login_username_check_loc = (By.XPATH, testData.get_elementinfo(3))
    # 鼠标悬停退出登录
    login_exit_loc = (By.XPATH, testData.get_elementinfo(4))
    # 选择确认退出
    login_exit_button_loc = (By.XPATH, testData.get_elementinfo(5))
    # 鼠标悬停平台管理菜单
    open_platForm_button_loc = (By.XPATH, testData.get_elementinfo(6))
    # 鼠标悬停组织管理菜单
    open_OrgMan_button_loc = (By.XPATH, testData.get_elementinfo(7))
    # 鼠标悬停用户管理菜单
    open_UserMan_button_loc = (By.XPATH, testData.get_elementinfo(8))
    # 点击新增按钮
    add_user_button_loc = (By.XPATH, testData.get_elementinfo(9))
    # 输入用户姓名
    username_loc = (By.XPATH, testData.get_elementinfo(10))
    # 输入用户账号
    usercode_loc = (By.XPATH, testData.get_elementinfo(11))
    # 输入用户密码
    userpassword_loc = (By.ID, testData.get_elementinfo(12))
    # 下拉选择用户状态按钮
    userState_button_loc = (By.XPATH, testData.get_elementinfo(13))
    # 选择启用
    userState_button_true_loc = (By.XPATH, testData.get_elementinfo(14))
    # 选择禁用
    userState_button_false_loc = (By.XPATH, testData.get_elementinfo(15))
    # 打开用户组织选择页面
    userOrg_button_loc = (By.XPATH, testData.get_elementinfo(16))
    # 勾选用户组织
    userOrg_click_button_loc = (By.XPATH, testData.get_elementinfo(17))
    # 选择用户组织后，点击确定按钮
    userOrg_confirm_button_loc = (By.XPATH, testData.get_elementinfo(18))
    # 点击保存按钮
    save_button_loc = (By.XPATH, testData.get_elementinfo(19))

    user_login_success_loc = (By.XPATH, testData.get_CheckElementinfo(0))
    exit_login_success_loc = (By.XPATH, testData.get_CheckElementinfo(1))
    userinfo_open_success_loc = (By.XPATH, testData.get_CheckElementinfo(2))

    def login_username(self, text):
        """
        输入用户信息
        :param text:
        :return:
        """
        self.find_element(*self.login_username_loc).clear()
        self.find_element(*self.login_username_loc).send_keys(text)

    def login_password(self, text):
        """
        输入密码
        :param text:
        :return:
        """
        self.find_element(*self.login_password_loc).clear()
        self.find_element(*self.login_password_loc).send_keys(text)

    def login_button(self):
        """
        点击登录按钮
        :return:
        """
        self.find_element(*self.login_button_loc).click()
        sleep(1)

    def login_username_check(self):
        """
        鼠标悬停账户菜单
        :return:
        """
        self.find_element(*self.login_username_check_loc).click()
        sleep(1)

    def login_exit(self):
        """
        鼠标悬停退出登录
        :return:
        """
        self.find_element(*self.login_exit_loc).click()
        sleep(1)

    def login_exit_button(self):
        """
        选择确认退出
        :return:
        """
        self.find_element(*self.login_exit_button_loc).click()
        sleep(1)

    def open_platForm_button(self):
        """
        鼠标悬停平台管理菜单
        :return:
        """
        self.find_element(*self.open_platForm_button_loc).click()
        sleep(1)

    def open_OrgMan_button(self):
        """
        鼠标悬停组织管理菜单
        :return:
        """
        self.find_element(*self.open_OrgMan_button_loc).click()
        sleep(1)

    def open_UserMan_button(self):
        """
        鼠标悬停用户管理菜单
        :return:
        """
        self.find_element(*self.open_UserMan_button_loc).click()
        sleep(1)

    def add_user_button(self):
        """
        点击新增按钮
        :return:
        """
        self.find_element(*self.add_user_button_loc).click()
        sleep(1)

    def input_username(self, username):
        """
        输入用户姓名
        :param username:
        :return:
        """
        self.find_element(*self.username_loc).clear()
        self.find_element(*self.username_loc).send_keys(username)

    def input_usercode(self, usercode):
        """
        输入用户账号
        :param usercode:
        :return:
        """
        self.find_element(*self.usercode_loc).clear()
        self.find_element(*self.usercode_loc).send_keys(usercode)

    def input_userpassword(self, userpassword):
        """
        输入用户密码
        :param userpassword:
        :return:
        """
        self.find_element(*self.userpassword_loc).clear()
        self.find_element(*self.userpassword_loc).send_keys(userpassword)

    def userState_button(self):
        """
        下拉选择用户状态按钮
        :return:
        """
        self.find_element(*self.userState_button_loc).click()
        sleep(1)

    def userState_button_true(self):
        """
        选择启用
        :return:
        """
        self.find_element(*self.userState_button_true_loc).click()
        sleep(1)

    def userState_button_false(self):
        """
        选择禁用
        :return:
        """
        self.find_element(*self.userState_button_false_loc).click()
        sleep(1)

    def userOrg_button(self):
        """
        打开用户组织选择页面
        :return:
        """
        self.find_element(*self.userOrg_button_loc).click()
        sleep(1)

    def userOrg_click_button(self):
        """
        勾选用户组织
        :return:
        """
        self.find_element(*self.userOrg_click_button_loc).click()
        sleep(1)

    def userOrg_confirm_button(self):
        """
        选择用户组织后，点击确定按钮
        :return:
        """
        self.find_element(*self.userOrg_confirm_button_loc).click()
        sleep(1)

    def save_button(self):
        """
        点击保存按钮
        :return:
        """
        self.find_element(*self.save_button_loc).click()
        sleep(1)

    # 检查登录是否成功
    def user_login_success_hint(self):
        return self.find_element(*self.user_login_success_loc).get_attribute("title")

    # 检查退出登录是否成功
    def exit_login_success_hint(self):
        return self.find_element(*self.exit_login_success_loc).text

    # 检查打开用户管理页面
    def userinfo_open_success_hint(self):
        return self.find_element(*self.userinfo_open_success_loc).text

    def page_open(self):
        """
        打开操作页面
        :return:
        """
        self.open_platForm_button()
        self.open_OrgMan_button()
        self.open_UserMan_button()
        sleep(1)

    def user_login(self, username, password):
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
