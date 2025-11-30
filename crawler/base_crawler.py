import random
from dataclasses import dataclass, asdict
from datetime import datetime
import time

import pandas as pd
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

from utils.log import logger
from utils.es import ESConnection


@dataclass
class Tender:
    region: str
    href: str
    title: str
    release_date: str = ''
    html: str = ''
    crawl_date: str = ''


class BaseCrawler:

    def __init__(self, region, max_page_num=None):
        self.region = region
        self.max_page_num = max_page_num
        self.tenders = {}
        self.exists_urls = set()
        self.es_conn = ESConnection()

    def run(self, increment=True):
        self.exists_urls = self.get_exists_url_from_es()
        try:
            with Stealth().use_sync(sync_playwright()) as p:
                # 创建真正的浏览器实例，使用全局初始化脚本
                browser = p.chromium.launch(
                    headless=False,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-blink-features=AutomationControlled',
                        '--start-maximized'
                    ]
                )
                context = browser.new_context()
                if increment:
                    self._crawl(context)
                else:
                    self._crawl_history(context)
        finally:
            ...
            self.save_tenders_to_es()
            self.save_tenders_to_excel()

    def _crawl(self, context):
        ...

    def _crawl_history(self, context):
        ...

    def _get_crawl_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _execute_by_new_page(self, context, url, func, *args, **kwargs):
        with context.new_page() as page:
            logger.info(f"[{self.region}]start to goto: {url}")
            page.goto(url, wait_until="domcontentloaded")
            return func(page, *args, **kwargs)

    @staticmethod
    def _random_sleep(_min=1, _max=60):
        sleep_seconds = random.uniform(_min, _max)
        time.sleep(sleep_seconds)

    def save_tenders_to_excel(self):
        if not self.tenders:
            logger.info(f"[{self.region}]Nothing to save.")
            return
        data = [asdict(tender) for tender in self.tenders.values()]
        file_name = str(datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')
        file_name = f"{self.region}_{file_name}.xlsx"
        logger.info(f"[{self.region}]Save tenders to {file_name}")
        pd.DataFrame(data).to_excel(file_name)

    def save_tender_to_es(self, tender):
        logger.info(f"[{self.region}]Save {tender.title} tenders to Elasticsearch.")
        self.es_conn.save_tender(tender)

    def save_tenders_to_es(self):
        if not self.tenders:
            logger.info(f"[{self.region}]Nothing to save.")
            return
        logger.info(f"[{self.region}]Save {len(self.tenders)} tenders to Elasticsearch.")
        self.es_conn.save_tenders_bulk(self.tenders.values())

    def get_exists_url_from_es(self):
        query_body = {
            "query": {
                "term": {
                    "region": self.region
                }
            },
            "sort": [
                {
                    "release_date": {
                        "order": "desc"  # 按 release_date 降序排列
                    }
                }
            ],
            "_source": False,  # 只返回 href 字段，减少数据传输
            "size": 10000  # 调整返回结果数量，根据你的数据量设置
        }
        data = self.es_conn.search_data(query_body) or set()
        return set(i['_id'] for i in data)


if __name__ == '__main__':
    a = Tender("1", "2", "3")
    print(asdict(a))