import time

from crawler.base_crawler import BaseCrawler, Tender
from utils.log import logger


class HeBei(BaseCrawler):
    def __init__(self):
        super().__init__('hebei')
        self.index_url = 'https://szj.hebei.gov.cn/hbggfwpt/jydt/salesPlat.html'
        self.headers = {}

    def _crawl(self, context):
        page = context.new_page()
        page.goto("https://szj.hebei.gov.cn/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(1)
        page.goto(self.index_url, wait_until="domcontentloaded", timeout=5000)
        page.wait_for_selector("ul#content", timeout=30000)
        page.locator('a:text-is("政府采购")').click()
        time.sleep(.5)
        results = page.evaluate('''() => {
                        // 获取所有符合条件的li元素
                        const items = document.querySelectorAll('#content li');
                        const data = [];

                        items.forEach(item => {
                            // 提取a标签的href和title
                            const link = item.querySelector('a');
                            const href = link ? link.href : null;
                            const title = link ? link.title : null;

                            // 提取span.r的文本
                            const span = item.querySelector('span.r');
                            const releaseDate = span ? span.textContent.trim() : null;

                            if (href || title || releaseDate) {
                                data.push({ href, title, releaseDate });
                            }
                        });

                        return data;
                    }''')
        logger.info(f"get {len(results)} items")
        for result in results:
            page.goto(result['href'], wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("div.ewb-copy", timeout=10000)
            html = page.locator("div.ewb-copy").inner_html()
            tender = Tender(self.region, result['href'], result['title'], result['releaseDate'], html, self._get_crawl_date())
            self.save_tender_to_es(tender)
            self._random_sleep(_max=30)



if __name__ == '__main__':
    HeBei().run()

