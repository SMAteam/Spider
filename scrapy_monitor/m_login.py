#-*- coding = utf-8 -*-


#-*- coding = utf-8 -*-

import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import base64
import os
import random
from sys import version_info
U_List = [{'USERNAME':'13954630660','PASSWORD':'whj123456'}]
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')


def base64_api(uname, pwd, img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""
class CrackWeiboSlide():
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Flogin.weibo.cn%2Flogin%2F'
        # self.url = 'https://login.sina.com.cn/signup/signin.php'
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 15)
        i = random.randint(0,0)
        self.username = U_List[i]['USERNAME']
        self.password = U_List[i]['PASSWORD']

    # def __del__(self):
    #     self.browser.close()

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(3)
        submit.click()
        yanzhengma  = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'm-btn-orange')))
        yanzhengma.click()
        time.sleep(10)
        keyword = 552921
        passt = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
        passt.send_keys(keyword)
        login = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'm-btn-block')))
        login.click()
        time.sleep(10)
        cookies = {i["name"]: i["value"] for i in self.browser.get_cookies()}
        print(len(cookies))
        print(cookies)
        time.sleep(10)
    def main(self):
        """
        批量获取验证码
        :return: 图片对象
        """
        try:
            self.open()
        except:
            cookies = {i["name"]: i["value"] for i in self.browser.get_cookies()}
            return cookies

if __name__ == '__main__':
    num = 0
    crack = CrackWeiboSlide()
    cookies={}
    crack.main()
