import _thread
import os
import random
import sys
import time

import jsons
import requests

from util import CommonUtil


class WechatLogin:

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Referer': 'https://mp.weixin.qq.com/'
        }
        self.QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'webWeixinQr.jpg'
        self.username = "1379960679@qq.com"
        self.password = "cxxxxxxxxxx."
        self.token = ''

    def weixin_login(self):
        url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
        params = {
            'username': self.username,
            'pwd': CommonUtil.md5(self.password),
            'imgcode': '',
            'f': 'json'
        }
        response = self.session.post(url, data=params, headers=self.headers, verify=False)
        if response.status_code == 200:
            target = response.content.decode('utf-8')
            print(target)
            self.get_weixin_login_qrcode()

    def get_weixin_login_qrcode(self):
        url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300"
        response = self.session.get(url, headers=self.headers, verify=False)
        # target = response.content.decode('utf-8')
        # print(target)
        self.tip = 1
        with open(self.QRImgPath, 'wb') as f:
            f.write(response.content)
            f.close()
        # 打开二维码
        if sys.platform.find('darwin') >= 0:
            os.subprocess.call(['open', self.QRImgPath])  # 苹果系统
        elif sys.platform.find('linux') >= 0:
            os.subprocess.call(['xdg-open', self.QRImgPath])  # linux系统
        else:
            os.startfile(self.QRImgPath)  # windows系统
        print('请使用微信扫描二维码登录')

    def check_login(self):
        while True:
            url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1"
            response = self.session.get(url, headers=self.headers, verify=False)
            json = jsons.loads(response.text)
            if json["status"] == 1:
                self.login()
                break
            time.sleep(10)

    def login(self):
        url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"
        data = {
            'f': 'json',
            'ajax': 1,
            'random': random.random()
        }
        response = self.session.post(url, data=data, headers=self.headers, verify=False)
        # {"base_resp":{"err_msg":"ok","ret":0},"redirect_url":"/cgi-bin/home?t=home/index&lang=zh_CN&token=1502993366"}
        json = jsons.loads(response.text)
        redirect_url = json["redirect_url"]
        self.token = redirect_url[redirect_url.rfind("=") + 1:len(redirect_url)]


if __name__ == '__main__':
    wechat = WechatLogin()
    wechat.weixin_login()
    _thread.start_new_thread(wechat.check_login(), ("Thread-1", 2,))
