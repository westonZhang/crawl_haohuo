# coding:utf-8
import utils.logics as logics


def extractor_sales(salesStr):
    """解析销量"""
    sales = 0
    if "热销" in salesStr:
        sales = logics.DEFAULT_HOT_SALES
    elif "热" in salesStr:
        salesStr = salesStr.replace("热卖", "").replace("热买", "").replace("+", "").replace("件", "")
        sales = int(salesStr)
    elif "爆" in salesStr:
        salesStr = salesStr.replace("爆卖", "").replace("爆买", "").replace("+", "").replace("件", "")
        if "万" in salesStr:
            sales = int(float(salesStr.replace("万", "")) * 10000)
        else:
            sales = int(salesStr)
    else:
        print("未知销量情况:", salesStr)
    return sales
