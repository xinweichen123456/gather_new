
# ----------------------------------------------------------------------------------------------------------------------

import random
import requests
from lxml import etree
import time
from faker import Factory
from pymongo import MongoClient


# -----------------------------------------生成随机的请求头 User-Agent-----------------------------------------------------
def get_user_agent(num):
    factory = Factory.create()
    user_agent = []
    for i in range(num):
        user_agent.append({'User-Agent': factory.user_agent()})
    return user_agent


# -----------------------------------------爬取代理IP  主要爬取快代理-----------------------------------------------------
def get_proxy(page_num):
    """
    爬取代理IP 并检验IP的有效性
    :param page_num: 需要爬取的页数
    :return: proxies_list_use: 返回爬取的有效IP地址
    """
    headers = get_user_agent(5)

    # ip的格式 {'协议类型':'ip:端口'}
    proxies_list = []

    for i in range(1, 5):
        print('正在爬取代理第{}页的所有代理ip'.format(i))
        header_i = random.randint(0, len(headers) - 1)
        headers = headers[header_i]
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)

        page_text = requests.get(url=base_url, headers=headers).text

        tree1 = etree.HTML(page_text)

        tr_list = tree1.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')

        for tr in tr_list:
            http_type = tr.xpath('./td[@data-title="类型"]/text()')[0]
            ip = tr.xpath('./td[@data-title="IP"]/text()')[0]
            port = tr.xpath('./td[@data-title="PORT"]/text()')[0]

            proxies = {http_type: ip + ':' + port}
            proxies_list.append(proxies)
            # print(proxies)
            time.sleep(1)

    proxies_list_use = check_ip(proxies_list)

    save_ip(proxies_list_use)

    return proxies_list_use


# -----------------------------------------利用百度检验 爬取的代理IP的有效性-------------------------------------------------
def check_ip(proxies_list):
    """
    检测代理IP的质量 直接利用爬取的代理IP去访问百度 设置响应时间为0.1
    :param proxies_list:
    :return:
    """
    headers = get_user_agent(5)
    header_i = random.randint(0, len(headers) - 1)
    headers = headers[header_i]
    can_use = []
    for proxy in proxies_list:

        try:
            response = requests.get('https://www.baidu.com', headers=headers, proxies=proxy, timeout=0.1)
            if response.status_code == 200:
                can_use.append(proxy)
        except Exception as e:
            print('代理IP的错误为：', e)

    return can_use


# -----------------------------------------持久化存储到 MongoDB 中 便于后期从里面拿到有效的代理IP------------------------------
def save_ip(ip_list):
    """
    将爬取到代理IP存储到MongoDB中
    :param ip_list: 爬取到的有效IP （列表）
    :return:
    """
    client = MongoClient()
    time_info = time.strftime("%Y-%m-%d", time.localtime())
    collection = client['快代理'][time_info + '爬取的代理IP']
    collection.insert_many(ip_list)


# -----------------------------------------读取MongoDB 中的有效IP 用来伪装IP地址爬取其他的网站url------------------------------
def read_ip():
    """
    从MongoDB中随机调用一个有效的IP
    :return:proxy 返回数据库中随机的有效IP地址
    """
    client = MongoClient()
    time_info = time.strftime("%Y-%m-%d", time.localtime())
    collection = client['快代理'][time_info + '爬取的代理IP']
    ip_list = list(collection.find())

    proxy_i = random.randint(0, len(ip_list) - 1)
    proxy = {ip_list[proxy_i]['http_type']: ip_list[proxy_i]['ip_port']}

    return proxy


# -------------------------------------------------主函数main()----------------------------------------------------------
def main():
    useful_ip = get_user_agent(5)
    proxy = read_ip()
