# coding: utf-8
import time
import json
import utils.logics as logics
from utils.search_time import is_between_search_time
from spider.spider_services.mysql_api_service import MysqlApiService
from spider.spider_services.spider_service import SpiderService
from spider.spider_services.result_service import ResultService


class BaseSpider(object):

    def __init__(self):
        self.spider_service = SpiderService()
        self.mysql_api_service = MysqlApiService()
        self.result_service = ResultService()

    def send(self):
        print("Start to send task.")
        while True:
            if not is_between_search_time():
                print("Now is not between search time, sleep 1 minute...")
                time.sleep(60)
                continue

            resp = self.mysql_api_service.my_query(logics.NO_SEARCH)
            products = json.loads(resp.text)["data"]
            if len(products) == 0:
                print("Now no task need send, sleep 1 minute...")
                time.sleep(60)
                continue

            update_products = self.spider_service.send_task(products)
            resp = self.mysql_api_service.my_update(update_products)
            print(resp.text)

    def receive(self):
        print("Start to receive result.")
        while True:
            if not is_between_search_time():
                print("Now is not between search time, sleep 1 minute...")
                time.sleep(60)
                continue

            resp = self.mysql_api_service.my_query(logics.SEARCHING)
            products = json.loads(resp.text)["data"]
            if len(products) == 0:
                print("Now no task need receive, sleep 1 minute...")
                time.sleep(60)
                continue

            self.spider_service.receive_result(products)
