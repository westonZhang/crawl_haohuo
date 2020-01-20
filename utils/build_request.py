# coding:utf-8
from utils.user_agent import UserAgentUtil

user_agent = UserAgentUtil()

base_header = {
    "accept": "application/json, text/plain, */*",
    "accept_encoding": "gzip, deflate, br",
    "accept_language": "zh-CN,zh;q=0.9,en;q=0.8",
    "origin": "http://haohuo.jinritemai.com",
    "sec_fetch_mode": "cors",
    "sec_fetch_site": "cross-site",
}


def build_request(url):
    """构建下载中心请求"""
    base_header["user_agent"] = user_agent.random_one()
    return {
        "url": {"url": url},
        "header": base_header
    }
