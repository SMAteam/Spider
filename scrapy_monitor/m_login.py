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
U_List = [{'USERNAME':'ifk513@163.com','PASSWORD':'KOAoym666yp'},{'USERNAME':'13054220294','PASSWORD':'nnf016407f'},{'USERNAME':'yuqemo@163.com','PASSWORD':'BXDfox641xW'},{'USERNAME':'mla352@163.com','PASSWORD':'BDXiix7532X'},{'USERNAME':'ioscce@163.com','PASSWORD':'CJQwdh109Ut'}]
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
        i = random.randint(0,4)
        self.username = U_List[i]['USERNAME']
        self.password = U_List[i]['PASSWORD']

    def __del__(self):
        self.browser.close()

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
        time.sleep(10)
        submit.click()

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'code_img')))
        except TimeoutException:
            print('未出现验证码')
            self.open()
        time.sleep(2)
        location = img.location
        size = img.size
        # top, bottom, left, right = location['y']+70, location['y'] +130, location['x']+120, location['x'] + 250
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        result = base64_api(uname='sendoh', pwd='whj970519', img=captcha)
        print(result)
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'W_btn_a')))
        cap = self.wait.until(EC.presence_of_element_located((By.ID, 'door')))
        cap.send_keys(result)
        submit.click()
        time.sleep(10)
        cookies = {i["name"]: i["value"] for i in self.browser.get_cookies()}
        print(len(cookies))
        print(cookies)


        return cookies



    def main(self):
        """
        批量获取验证码
        :return: 图片对象
        """
        try:
            self.open()
            return self.get_image()
        except:
            cookies = {i["name"]: i["value"] for i in self.browser.get_cookies()}
            return cookies


def get_cookie():
    num=0
    crack = CrackWeiboSlide()
    cookies={}
    while (len(cookies) <= 1):
        num = num+1
        print("获取第"+str(num)+"次")
        if(num>30):
            print("重新选择账号密码")
            crack = CrackWeiboSlide()
        print(len(cookies))
        cookies=crack.main()
    with open(os.path.join(os.path.dirname(__file__), '../data_model/cookie.json'), 'w') as f:
        json.dump(cookies, f,ensure_ascii=False)
        print(cookies)
        print("cookies写入成功")

if __name__ == '__main__':
    num = 0
    crack = CrackWeiboSlide()
    cookies={}
    while (len(cookies) <= 1):
        print("获取第"+str(num)+"次")
        num = num + 1
        if (num > 20):
            print("重新选择账号密码")
            crack = CrackWeiboSlide()
        print(len(cookies))
        cookies = crack.main()
        print(len(cookies))
        cookies=crack.main()
    with open(os.path.join(os.path.dirname(__file__), '../data_model/cookie.json'), 'w') as f:
        json.dump(cookies, f,ensure_ascii=False)
        print(cookies)
        print("cookies写入成功")
