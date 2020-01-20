# coding: utf-8
import time
import json
import requests
import settings


class MysqlApiService(object):
    """数据库操作"""

    def my_query(self, status=0):
        while True:
            try:
                resp = requests.get(settings.MYSQL_QUERY_API + str(status))
                return resp
            except requests.exceptions.ConnectionError:
                print("Mysql query api ConnectionError, time sleep 30 seconds then try again.")
                time.sleep(30)

    def my_save(self, save_data):
        while True:
            try:
                resp = requests.post(settings.MYSQL_SAVE_API, data=json.dumps(save_data))
                return resp
            except requests.exceptions.ConnectionError:
                print("Mysql save api ConnectionError, time sleep 30 seconds then try again.")
                time.sleep(30)

    def my_update(self, update_products):
        while True:
            try:
                resp = requests.post(settings.MYSQL_UPDATE_API, data=json.dumps(update_products))
                return resp
            except requests.exceptions.ConnectionError as e:
                print("Mysql update api ConnectionError, time sleep 30 seconds then try again.")
                time.sleep(30)
                return "Update error: {}".format(e)
