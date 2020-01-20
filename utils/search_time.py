# coding:utf-8
import os
import datetime
import settings


def is_between_search_time():
    os.environ['TZ'] = 'Asia/Shanghai'  # 设置时区

    now = datetime.datetime.now()
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + settings.START_TIME,
                                            "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + settings.END_TIME,
                                          "%Y-%m-%d %H:%M:%S")

    return start_time < now and now < end_time
