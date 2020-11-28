# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


import os
# selenium 中的鼠标和键盘事件被封装在ActionChains类中，正确的使用方法是ActionChains(driver).click(btn).perform()
# 鼠标类ActionChains
# 键盘类Keys
# http://sahitest.com/demo/


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		self.driver.maximize_window()
		# self.driver.get("http://sahitest.com/demo/clicks.htm")

	def test_mounse(self):
		# 双击
		btn = self.driver.find_element_by_xpath("/html/body/form/input[2]")
		ActionChains(self.driver).double_click(btn).perform()
		sleep(2)

		# 单击
		btn1 = self.driver.find_element_by_xpath("/html/body/form/input[3]")
		ActionChains(self.driver).click(btn1).perform()
		# 等价于 self.driver.find_element_by_xpath("/html/body/form/input[3]").click()

		# 点击右键, 通过find element方法获取了element元素，对element元素进行操作
		btn1 = self.driver.find_element_by_xpath("/html/body/form/input[4]")
		ActionChains(self.driver).context_click(btn1).perform()

		self.driver.quit()

	def test_keyboard(self):
		self.driver.get("http://www.baidu.com")
		kw = self.driver.find_element_by_id("kw")
		kw.send_keys("selenium")

		# 针对得到的元素对话框操作
		kw.send_keys(Keys.CONTROL, 'a')  # 全选
		sleep(2)
		kw.send_keys(Keys.CONTROL, 'x')  # 剪切
		sleep(2)
		kw.send_keys(Keys.CONTROL, 'v')  # 粘贴

		sleep(2)

		ele = self.driver.find_element_by_link_text("百度首页")

		#  注意ActionChains的用法，一定要加self.driver
		ActionChains(self.driver).move_to_element(ele).perform()
		sleep(3)

		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	# case.test_mounse()
	case.test_keyboard()



