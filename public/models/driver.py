#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'tina'

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import setting
import configparser

def browser():
    """
    启动浏览器驱动
    :return: 返回浏览器驱动URL
    """
    try:
        con = configparser.ConfigParser()
        con.read(setting.CONFIG_DIR, encoding='utf-8')
        # driver = webdriver.Chrome(executable_path='driver/chromedriver')
        os.environ['webdriver.chrome.driver'] = r'G:\DemoUI-master\driver\chromedriver.exe'
        service = Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        driver.get(con.get("WebURL","URL"))
        return driver
    except Exception as msg:
        print("驱动异常-> {0}".format(msg))
