# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
import os


# selenium 操作下拉列表，需要用到selenium中的一个工具类Select
# import一个模块可以使用快捷键 alt + 回车
from selenium.webdriver.support.select import Select


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		dir_path = os.path.dirname(os.path.abspath(__file__))
		form_path = os.path.join(dir_path, 'forms3.html')
		self.driver.get(form_path)

	def test_select(self):
		# 通过id选择
		se = self.driver.find_element_by_id("provise")
		select = Select(se)
		# 通过inde选择
		select.select_by_index(2)

		sleep(2)
		# 通过表单value选择
		select.select_by_value('bj')
		sleep(2)

		# 通过可视化显示文本选择
		select.select_by_visible_text('TianJin')
		sleep(1)

		self.driver.quit()

	def test_multiple_select(self):
		se = self.driver.find_element_by_id("provise")
		select = Select(se)

		for i in range(0, 3):
			select.select_by_index(i)

		sleep(2)
		# 反向选择
		select.deselect_all()

		sleep(2)

	# 测试所有选项
	def test_options(self):
		se = self.driver.find_element_by_id("provise")
		select = Select(se)

		for option in select.options:
			print(option.text)


if __name__ == '__main__':
	case = TestCase()
	# case.test_select()
	# case.test_multiple_select()
	case.test_options()