import time
import random
import requests
from lxml.html import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

REQUEST_TIMEOUT = 5

def get(url, **kwargs):
    """requests get封装"""
    try:
        return requests.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
    except:
        return

def post(url, data, **kwargs):
    """requests post封装"""
    try:
        return requests.post(url, json=data, timeout=REQUEST_TIMEOUT, **kwargs)
    except:
        return

def html2tree(html):
    """html转为etree"""
    try:
        return etree.HTML(html)
    except:
        return

def resp2x(resp, json=False):
    """response返回类型"""
    try:
        return resp.text if json is False else resp.json()
    except:
        return

def url2tree(url, **kwargs):
    """请求url到转化为etree的全部过程封装"""
    resp = get(url, **kwargs)
    html = resp2x(resp)
    return html2tree(html)

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