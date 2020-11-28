# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as CE


import os

# selenium中三种等待方式()
# 在UI自动化测试中，必然会遇到环境不稳定，网络慢的情况，这时如果不做任何处理的话，代码会由于没有找到元素而报错。另外，一种情况就是页面使ajax
# 异步加载机制。这时我们就要用到wait, 而在selenium中，我们一共可以用到三种等待。

# 1. time.sleep(固定时间的等待)
# 开发自动化测试框架过程中，最忌讳使用的python自带模块的time的sleep方法进行等待， 虽然可以自定义等待时间，但当网络条件良好时， 依旧按照预设的时间
# 等待， 导致整个项目的自动化测试时间无限延长， 不建议使用
# 但在脚本调试过程中， 可以使用

# 2. implicitly_wait（等待时间）
# 一次设置，全程有效。
# 隐式等待实际是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到结束，然后执行下一步。这样的隐式等待有个坑，JavaScript
# 一般都放在我们的body的最后进行加载， 实际这是页面上元素都已经加载完成，我们却在等待全部页面加载结束。
# 隐式等待对整个driver生命周期都起作用，在最开始设置一次即可。

# 3. WebDriverWait(显示等待)
# 动态轮巡，
# WebDriverWait是selenium提供的得到显示等待模块引入路径
# from slenium.webdriver.support.wait import WebDriverWait
# WebDriverWait参数： driver: 传入WebDriver的实例； timeout: 超长时间，等待的最长时间；polt_frenquency: 调用until或until_not方法的时间间隔，
# 默认为0.5s; ignored_exceptions : 忽略异常

# 两种重要的方法(until & until_not)：
# method：在等待期间，没隔一段时间调用这个传入的方法，知道返回值不是false
# message: 如果超时， 抛出TimeoutException, 将message传入异常


class TestCase(object):
	def __init__(self):
		self.driver = webdriver.Chrome(
			executable_path=r"C:\Users\yangzhao\AppData\Local\Programs\selenium_driver\chromedriver.exe")
		self.driver.get("http://www.baidu.com")

	# sleep方法较耗性能
	def test_sleep(self):
		self.driver.find_element_by_id("kw").send_keys("selenium")

		sleep(2)  # 线程阻塞 blocking wait
		self.driver.find_element_by_id("su").click()

		sleep(2)
		self.driver.quit()

	# 隐式等待
	def test_implicitly(self):
		# 若隐式等待和显示等待同时存在，则按照最长的timeout选择
		self.driver.implicitly_wait(10)  # 开始的时候设置超时时间，若元素未出现，则等待
		self.driver.find_element_by_id("kw").send_keys("selenium")
		self.driver.find_element_by_id("su").click()
		self.driver.quit()

	def test_webdriverwait(self):
		# 第三个参数是轮询的时间， 多长时间轮询一次，判定是否
		wait = WebDriverWait(self.driver, 2)
		# 直到条件成功, 判断title， 是否出现
		wait.until(CE.title_is("百度一下，你就知道"))
		# self.driver.find_element_by_id("kw").send_keys("selenium")
		# self.driver.find_element_by_id("su").click()
		self.driver.quit()


if __name__ == '__main__':
	case = TestCase()
	case.test_webdriverwait()