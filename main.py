import time
import threading
from spider.base_spider import BaseSpider

spider = BaseSpider()


def run():
    threading_send_task = threading.Thread(target=spider.send)
    threading_send_task.start()
    time.sleep(60)
    for i in range(5):
        threading_receive_result = threading.Thread(target=spider.receive)
        threading_receive_result.start()
        time.sleep(30)


if __name__ == '__main__':
    print("Start to run.")
    run()
