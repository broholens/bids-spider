from utils import *

keyword = '招聘'
driver = make_driver()

def tsinghua(url='http://hq.tsinghua.edu.cn/front/frontAction.do?ms=gotoSecond&lmid=12457'):
    driver.get(url)
    search_el = driver.find_element_by_id('keyword')
    search_el.send_keys(keyword)
    search_el.send_keys(Keys.ENTER)
    random_sleep(2)
    for link in driver.find_elements_by_xpath('//dl//a'):
        print(link.get_attribute('href'))

tsinghua()