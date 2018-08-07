#!/home/zodius/.virtualenvs/ctf2/bin/python
import config
import requests as req
from bs4 import BeautifulSoup
import sys

def login():
	s = req.session()

	url = 'https://cis.ncu.edu.tw/HumanSys/login'
	login = 'https://portal.ncu.edu.tw/j_spring_security_check'

	res = s.get(url, allow_redirects=True)

	res = s.post(login, data={"j_username":config.user, "j_password":config.passwd})
	return s

def sign(s):
	work = 'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn/create?ParttimeUsuallyId=66103'
	
	res = s.get(work)
	soup = BeautifulSoup(res.text, 'html.parser')
	hidden_form = soup.select('input[type="hidden"]')
	data = {k['name']:k['value'] for k in hidden_form}
	data['AttendWork'] = 'coding'
	data['functionName'] = 'doSign'
	work = 'https://cis.ncu.edu.tw/HumanSys/student/stdSignIn_detail'
	res = s.post(work, data=data)
	print(res.text)

s = login()
sign(s)
