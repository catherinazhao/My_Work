# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.remote.webelement import WebElement

chrome = webdriver.Chrome(executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")

chrome.get("http://www.baidu.com")


# chrome.find_element_by_id('kw').send_keys('北京今天天气')
# sleep(2)
# chrome.find_element_by_id('su').click()
# sleep(2)
# print(type(chrome.find_element_by_id('kw')))
# chrome.quit()

# e = WebElement;

chrome.find_element_by_link_text('新闻').click()
windows = chrome.window_handles

while 1:
	for handle in windows:
		chrome.switch_to.window(handle)
		sleep(2)
		# chrome.switch_to_window(handle)：



