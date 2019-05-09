import csv
import time
import requests
import html2text
from selenium import webdriver
from lxml.html import etree
from fake_useragent import UserAgent

ua = UserAgent()

# 关键词，使用
keywords = ['大学 招聘', '学校 招聘']

def make_csv_handler(filename):
    """创建并返回csv句柄"""
    f_result = open(filename, 'a+', newline='')
    return csv.writer(f_result)

result_filename = 'result.csv'
checked_filename = 'checked.csv'
urls_filename = 'urls.csv'

# 保存符合条件的url
result_handler = make_csv_handler(result_filename)
# 中间文件，保存已经检查过的招标url
checked_handler = make_csv_handler(checked_filename)
# 保存所有招标url
urls_handler = make_csv_handler(urls_filename)

# 陕西省政府采购网
url = 'http://www.ccgp-shaanxi.gov.cn/notice/list.do?noticetype=3&province=province'


def make_driver():
    """创建webdriver"""
    ops = webdriver.ChromeOptions()
    ops.add_argument('--headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-gpu')
    d = webdriver.Chrome(options=ops)
    d.maximize_window()
    return d

def parse_urls(d, page_no):    
    """获取某一页所有招标公告链接并存入csv文件"""
    d.execute_script("javascript:toPage('',{});".format(page_no))
    time.sleep(.5)
    link_xp = '//a[starts-with(@href, "http://www.ccgp-shaanxi.gov.cn:80/notice/noticeDetail.do?noticeguid=")]'
    links = d.find_elements_by_xpath(link_xp)
    for link in links:
        urls_handler.writerow([link.get_attribute('href')])

def get_all_tender_urls(start_page=1, end_page=300):
    """获取指定页之间的所有招标公告"""
    d = make_driver()
    d.get(url)
    for i in range(start_page, end_page):
        print('page', i)
        # 出错重新获取
        while 1:
            try:
                parse_urls(d, i)
                break
            except:
                d.get(url)
    d.quit()


"""
下面是使用requests直接post数据，
但是post不成功
"""
## 提交post请求的url
# url_post = 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3'
# def post(url, data):
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'Host': 'www.ccgp-shaanxi.gov.cn',
#         'Origin': 'http://www.ccgp-shaanxi.gov.cn',
#         'Referer': 'http://www.ccgp-shaanxi.gov.cn/notice/list.do?noticetype=3&province=province',
#         'X-Requested-With': 'XMLHttpRequest',
#         # 'User-Agent': str(ua.random),
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
#         # 'Cookie': '_gscu_614399700=57286768f4k55y92; _gscbrs_614399700=1; JSESSIONID=420982898024A1B32EB044C93BB19481; HasLoaded=true; _gscs_614399700=t57293354jocdj320|pv:17'
#     }
#     try:
#         resp = requests.post(url, json=data, headers=headers)
#         return resp
#     except:
#         return

# def resp2tree(resp):
#     if not resp:
#         return
#     return etree.HTML(resp.text)

# def parse_urls(page_no):
#     data = {
#         'page.pageNum': page_no,
#         "parameters['regionguid']": 610001,
#     }
#     resp = post(url, data)
#     time.sleep(1)
#     tree = resp2tree(resp)
#     return tree.xpath('//a[starts-with(@href, "http://www.ccgp-shaanxi.gov.cn:80/notice/noticeDetail.do?noticeguid=")]/@href')


def filter_tender(url):
    """筛选招标公告,存入csv文件"""
    resp = requests.get(url, headers={'User-Agent': str(ua.random)}, timeout=5)
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    text = h.handle(resp.text)
    checked_handler.writerow([url])
    # 多关键词过滤
    for i in keywords:
        flag = []
        for j in i.split():
            _flag = True if j in text else False
            flag.append(_flag)
        if all(flag) is True:
            result_handler.writerow([url])
            return url

def load_urls(filename):
    """从csv文件中加载数据并去重，返回set"""
    urls = set()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.add(row[0])
    return urls


def _save_legal_tender_urls():
    """存储所有期望的招标url"""
    urls = load_urls(urls_filename)
    passed_urls = load_urls(checked_filename)
    urls = urls - passed_urls
    len_urls = len(urls)
    for index, url in enumerate(urls):
        url = filter_tender(url)
        if url:
            print('{}/{} {}'.format(index, len_urls, url))
    return True

def save_legal_tender_urls():
    """请求达到速率 重新加载"""
    while 1:
        try:
            result = _save_legal_tender_urls()
            if result is True:
                break
        except:
            pass

def main():
    get_all_tender_urls()
    save_legal_tender_urls()

if __name__ == '__main__':
    main()