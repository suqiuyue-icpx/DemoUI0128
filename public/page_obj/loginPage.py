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

testData = getyaml(setting.TEST_Element_YAML + '/' + 'login.yaml')

class login(Page):
    """
    用户登录页面
    """
    url = '/'
    # dig_login_button_loc = (By.ID, testData.get_elementinfo(2))
    def dig_login(self):
        """
        首页登录
        :return:
        """
        self.find_element(*self.login_username_loc).click()
        sleep(5)

    # 定位器，通过元素属性定位元素对象
    # 用户名输入框
    login_username_loc = (By.ID,testData.get_elementinfo(0))
    # 密码输入框
    login_password_loc = (By.ID,testData.get_elementinfo(1))
    # 取消自动登录
    # keeplogin_button_loc = (By.XPATH,testData.get_elementinfo(3))
    # 单击登录
    login_button_loc = (By.XPATH,testData.get_elementinfo(2))
    # 找到用户名
    login_userCheck_loc = (By.XPATH, testData.get_elementinfo(3))
    # 找到退出登录
    login_exit_loc = (By.XPATH, testData.get_elementinfo(4))
    # 选择退出
    login_exit_button_loc = (By.XPATH,testData.get_elementinfo(5))

    def login_username(self,username):
        """
        登录手机号
        :param username:
        :return:
        """
        self.find_element(*self.login_username_loc).clear()
        self.find_element(*self.login_username_loc).send_keys(username)

    def login_password(self,password):
        """
        登录密码
        :param password:
        :return:
        """
        self.find_element(*self.login_password_loc).clear()
        self.find_element(*self.login_password_loc).send_keys(password)

    # def keeplogin(self):
    #     """
    #     取消单选自动登录
    #     :return:
    #     """
    #     self.find_element(*self.keeplogin_button_loc).click()

    def login_button(self):
        """
        登录按钮
        :return:
        """
        self.find_element(*self.login_button_loc).click()

    def login_exit(self):
        """
        退出系统
        :return:
        """
        above = self.find_element(*self.login_userCheck_loc)
        ActionChains(self.driver).move_to_element(above).perform()
        sleep(2)
        self.find_element(*self.login_exit_loc).click()
        sleep(2)
        self.find_element(*self.login_exit_button_loc).click()

    def user_login(self,username,password):
        """
        登录入口
        :param username: 用户名
        :param password: 密码
        :return:
        """
        self.open()
        self.dig_login()
        self.login_username(username)
        self.login_password(password)
        sleep(1)
        #self.keeplogin()
        #sleep(1)
        self.login_button()
        sleep(1)

    user_login_success_loc = (By.XPATH,testData.get_CheckElementinfo(0))
    exit_login_success_loc = (By.XPATH,testData.get_CheckElementinfo(1))


    # 登录成功用户名
    def user_login_success_hint(self):
        above = self.find_element(*self.login_userCheck_loc)
        ActionChains(self.driver).move_to_element(above).perform()
        sleep(2)
        return self.find_element(*self.user_login_success_loc).get_attribute("title")

    # 退出登录
    def exit_login_success_hint(self):
        return self.find_element(*self.exit_login_success_loc).text
