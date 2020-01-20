# coding: utf-8
import requests
import time
import json
import base64
import utils.logics as logics
from utils.user_agent import UserAgentUtil
from utils.build_request import build_request
from spider.spider_services.mysql_api_service import MysqlApiService
from spider.spider_services.dc_service import DcService
from utils.extractor_sales import extractor_sales


class SpiderService(object):
    """抓取服务类"""

    def __init__(self):
        self.dc_service = DcService()
        self.user_agent = UserAgentUtil()
        self.mysql_api = MysqlApiService()
        self.session = requests.Session()
        self.haohuo_base_url = "https://ec.snssdk.com/product/lubanajaxstaticitem?id={}&token=&page_id=&b_type_new=0"

    def send_task(self, products):
        """发送任务"""
        update_products = list()
        for product in products:
            product_code = product["product_code"]
            send_data = build_request(self.haohuo_base_url.format(product_code))
            resp = self.dc_service.dc_send(send_data)
            update_products.append({
                "product_code": product_code,
                "status": logics.SEARCHING
            })
            print("product_code:{},{}".format(product_code, resp.text))
            time.sleep(0.1)

        return update_products

    def receive_result(self, products):
        """获取结果"""
        for product in products:
            product_code = product["product_code"]
            receive_data = {
                "url": {"url": self.haohuo_base_url.format(product_code)}
            }
            resp = self.dc_service.dc_receive(receive_data)
            res_json = json.loads(resp.text)
            if res_json["code"] != 200 or not res_json["data"] or not res_json["data"]["rdata"]:
                continue

            data_json = json.loads(res_json["data"]["rdata"])
            for unique_md5 in data_json:
                result = base64.b64decode(data_json[unique_md5]["result"]).decode("utf-8")
                info_json = json.loads(result)
                current_date = time.strftime("%Y-%m-%d", time.localtime(info_json["data"]["current_time"]))
                today = time.strftime("%Y-%m-%d")
                if current_date != today:
                    resp = self.mysql_api.my_update([{"product_code": product_code, "status": logics.NO_NEED_SEARCH}])
                    print(resp.text.strip())
                    continue

                resp = self.mysql_api.my_update([{"product_code": product_code, "status": logics.SEARCH_SUCCESS}])
                print(resp.text.strip())

                save_data = {
                    "product_code": product_code,
                    "price": int(info_json["data"]["discount_price"] / 100),
                    "sales": extractor_sales(info_json["data"]["sell_num"]),
                    "date": today
                }

                resp = self.mysql_api.my_save(save_data)
                print(resp.text.strip())

            time.sleep(0.1)
