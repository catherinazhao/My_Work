# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
import os

# 测试form表单操作步骤


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		dir_path = os.path.dirname(os.path.abspath(__file__))
		print("dir_path is: ", dir_path)
		file_path = "file:///" + dir_path + '/forms.html'
		form_path = os.path.join(dir_path, "forms.html")

		self.driver.get(form_path)

	def test_login(self):
		# 输入用户名和密码
		user_name = self.driver.find_element_by_id("username")
		user_name.send_keys("Admin")
		pass_word = self.driver.find_element_by_id("pwd")
		pass_word.send_keys("123")

		# 取得当前输入的用户名和密码
		print(user_name.get_attribute('value'))
		print(pass_word.get_attribute('value'))

		sleep(2)

		# 点击提交
		self.driver.find_element_by_id('submit').click()

		sleep(1)

		# 处理alert
		self.driver.switch_to.alert.accept()

		# 清除数据
		user_name.clear()
		pass_word.clear()


if __name__ == '__main__':
	case = TestCase()
	case.test_login()