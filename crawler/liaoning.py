import time
from datetime import datetime

from pandas.core.config_init import data_manager_doc

from crawler.base_crawler import BaseCrawler, Tender
from utils.log import logger


class LiaoNing(BaseCrawler):
    def __init__(self):
        super().__init__('liaoning')
        self.url = 'http://www.ccgp-liaoning.gov.cn/portalindex?currentKey=pubAnnounce'
        self.headers = {}

    def _parse_cookie(self, cookies):
        for cookie in cookies:
            self.headers['cookie'] = cookie['name'] + '=' + cookie['value']

    def _crawl(self, context):
        page = context.new_page()
        def handle_request(request):
            headers = request.headers
            if 'fn' in headers:
                self.headers['fn'] = headers['fn']
        page.on("request", handle_request)
        resp = page.goto(self.url, wait_until="domcontentloaded")
        self.headers.update(resp.headers)
        self.headers.update({
            'content-type': 'application/json;charset=UTF-8',
            'access-control-allow-origin': '*/*',
            'isloading': 'true',
        })
        self._parse_cookie(page.context.cookies())
        # today = str(datetime.today().date())
        today = '2025-12-01'
        records = self._get_tenders_list(context, today)
        for record in records:
            logger.info(f"start crawling tender {record}")
            # TODO: resp1.body()乱码 charset=gb2312
            resp1 = page.goto(record[1], wait_until="domcontentloaded")
            print(1)

    def _get_tenders_list(self, context, date_str):
        logger.info(f"start to get tenders list for {date_str}.")
        response = context.request.post(
            url="http://www.ccgp-liaoning.gov.cn/gateway/complaint_core/homePage/getHomePunInfoList",
            data={
              "title": "",
              "planNo": "",
              "district": "[]",
              "releaseDateStart": date_str,
              "releaseDateEnd": date_str,
              "infoTypeCode": "1001",  # 采购公告
              "current": 1,
              "rowCount": 100
            },
            headers=self.headers
        )
        data = response.json()
        if data.get("code") != 200:
            logger.error(f"get data failed:{data}")
            return []
        if data.get("data", {}).get('total') == 0:
            logger.warning(f"total count is 0: {data}")
            return []
        records = []
        for record in data['data']['data']:
            title = record['title']
            release_date = record['releaseDate']
            href = record['infoPath']
            if not href.startswith('http'):
                href = 'http://218.60.151.59:9004/' + href
            records.append((self.region, href, title, release_date))
        logger.info(f"get tenders list for {date_str} success: {records}.")
        return records


if __name__ == '__main__':
    LiaoNing().run()