import re
from utils import *

keywords = ['招聘']
driver = make_driver()
urls = set()
urls_cleaned = set()


def tsinghua(url='http://hq.tsinghua.edu.cn/front/frontAction.do?ms=gotoSecond&lmid=12457'):
    ptn = re.compile('\'(\d.*?)\',\'(\d.*?)\'')
    driver.get(url)
    search_el = driver.find_element_by_id('keyword')
    for kw in keywords:
        search_el.send_keys(kw)
        search_el.send_keys(Keys.ENTER)
        random_sleep(2)
        for link in driver.find_elements_by_xpath('//dl//a'):
            xxid, lmid = ptn.findall(link.get_attribute('href'))[0]
            url = 'http://hq.tsinghua.edu.cn/front/frontAction.do?ms=gotoThird&lmid={}&xxid={}'.format(lmid, xxid)
            urls_cleaned.add(url)


def nwupl(url='http://gzc.nwupl.edu.cn/plus/list.php?tid=8'):
    tree = url2tree(url)
    if not tree:
        return
    last_page = tree.xpath('//ul[@class="pagelist"]//a/@href')[-1]
    last_page = 'http://gzc.nwupl.edu.cn' + last_page
    page_count = int(last_page.split('=')[-1])
    page_prefix = last_page.rstrip(str(page_count))
    for i in range(1, page_count+1):
        page_url = page_prefix + str(i)
        tree = url2tree(page_url)
        for link in tree.xpath('//ul/li/h2/a/@href'):
            urls.add('http://gzc.nwupl.edu.cn' + link)