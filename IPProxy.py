# -*- coding: utf-8 -*-
# @Date    : 2017-3-3 16:28:15
# @Author  : youth-lee (you@example.org)
# @Link    : http://www.cnblogs.com/youth-lee/
# @Version : Ver 0.1

'''
1、从西刺代理往上获取第一页国内高匿的IP
2、使用多线成检验获取的IP是否可在访问网易
3、可调用
    from IPProxy import getProxy
    ip_list = getProxy.ip_list_able
'''

import requests
import datetime
from bs4 import BeautifulSoup
from threading import Thread


class getProxy():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER"
        self.header = {"User-Agent": self.user_agent}
        self.start_url = "http://www.xicidaili.com/nn/"
        self.ip_list = []
        self.ip_list_able = []

        self.get_ip()
        self.check_ip_list()

        print("获取了%s个可用代理" % len(self.ip_list_able))

    def getContent(self, url):
        # 获取网页内容并返回
        content = requests.get(url, headers=self.header)
        soup = BeautifulSoup(content.text, "lxml")
        return soup

    def get_ip(self):
        soup = self.getContent(self.start_url)
        tr_soup = soup.find("table", id="ip_list").find_all("tr")
        # 把第一个tr标签剔除，第一个tr为标题行
        tr_soup.pop(0)
        for tr in tr_soup:
            items = tr.find_all("td")

            if items is not []:
                ip = items[1].get_text().strip()
                port = items[2].get_text().strip()
                ip_port = ip + ":" + port
                self.ip_list.append(ip_port)

    def check_ip_list(self):
        # 使用多线程检测ip是否可用
        threads = []
        for ip_port in self.ip_list:
            t = Thread(target=self.check_ip, args=[ip_port])
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def check_ip(self, ip_port):
        # 如果能正常访问则将ip放入到ip_list_able中
        if self.is_Alive(ip_port):
            self.ip_list_able.append(ip_port)

    def is_Alive(self, ip_port):
        # 使用代理IP去访问网易，能成功则能使用
        proxy = {"http": ip_port}
        test_url = "http://www.163.com"

        try:
            test_content = requests.get(
                test_url, headers=self.header, proxies=proxy, timeout=1)
            if test_content.status_code == 200:
                # print("%s满足使用条件！" % (ip_port))
                return True
            else:
                # print("%s不满足使用条件！" % (ip_port))
                return False
        except:
            # print("%s不满足使用条件！" % (ip_port))
            return False


if __name__ == "__main__":

    time1 = datetime.datetime.now()

    obj = getProxy()

    print("获得%s个代理IP！" % len(obj.ip_list_able))

    for ip in obj.ip_list_able:
        print(ip)

    time2 = datetime.datetime.now()
    print("耗时：%s" % str(time2 - time1))
