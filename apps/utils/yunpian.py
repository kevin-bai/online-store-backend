# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/7 20:54'

import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【生鲜超市】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        return_dict = json.loads(response.text)
        return return_dict


if __name__ == "__main__":
    yunpian = YunPian('473111e06a4d8399c2f2f4555b745cd4')
    yunpian.send_sms(code='33333',mobile=13818966564)