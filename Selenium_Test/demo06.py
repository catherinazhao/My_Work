# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
import os


# 测试checkbox和radio button
class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		dir_path = os.path.dirname(os.path.abspath(__file__))
		form_path = os.path.join(dir_path, 'forms2.html')
		self.driver.get(form_path)

	# checkbox是方框的选项，可以进行多选
	def test_checkbox(self):
		swimming = self.driver.find_element_by_name("swimming")
		# 判断当前元素是否选中, 未选中的情况下，在选择
		if not swimming.is_selected():
			swimming.click()

		sleep(2)
		reading = self.driver.find_element_by_name("reading")
		if not reading.is_selected():
			reading.click()

		sleep(2)
		# 取消选中
		reading.click()

	# radio button是圆圈的选项，不可进行多选，具有排他性，只能存在其一
	def test_radio_button(self):
		genders = self.driver.find_elements_by_name("gender")
		gender1 = genders[0]

		genders[0].click()
		sleep(2)

		genders[1].click()
		sleep(2)

		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	case.test_checkbox()
	case.test_radio_button()



