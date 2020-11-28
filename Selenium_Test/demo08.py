# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
import os

# selenium处理弹框
# 页面上的弹框有三种， alert(用来提示)； confirm(用来确认)； prompt(输入内容)


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		dir_path = os.path.dirname(os.path.abspath(__file__))
		form_path = os.path.join(dir_path, 'test_alert.html')
		self.driver.get(form_path)

	def test_alert(self):
		# 点击
		self.driver.find_element_by_id('alert').click()
		# 切换到alert, 对alert进行操作
		alert = self.driver.switch_to.alert

		sleep(3)
		# 接受alert警告
		alert.accept()

	# 测试confirm, 涉及是否删除数据
	def test_confirm(self):
		self.driver.find_element_by_id('confirm').click()
		confirm = self.driver.switch_to.alert
		print(confirm.text)
		# 接受confirm操作
		sleep(3)
		# confirm.accept()

		# 拒绝删除，选否定
		confirm.dismiss()

	# 测试需要输入内容
	def test_prompt(self):
		self.driver.find_element_by_id("prompt").click()
		prompt = self.driver.switch_to.alert
		print(prompt.text)
		prompt.accept()
		# prompt.dismiss()


if __name__ == "__main__":
	case = TestCase()
	# case.test_alert()
	# case.test_confirm()
	case.test_prompt()

	case.driver.quit()
