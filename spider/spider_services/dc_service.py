# coding: utf-8
import time
import json
import requests
import settings


class DcService(object):
    """下载中心类"""

    def __init__(self):
        pass

    def dc_send(self, send_data):
        """发送请求"""
        while True:
            try:
                resp = requests.post(settings.DC_SEND_API, data=json.dumps(send_data))
                return resp
            except requests.exceptions.ConnectionError:
                print("Dc send api ConnectionError, time sleep 30 seconds then try again.")
                time.sleep(30)

    def dc_receive(self, receive_data):
        """接收结果"""
        while True:
            try:
                resp = requests.post(settings.DC_RECEIVE_API, data=json.dumps(receive_data))
                return resp
            except requests.exceptions.ConnectionError:
                print("Dc receive api ConnectionError, time sleep 30 seconds then try again.")
                time.sleep(30)
