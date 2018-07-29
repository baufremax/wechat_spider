# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib.request
import re

url =  'https://accounts.douban.com/login'
#构造post数据
data={
    # 'redir': 'https://www.douban.com/people/138461169/',
    'form_email':'1914185859@qq.com',
    'form_password':'dbwzy852845',
    'login':u'登录'
}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
r = requests.post(url, data, headers=headers)
page = r.text
#利用bs4获得验证码图片地址
soup = BeautifulSoup(page,"html.parser")
captcha_url = soup.find('img',id='captcha_image')['src']
#利用正则获得验证码ID
pattern = re.compile('<input type="hidden" name="captcha-id" value="(.*?)"/')
captcha_id = re.findall(pattern, page)
#将验证码图片保存到本地
urllib.request.urlretrieve(captcha_url,"./captcha.jpg")
captcha = input('please input the captcha:')
data['captcha-solution'] = captcha
data['captcha-id'] = captcha_id

r = requests.post(url, data=data, headers=headers)

page = r.text
print(page)

