# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep

#  selenium执行javascript, 分为两种方式，同步和异步


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		self.driver.maximize_window()
		self.driver.get("http://www.baidu.com")

	def test1(self):
		# 弹出一个alert框
		self.driver.execute_script("alert('test')")
		sleep(2)
		self.driver.switch_to.alert.accept()
		sleep(2)

	# 获取标题
	def test2(self):
		js = "return document.title"
		title = self.driver.execute_script(js)
		print(title)

	def test3(self):
		js = 'var q = document.getElementById("kw"); q.style.border="2px solid red"'
		self.driver.execute_script(js)
		sleep(2)

	def test4(self):
		self.driver.find_element_by_id("kw").send_keys("selenium")
		self.driver.find_element_by_id("su").click()
		sleep(2)
		js = 'window.scrollTo(0, document.body.scrollHeight)'
		self.driver.execute_script(js)
		sleep(2)

		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	case.test1()
	case.test2()
	case.test3()
	case.test4()

