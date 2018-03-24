#-*- coding: utf-8 -*-
'''
	Automatic signup to NCU csie system with selenium
'''
import time
import sys
from pyvirtualdisplay import Display
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

USER_NAME = ""
PASSWORD = ""
LOGIN_WORK = u''

def check_login(browser):
	try:
		logout_btn = browser.find_element(By.LINK_TEXT,'登出')
		return True
	except NoSuchElementException:
		return False

def login(browser):
	# find login btn
	try:
		login_btn = browser.find_element(By.LINK_TEXT,'登入')
		login_btn.click()
		user = browser.find_element(By.NAME,'j_username')
		user.clear()
		user.send_keys(USER_NAME)
		passwd = browser.find_element(By.NAME,'j_password')
		passwd.clear()
		passwd.send_keys(PASSWORD)
		browser.find_element(By.XPATH,'//button[@type="submit"]').click()
		return True

	except NoSuchElementException:
		print('Can\'t find element')
		return False


#init
win = Display(visible=0).start()
browser = webdriver.Firefox()
waiter = WebDriverWait(browser, 30)

browser.get('https://cis.ncu.edu.tw/HumanSys/')
print('open %s' % browser.title)

# check if logined or not
if not check_login(browser):
	login(browser)
	#todo check if login succees

# open sign up page
group_btn = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.LINK_TEXT,'兼任助理/工讀生/臨時工專區')))
ActionChains(browser).move_to_element(group_btn).perform()

group_btn = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.LINK_TEXT,'簽到退作業')))
time.sleep(1)
group_btn.click()

# open table by job name
xpath = './/table[@id="table1"]/tbody/tr[td[2] = "%s"]/td[6]/a[1]' % LOGIN_WORK
xpath = xpath.encode('utf-8')
job_btn = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,str(xpath))))
job_btn.click()

# check sign-in or sign-out
try:
	print('finding sign-in')
	sign_in = WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.XPATH,'.//input[@id="signin"]')))
	sign_in.click()
	print('sign-in success')
except TimeoutException:
	try:
		print('finding sign-out')
		sign_out = WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.XPATH,'.//input[@id="signout"]')))
		work_content = browser.find_element(By.XPATH,'.//textarea[@id="AttendWork"]')
		work_content.send_keys('coding')
		sign_out.click()
		print('sign-out success')
	except (TimeoutException, NoSuchElementException):
		print('Error, can\'t recognize sign-in or sign-out')
		print('quitting')
		browser.quit()
		sys.exit(1)

browser.quit()
