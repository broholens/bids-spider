import json

from crawler.base_crawler import BaseCrawler, Tender
from utils.log import logger


class TianJin(BaseCrawler):
    def __init__(self):
        super().__init__('tianjin')
        self.authorization = None
        self.headers = None

    def _get_tender_details(self, context, tender_id):
        logger.info(f"start to request tender details for {tender_id}")
        response = context.request.post(
            url="https://www.tjggzy.cn/api/api/portal/Announcement/GetDetail",
            data={"Id": tender_id},
            headers=self.headers
        )
        data = response.json()
        if data.get("statusCode") != 2000:
            logger.error(f"get tender details error:{data}")
            return
        tender = Tender(region=self.region, href=tender_id, title=data['responseData']['announcementName'],
                        release_date=data['responseData']['publishTime'], html=data['responseData']['noticeContent'],
                        crawl_date=self._get_crawl_date())
        self.save_tender_to_es(tender)
        self.tenders[tender_id] = tender
        logger.info(f"get tender details for {tender_id} success")


    def _get_page_dictionary(self, context):
        logger.info(f"start to get page dictionary for 行业类型.")
        response = context.request.post(
            url="https://www.tjggzy.cn/api/api/v1/Dictionary/PageDictionaryItem",
            # 行业类型：政府采购/房屋市政...
            data={"state": 1, "pageIndex": 1, "pageSize": 9999, "dictionaryTypeCode": "w10.hylx"},
            headers=self.headers
        )
        data = response.json()
        if data.get("statusCode") != 2000:
            logger.error(f"get page dictionary error:{data}")
            return {}
        # 政府采购 4 [{\"typeCode\":\"w10.xxlx\",\"value\":[\"13\",\"14\",\"15\",\"16\",\"17\",\"18\",\"19\"]},{\"typeCode\":\"w10.gggslx\",\"value\":[\"3\",\"10\",\"16\",\"22\"]},{\"typeCode\":\"w10.xzqh\",\"value\":[\"120100\",\"120116\",\"120101\",\"120102\",\"120103\",\"120104\",\"120105\",\"120106\",\"120110\",\"120111\",\"120112\",\"120113\",\"120114\",\"120115\",\"120117\",\"120118\",\"120119\"]}]
        records = {}
        for record in data['responseData']['records']:
            xxlx = []
            for i in json.loads(record['customAttribute']):
                if i['typeCode'] == 'w10.gggslx':
                    xxlx = i['value']
            records[record['itemValue']] = xxlx
        logger.info(f"get page dictionary for 行业类型 success: {records}.")
        return records
        # response = context.request.post(
        #     url="https://www.tjggzy.cn/api/api/v1/Dictionary/PageDictionaryItem",
        #     # 信息类型：评标结果公示/定标结果公示...
        #     data={"state": 1, "pageIndex": 1, "pageSize": 9999, "dictionaryTypeCode": "w10.gggslx"},
        #     headers=self.headers
        # )
        # data = response.json()
        # if data.get("statusCode") != 2000:
        #     logger.error(f"get page dictionary error:{data}")
        #     return
        # records = {
        #     # 评标结果公示 8
        #     record['itemValue']: record['itemText']
        #     for record in data['responseData']['records']
        # }

    def _get_tender_list(self, context, hylx, xxlx):
        """传入行业类型与信息类型"""
        logger.info(f"start to get tender list for {hylx}, {xxlx}.")
        response = context.request.post(
            url="https://www.tjggzy.cn/api/api/portal/Announcement/Page",
            # 行业类型：政府采购/房屋市政...
            data={
              "PageIndex": 1,
              "PageSize": 50,
              "State": 2,
              "tenderProjectCode": "",
              "bidSectionCode": "",
              "announcementName": "",
              "announcementCode": "",
              "orderByFieldType": 1,
              "orderByType": 0,
              "recordCode": "",
              "industryType": [hylx],
              "announcementType": xxlx,
              "infoType": "",
              "districtCode": "",
              "publishTimeType": -1
            },
            headers=self.headers
        )
        data = response.json()
        if data.get("statusCode") != 2000:
            logger.error(f"get tender list error:{data}")
            return set()
        records = set([
            record['announcementId']
            for record in data['responseData']['records']
        ])
        logger.info(f"get tender list success: {records}.")
        return records

    def _crawl(self, context):
        page = context.new_page()
        def handle_request(request):
            headers = request.headers
            if 'authorization' in headers:
                self.authorization = headers['authorization']
        page.on("request", handle_request)
        page.goto("https://www.tjggzy.cn/announcementIndex")
        page.wait_for_load_state("networkidle")

        # 再次尝试获取authorization
        if not self.authorization:
            try:
                auth_storage = page.evaluate("() => localStorage.getItem('authorization')")
                if auth_storage:
                    self.authorization = auth_storage
            except:
                pass
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://www.tjggzy.cn/announcementIndex",
            "Authorization": self.authorization,  # 关键：带上提取的authorization
            "User-Agent": page.evaluate("navigator.userAgent")
        }
        pages = self._get_page_dictionary(context)
        for hylx, xxlxs in pages.items():
            for xxlx in xxlxs:
                tender_list = self._get_tender_list(context, hylx, xxlx)
                for tender_id in tender_list:
                    if tender_id in self.exists_urls:
                        continue
                    self._get_tender_details(context, tender_id)
                    self._random_sleep(_max=30)

if __name__ == "__main__":
    TianJin().run()
