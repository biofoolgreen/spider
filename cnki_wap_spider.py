#!/usr/bin/env python
# coding=UTF-8
'''
@Description: 爬取手机知网
@Version: 
@Author: biofool2@gmail.com
@LastEditors: Please set LastEditors
@Date: 2019-03-08 11:47:00
@LastEditTime: 2019-03-08 15:38:59
'''

import os
import time
import json
import random
import requests
# import pandas as pd
from bs4 import BeautifulSoup as BS
from urllib.parse import quote


def rand_header():
    agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
        'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    headers = {
            "User-Agent": random.choice(agents),
            "Accept":"*/*",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Connection":"keep-alive",
            "Host": "wap.cnki.net",
            "Referer": "http://wap.cnki.net/touch/web",
            "Cookie": "UM_distinctid=165effd462a3a2-01fa8a8c0e61b1-9393265-1fa400-165effd462b100; Ecp_ClientId=4190307162501611368; Ecp_IpLoginFail=190307223.255.127.34; cnkiUserKey=f5c9af9f-3c57-d0b0-b948-bc0bd9a8d859; SID=201139; ASP.NET_SessionId=wndzz3hxjlkeg45dfi3j2pxl; Search_History=%5b%7b%22SearchType%22%3a101%2c%22SearchKeyWord%22%3a%22%e7%85%a4%e7%9f%bf%22%7d%2c%7b%22SearchType%22%3a101%2c%22SearchKeyWord%22%3a%22%e7%85%a4%e7%9f%bf%22%7d%2c%7b%22SearchType%22%3a101%2c%22SearchKeyWord%22%3a%22%e7%85%a4%e7%9f%bf%22%7d%2c%7b%22SearchType%22%3a101%2c%22SearchKeyWord%22%3a%22%e7%85%a4%e7%9f%bf%22%7d%2c%7b%22SearchType%22%3a101%2c%22SearchKeyWord%22%3a%22%e7%85%a4%e7%9f%bf%22%7d%5d; touchThirdLoginReturnUrl=http%3a%2f%2fwap.cnki.net%2ftouch%2fweb%2fArticle%2fSearch%2f%3fkw%3d%e7%85%a4%e7%9f%bf",
            "Upgrade-Insecure-Requests": "1"}   
    return headers


def get_links(keywords):
    kw = quote(keywords)
    start_url = r"http://wap.cnki.net/touch/web/Article/Search/?kw=%s&field=5" % kw
    print(start_url)

    req = requests.get(url=start_url, headers=rand_header(), verify=False)
    # print(req.text)
    start_page = BS(req.text, "html5lib")
    div0 = start_page.find_all('div', class_='g-search-body c-book__person-outer')
    print(len(div0))
    div1 = BS(str(div0[0]), "html5lib")
    content = div1.find_all('div', class_="c-company__body-item")
    # print(content)
    # names = []
    links = []
    for i in range(len(content)):
        ct = content[i]
        text = BS(str(ct), 'html5lib')
        title = text.find_all("a")[0]
        # name = text.find_all("div", class_="c-company__body-title  c-company__body-title-blue")[0]
        link = title.get("href")
        # names.append(name)
        links.append(link)
    # print(links)
    return links


def get_content(url):
    req = requests.get(url=url, headers=rand_header(), verify=False)
    page = BS(req.text, 'html5lib')
    title = page.find_all('div',class_="c-card__title2")
    print(title)
    content = page.find_all('div', class_='c-card__aritcle')[0]
    kw = page.find_all('div', class_='c-card__paper-content c-card__paper-content-normal')
    return title, content, kw


if __name__ == "__main__":
    keywords = "煤矿"
    links = get_links(keywords)
    cnki_dicts = []
    for link in links:
        print("正在处理 ： %s" % link)
        t, c, kw = get_content(link)
        cdic = {}
        cdic["title"] = t
        cdic["content"] = c
        cdic["kws"] = kw
        cnki_dicts.append(cdic)

    print(cnki_dicts)
