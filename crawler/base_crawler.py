import random
from dataclasses import dataclass, asdict
from datetime import datetime
import time

import pandas as pd
from playwright.sync_api import sync_playwright

from utils.log import logger
from utils.es import ESConnection


@dataclass
class Tender:
    region: str
    href: str
    text: str
    release_date: str = ''
    html: str = ''
    crawl_date: str = ''


class BaseCrawler:

    def __init__(self, region, max_page_num=None):
        self.region = region
        self.max_page_num = max_page_num
        self.tenders = {}
        self.es_conn = ESConnection()

    def run(self, increment=True):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False, args=['--start-maximized'])
                context = browser.new_context(no_viewport=True)
                if increment:
                    self._crawl(context)
                else:
                    self._crawl_history(context)
        finally:
            self.save_tenders_to_excel()

    def _crawl(self, context):
        ...

    def _crawl_history(self, context):
        ...

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
    
    def save_tenders_to_es(self):
        if not self.tenders:
            logger.info(f"[{self.region}]Nothing to save.")
            return
        logger.info(f"[{self.region}]Save {len(self.tenders)} tenders to Elasticsearch.")
        self.es_conn.save_tenders_bulk(self.tenders.values())


if __name__ == '__main__':
    a = Tender("1", "2", "3")
    print(asdict(a))