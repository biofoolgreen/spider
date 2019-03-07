# -*- coding:utf-8 -*-
import os
import sys
import requests
from bs4 import BeautifulSoup


class NovelSpider(object):
    """
    爬取网站https://www.biqukan.com/1_1094/下的所有小说章节
    """
    def __init__(self):
        self._root_url = r"http://www.biqukan.com/"
        self.url = r"http://www.biqukan.com/1_1094/"
        self.chapname = []          # 章节名
        self.chap_urls = []         # 章节链接
        self.num_chaps = 0         # 章节数
    
    def get_chap_urls(self):
        """获取所有章节的url"""
        req = requests.get(url=self.url)
        # 加入解析方式，否则findall得到的结果不完整
        bs = BeautifulSoup(req.text, "html5lib")
        div = bs.find_all('div', class_='listmain')
        print(len(div[0]))
        href_bs = BeautifulSoup(str(div[0]))
        href = href_bs.find_all("a")
        print(len(href))
        self.num_chaps = len(href[15:])    # 剔除前15个没用章节
        for cp in href[15:]:
            self.chapname.append(cp.string)
            self.chap_urls.append(self._root_url + cp.get("href"))
    
    def get_chap_content(self, target):
        """获取每章节的内容"""
        req = requests.get(url=target)
        bs = BeautifulSoup(req.text, "html5lib")
        texts = bs.find_all('div', class_='showtxt')
        if len(texts)>0:
            content = texts[0].text.replace("\xa0"*8, "\n")
        else:
            content = " "
        return content
    
    def writer(self, fpath, chapname, chaptext):
        """将爬取的内容写入文件"""
        with open(fpath, "a", encoding='utf-8') as f:
            f.write(chapname + "\n" + "="*100 + "\n")
            f.writelines(chaptext)
            f.write("\n\n")

def main():
    ns = NovelSpider()
    ns.get_chap_urls()
    fpath = "一念永恒.txt"
    print("开始下载。。。一共 %s 章" % ns.num_chaps)
    for i in range(ns.num_chaps):
        print(ns.chapname[i])
        ns.writer(fpath, ns.chapname[i], ns.get_chap_content(ns.chap_urls[i]))
        sys.stdout.write("  已下载 ： %.3f%%" % (float((i+1)/ns.num_chaps)) + "\r")
        sys.stdout.flush()
    print("下载完成。")


if __name__ == "__main__":
    main()