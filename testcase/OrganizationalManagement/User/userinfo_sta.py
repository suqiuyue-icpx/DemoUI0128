#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = '盖华慧'

import csv
import os,sys
from time import sleep

from selenium.webdriver.support.select import Select

from public.page_obj.OrganizationalManagement.userinfo.userinfoPage import userinfo
from public.page_obj.loginPage import login
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest,ddt,yaml
from config import setting
from public.models import myunit,screenshot
from public.models.log import Log

try:
    f =open(setting.TEST_DATA_YAML + '/OrganizationalManagement/userinfo/userinfo_data.yaml',encoding='utf-8')
    testData = yaml.load(f,Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log = Log()
    log.error("文件不存在：{0}".format(file))

@ddt.ddt
class Demo_UI(myunit.MyTest):
    """登录系统"""
    @staticmethod
    def user_login(driver, datayaml):
        """
        用户登录
        :param driver: 浏览器驱动
        :param datayaml: 测试数据
        :return:
        """
        username = datayaml['data']['logcode']
        password = datayaml['data']['password']
        userinfo(driver).user_login(username, password)

    @staticmethod
    def userPage_open(driver):
        """
        用户登录
        :param driver: 浏览器驱动
        :param datayaml: 测试数据
        :return:
        """
        userinfo(driver).page_open()

    @staticmethod
    def add_user_button(driver, datayaml):
        """
        用户登录
        :param driver: 浏览器驱动
        :param datayaml: 测试数据
        :return:
        """
        userinfo(driver).add_user_button()
        userinfo(driver).input_username(datayaml['data']['username'])
        userinfo(driver).input_usercode(datayaml['data']['usercode'])
        userinfo(driver).input_userpassword('A1')
        userinfo(driver).userOrg_button()
        userinfo(driver).userOrg_click_button()
        userinfo(driver).userOrg_confirm_button()
        userinfo(driver).save_button()

    def exit_login(self):
        """
        退出登录
        :return:
        """
        userinfo(self.driver).user_exit()

    def user_query_check(self):
        """
        用户查询
        :return:
        """
        userinfo(self.driver).user_exit()


    @ddt.data(*testData)
    def test_add(self, datayaml):
        """
        新增用户
        :param datayaml: 加载userinfo_data用户信息测试数据
        :return:
        """
        log = Log()
        if datayaml['screenshot'] == 'user_login_success':
            # 初始化页面,调用登录方法
            self.user_login(self.driver, datayaml)
            po = userinfo(self.driver)
            # 校验系统登录成功
            log.info("检查点1-> {}".format(po.user_login_success_hint()))
            self.assertEqual(po.user_login_success_hint(), datayaml['check'][0], "成功登录，返回实际结果是->: {}".format(po.user_login_success_hint()))
            log.info("成功登录，返回实际结果是->: {}".format(po.user_login_success_hint()))
            screenshot.insert_img(self.driver, datayaml['screenshot'] + '.jpg')
            # 打开用户管理页面
            self.userPage_open(self.driver)
            # 校验用户管理页面打开页面成功
            log.info("检查点2-> {}".format(po.userinfo_open_success_hint()))
            self.assertEqual(po.userinfo_open_success_hint(), datayaml['check'][1],"成功打开用户管理页面，返回实际结果是->: {}".format(po.userinfo_open_success_hint()))
            log.info("成功登录，返回实际结果是->: {}".format(po.userinfo_open_success_hint()))
            screenshot.insert_img(self.driver, datayaml['screenshot'] + '.jpg')
        elif datayaml['screenshot'] == 'user_add_success':
            po = userinfo(self.driver)
            # 新增用户
            self.add_user_button(self.driver, datayaml)
            # 校验用户管理页面新增用户成功
            log.info("检查点3-> {}".format(po.userinfo_open_success_hint()))
            self.assertEqual(po.userinfo_open_success_hint(), datayaml['check'][1],
                             "成功打开用户管理页面，返回实际结果是->: {}".format(po.userinfo_open_success_hint()))
            log.info("成功登录，返回实际结果是->: {}".format(po.userinfo_open_success_hint()))
            screenshot.insert_img(self.driver, datayaml['screenshot'] + '.jpg')
        elif datayaml['screenshot'] == 'user_exit_success':
            log.info("-----> 开始执行退出流程操作")
            self.exit_login()
            po_exit = userinfo(self.driver)
            log.info("检查点0-> 找到{0}元素,表示退出成功！".format(po_exit.exit_login_success_hint()))
            self.assertEqual(po_exit.exit_login_success_hint(), datayaml['check'][0],"退出登录，返回实际结果是->: {0}".format(po_exit.exit_login_success_hint()))
            log.info("退出登录，返回实际结果是->: {0}".format(po_exit.exit_login_success_hint()))


if __name__=='__main__':
    unittest.main()