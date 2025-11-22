import time

from base_crawler import Tender, BaseCrawler, logger


class BeiJing(BaseCrawler):
    def __init__(self):
        super().__init__("beijing", max_page_num=148)
        self.page_url = "http://www.ccgp-beijing.gov.cn/xxgg/sjxxgg/A002004001index_{}.htm"
        self.tenders = {}

    def _crawl(self, context):
        self._crawl_one_page(context, self.page_url.format(1))

    def _crawl_history(self, context):
        for i in range(1, self.max_page_num):
            self._crawl_one_page(context, self.page_url.format(i))

    def _crawl_one_page(self, context, page_url):
        logger.info(f"start to crawl: {page_url}")
        self._execute_by_new_page(context, page_url, self.get_one_page_titles)
        for url, tender in self.tenders.items():
            with context.new_page() as page:
                tender.html = self.parse_detail(page, url)
                self.tenders[url] = tender
                self._random_sleep(_max=30)
        # 暂存临时文件
        self.save_tenders()

    def get_one_page_titles(self, page):
        li_elements = page.locator("li:has(a):has(span.datetime)").all()
        if not li_elements:
            logger.warning("No details found.")
            return
        # 4. 循环解析每个<li>的href、text、日期
        for li in li_elements:
            # 4.1 提取<a>标签的href和文本
            a_tag = li.locator("a")
            # 提取href（补全为完整URL，避免相对路径）
            href = a_tag.get_attribute("href")
            href_full = f"http:{href}" if href.startswith("//") else href
            # 提取<a>标签的文本（去除首尾空白）
            a_text = a_tag.inner_text()
            # 4.2 提取<span.datetime>的日期文本
            date_text = li.locator("span.datetime").inner_text()
            tender = Tender(self.region, href_full, a_text, date_text)
            logger.info(f"Found tender: {tender}")
            self.tenders[href_full] = tender

    @staticmethod
    def parse_detail(page, url):
        logger.info(f"start to parse detail: {url}")
        page.goto(url, wait_until="domcontentloaded")
        return page.locator(".mainTextBox").inner_html()


if __name__ == "__main__":
    BeiJing().run(increment=False)
