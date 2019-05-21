import re
import csv
import time
import random
import requests
import html2text
from lxml.html import etree
from fake_useragent import UserAgent
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DB = 'bids'
DECODE = 'GBK'
REQUEST_TIMEOUT = 5
UA = UserAgent()


def connect_col():
    """连接到数据库的collection"""
    db = MongoClient()[DB]
    return db.bids


class Parser:
    """解析类。包括从请求到解析全部步骤所用到的函数"""
    def __init__(self, decode='utf-8'):
        self.decode = decode
        self.col = connect_col()

    def get(self, url, **kwargs):
        """requests get封装"""
        try:
            if 'headers' in kwargs:
                kwargs['headers'].update({'User-Agent': UA.random})
            return requests.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        except:
            return

    def post(self, url, data, **kwargs):
        """requests post封装"""
        try:
            if 'headers' in kwargs:
                kwargs['headers'].update({'User-Agent': UA.random})
            return requests.post(url, json=data, timeout=REQUEST_TIMEOUT, **kwargs)
        except:
            return

    def html2tree(self, html):
        """html转为etree"""
        try:
            return etree.HTML(html)
        except:
            return

    def resp2x(self, resp, json=False):
        """response返回类型"""
        try:
            return resp.content.decode(self.decode) if json is False else resp.json()
        except:
            return ''

    def url2tree(self, url, **kwargs):
        """请求url到转化为etree的全部过程封装"""
        resp = self.get(url, **kwargs)
        html = self.resp2x(resp)
        return self.html2tree(html)

    def url2text(self, url, **kwargs):
        """访问url，并返回经过html2text处理过的text"""
        resp = self.get(url, **kwargs)
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(self.resp2x(resp))

    def get_total_page(self, url, last_page, xp=True):
        """从初始url获取总页数"""
        resp = self.get(url)
        html = self.resp2x(resp)
        if html is None:
            return 1
        if xp is True:
            tree = self.html2tree(html)
            last_page = tree.xpath(last_page)[0]
        else:
            last_page = re.findall(last_page, html)[0]
        return int(last_page.split('=')[-1])

    def get_tender_urls(self, page, url_xp, prefix=''):
        """在页面中查找招标链接"""
        tree = self.url2tree(page)
        if tree is None:
            return
        urls = []
        for i in tree.xpath(url_xp):
            if prefix != '':
                i = i.split('/', 1)[-1]
            urls.append(prefix+i)
        return urls

    def save_text(self, urls):
        """将网页内容保存到mongodb中"""
        text_list = [
            {'url': url, 'text': self.url2text(url)}
            for url in urls
        ]
        self.col.insert_many(text_list)

# def filter_tender(url, keywords, checked_handler, result_handler):
#     """筛选招标公告,存入csv文件"""
#     resp = get(url)
#     h = html2text.HTML2Text()
#     h.ignore_links = True
#     h.ignore_images = True
#     text = h.handle(resp.text)
#     checked_handler.writerow([url])
#     # 多关键词过滤
#     for i in keywords:
#         flag = []
#         for j in i.split():
#             _flag = True if j in text else False
#             flag.append(_flag)
#         if all(flag) is True:
#             result_handler.writerow([url])
#             return url

def load_urls(filename):
    """从csv文件中加载数据并去重，返回set"""
    urls = set()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.add(row[0])
    return urls

def make_csv_handler(filename):
    """创建并返回csv句柄"""
    f_result = open(filename, 'a+', newline='')
    return csv.writer(f_result)

def make_driver(driver='phantomjs'):
    """只支持chrome和phantomjs"""
    if driver == 'phantomjs':
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        dcap["phantomjs.page.settings.loadImages"] = False
        d = webdriver.PhantomJS(desired_capabilities=dcap)
        return d
    # 创建chrome并配置
    ops = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    ops.add_experimental_option("prefs", prefs)
    ops.add_argument('--headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-gpu')
    ops.add_argument('--start-maximized')
    ops.add_argument('lang=zh_CN')
    ops.add_experimental_option('excludeSwitches', ['enable-automation'])
    ops.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"')
    try:
        d = webdriver.Chrome(options=ops)
    except:
        d = webdriver.Chrome(chrome_options=ops)
    return d

def random_sleep(max=5):
    """随机睡眠"""
    time.sleep(random.random()*max)