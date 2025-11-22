import random
from dataclasses import dataclass, asdict
from datetime import datetime
import time

import pandas as pd
from loguru import logger
from playwright.sync_api import sync_playwright


format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
            '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> ' \
            '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'
logger.add(
    sink="log",
    level="INFO",
    enqueue=True,
    rotation="1 weeks",
    retention=10,
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    compression="zip",
    format=format_
)


@dataclass
class Tender:
    region: str
    href: str
    text: str
    date: str = ''
    html: str = ''


class BaseCrawler:

    def __init__(self, region, max_page_num=None):
        self.region = region
        self.max_page_num = max_page_num
        self.tenders = {}

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
            self.save_tenders()

    def _crawl(self, context):
        ...

    def _crawl_history(self, context):
        ...

    def _execute_by_new_page(self, context, url, func, *args, **kwargs):
        with context.new_page() as page:
            page.goto(url, wait_until="domcontentloaded")
            return func(page, *args, **kwargs)

    @staticmethod
    def _random_sleep(_min=1, _max=60):
        sleep_seconds = random.uniform(_min, _max)
        time.sleep(sleep_seconds)

    def save_tenders(self):
        if not self.tenders:
            logger.info(f"[{self.region}]Nothing to save.")
            return
        data = [asdict(tender) for tender in self.tenders.values()]
        file_name = str(datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')
        file_name = f"{self.region}_{file_name}.xlsx"
        logger.info(f"Save tenders to {file_name}")
        pd.DataFrame(data).to_excel(file_name)


if __name__ == '__main__':
    a = Tender("1", "2", "3")
    print(asdict(a))