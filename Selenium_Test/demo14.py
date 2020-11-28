# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep

# selenium定位frame , iframe
# frame标签有frameset, frame, iframe三种，frameset跟其他普通标签没有区别，不会影响到正常的定位， 而frame和iframe对selenium定位
# 而言是一样的， selenium有一组对frame进行操作
# 1. switch_to.frame(reference)  切换frame, reference是传入的参数，用来定位frame, 可以传入id, name, index以及selenium的WebElement
# 对象
# 2. switch_to.default_content()  返回主文档
# 3. switch_to.parent_frame()  返回父文档


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		self.driver.maximize_window()
		self.driver.get("http://sahitest.com/demo/framesTest.htm")

	def test1(self):
		#
		# self.driver.find_element_by_link_text("新闻").click()
		# handles = self.driver.window_handles
		# print(handles)
		#
		# while 1:
		# 	for handle in handles:
		# 		self.driver.switch_to.window(handle)
		# 		sleep(2)
		# 找到名为top的 frame
		top = self.driver.find_element_by_name("top")
		# 定位到指定的frame
		self.driver.switch_to.frame(top)
		# 找到其中的元素
		self.driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/a[1]").click()

		sleep(2)
		# 切换出frame
		self.driver.switch_to.default_content()
		# 找到第二个frame
		second = self.driver.find_element_by_xpath("/html/frameset/frame[2]")
		self.driver.switch_to.frame(second)
		self.driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/a[2]").click()

		sleep(2)
		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	case.test1()