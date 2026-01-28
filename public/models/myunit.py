#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'tina'

from .driver import browser
import unittest


class MyTest(unittest.TestCase):
    """
    自定义MyTest类 - 修复None问题
    """

    @classmethod
    def setUpClass(cls):
        # 初始化浏览器
        cls.driver = browser()

        # 检查是否成功初始化
        if cls.driver is None:
            # 如果browser()返回None，尝试直接初始化
            try:
                from selenium import webdriver
                cls.driver = webdriver.Chrome()
            except Exception as e:
                raise Exception(f"浏览器初始化失败: {e}\n"
                                "请手动下载chromedriver.exe并放在项目根目录")

        # 设置浏览器选项
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        print("浏览器初始化成功")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()


# 运行测试
if __name__ == "__main__":
    # 创建一个简单的测试用例
    class TestExample(MyTest):
        def test_example(self):
            self.driver.get("https://www.baidu.com")
            self.assertIn("百度", self.driver.title)
            print("测试通过！")


    unittest.main()