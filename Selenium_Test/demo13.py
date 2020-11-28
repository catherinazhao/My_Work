# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os

# selenium 屏幕截图

# webdriver内置捕获屏幕并保存方法
# 1. save.screenshot(filename)  获取当前屏幕截图并保存为指定文件， filename指指定保存的路径或者图片的文件名  常用
# 2. get_sreenshot_as_base64()  获取当前屏幕图base65编码字符串
# 3. get_screenshot_as_file(filename) 获取当前的屏幕截图，使用完整的路径 常用
# 4. get_screenshot_as_png()   获取当前屏幕截图的二进制文件数据


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		self.driver.maximize_window()
		self.driver.get("http://www.baidu.com")

	def test_screenshot(self):
		self.driver.find_element_by_id("kw").send_keys("selemium")
		self.driver.find_element_by_id("su").click()
		time.sleep(2)
		self.driver.save_screenshot("screenshot1.png")

		st = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
		file_name = st + '.png'

		path = os.path.abspath("ScreenShot")
		file_path = path + '/' + file_name

		print(111111111, file_path)

		self.driver.get_screenshot_as_file(file_path)

		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	case.test_screenshot()




