#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'tina'

import csv
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest,ddt,yaml
from config import setting
from public.models import myunit,screenshot
from public.page_obj.loginPage import login
from public.models.log import Log

# 之前想从excel中直接读取数据，但是修改起来比较麻烦，将改成，先将csv中的数据，生成yaml文件,再从yaml中获取数据的思路
# def load_test_cases_from_csv(csv_file):
#     """从CSV加载测试用例"""
#     test_cases = []
#     with open(csv_file, 'r', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             test_cases.append((
#                 row['detail'],
#                 row['username'],
#                 row['password'],
#                 row['expected'],
#                 row['screenshot']
#             ))
#     return test_cases

try:
    f =open(setting.TEST_DATA_YAML +'/'+'login_data.yaml',encoding='utf-8')
    testData = yaml.load(f,Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log = Log()
    log.error("文件不存在：{0}".format(file))



@ddt.ddt
class Demo_UI(myunit.MyTest):
    """抽屉新热榜登录测试"""
    def user_login_verify(self,username,password):
        """
        用户登录
        :param username: 账号
        :param password: 密码
        :return:
        """
        login(self.driver).user_login(username,password)

    def exit_login_check(self):
        """
        退出登录
        :return:
        """
        login(self.driver).login_exit()

    @ddt.data(*testData)
    def test_login(self,datayaml):
        """
        登录测试
        :param datayaml: 加载login_data登录测试数据
        :return:
        """
        log = Log()
        # 调用登录方法
        self.user_login_verify(datayaml['data']['username'],datayaml['data']['password'])

        po = login(self.driver)
        if datayaml['screenshot'] == 'username_pawd_success':
            log.info("检查点-> {0}".format(po.user_login_success_hint()))
            self.assertEqual(po.user_login_success_hint(), datayaml['check'][0], "成功登录，返回实际结果是->: {0}".format(po.user_login_success_hint()))
            log.info("成功登录，返回实际结果是->: {0}".format(po.user_login_success_hint()))
            screenshot.insert_img(self.driver, datayaml['screenshot'] + '.jpg')
            log.info("-----> 开始执行退出流程操作")
            self.exit_login_check()
            po_exit = login(self.driver)
            log.info("检查点-> 找到{0}元素,表示退出成功！".format(po_exit.exit_login_success_hint()))
            test = format(po_exit.exit_login_success_hint())
            self.assertEqual(po_exit.exit_login_success_hint(), '登 录',"退出登录，返回实际结果是->: {0}".format(po_exit.exit_login_success_hint()))
            log.info("退出登录，返回实际结果是->: {0}".format(po_exit.exit_login_success_hint()))
        else:
            log.info("检查点-> {0}".format(po.phone_pawd_error_hint()))
            self.assertEqual(po.phone_pawd_error_hint(),datayaml['check'][0] , "异常登录，返回实际结果是->: {0}".format(po.phone_pawd_error_hint()))
            log.info("异常登录，返回实际结果是->: {0}".format(po.phone_pawd_error_hint()))
            screenshot.insert_img(self.driver,datayaml['screenshot'] + '.jpg')

if __name__=='__main__':
    unittest.main()