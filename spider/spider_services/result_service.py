# coding: utf-8
import time
import json
import base64
import utils.logics as logics
from utils.extractor_sales import extractor_sales
from spider.spider_services.mysql_api_service import MysqlApiService


class ResultService(object):
    """结果类"""

    def __init__(self):
        self.mysql_api_service = MysqlApiService()

    def handle_receive_result(self, data_json, product_code):
        """处理接收结果"""
        for unique_md5 in data_json:
            result = base64.b64decode(data_json[unique_md5]["result"]).decode("utf-8")
            info_json = json.loads(result)
            current_date = time.strftime("%Y-%m-%d", time.localtime(info_json["data"]["current_time"]))
            today = time.strftime("%Y-%m-%d")
            if current_date != today:
                self.mysql_api_service.my_update([{"product_code": product_code, "status": logics.NO_NEED_SEARCH}])
                continue

            save_data = {
                "product_code": product_code,
                "price": int(info_json["data"]["discount_price"] / 100),
                "sales": extractor_sales(info_json["data"]["sell_num"]),
                "date": today
            }
            self.mysql_api_service.my_update([{"product_code": product_code, "status": logics.NO_NEED_SEARCH}])
            resp = self.mysql_api_service.my_save(save_data)
            print(resp.text.strip())
