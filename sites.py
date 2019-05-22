sites = [
    # {
    #     'decode': 'utf-8',
    #     'start_url': 'http://www.zycg.gov.cn/article/llist?catalog=StockAffiche',
    #     'page_f': 'http://www.zycg.gov.cn/article/llist?catalog=StockAffiche&page={}',
    #     'last_page_xp': '//ul[@class="lby-list"]//a[last()-1]/text()',
    #     'xp_page': True,
    #     'url_xp': '//ul[@class="lby-list"]//a[starts-with(@href, "/article/show")]/@href',
    #     'url_prefix': 'http://www.zycg.gov.cn/',
    # },
    # {
    #     'decode': 'utf-8',
    #     'start_url': 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2018%3A11%3A19&end_time=2019%3A05%3A20&timeType=5&displayZone=%E5%85%A8%E9%83%A8&zoneId=&pppStatus=0&agentName=',
    #     'page_f': 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2018%3A11%3A19&end_time=2019%3A05%3A20&timeType=5&displayZone=%E5%85%A8%E9%83%A8&zoneId=&pppStatus=0&agentName=',
    #     'last_page_xp': 'size: (\d.*?),',
    #     'xp_page': False,
    #     'url_xp': '//ul[@class="vT-srch-result-list-bid"]/li/a/@href',
    # },
    # {
    #     'decode': 'gbk',
    #     'start_url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_1.html',
    #     'page_f': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_{}.html',
    #     'url_xp': '//ul[@class="xinxi_ul"]/li/a/@href',
    #     'url_prefix': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/',
    #     'total_page': 1000
    # },
    # {
    #     'decode': 'gbk',
    #     'start_url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index_1.html',
    #     'page_f': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_{}.html',
    #     'url_xp': '//ul[@class="xinxi_ul"]/li/a/@href',
    #     'url_prefix': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/',
    #     'total_page': 1000
    # },
    # {
    #     'start_url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1',
    #     'last_page_xp': '//span[@class="countPage"]/b/text()',
    #     'post_url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
    #     'url_xp': '//ul[@class="dataList"]/li/a/@href',
    #     'url_prefix': 'http://www.ccgp-tianjin.gov.cn',
    #     'page_no_key': 'page',
    #     'data': {
    #         'method': 'view',
    #         'id': 1665,
    #         'step': 1,
    #         'view': 'Infor',
    #         'st': 1
    #     },
    # },
    # {
    #     'start_url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1664&ver=2',
    #     'last_page_xp': '//span[@class="countPage"]/b/text()',
    #     'post_url': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
    #     'url_xp': '//ul[@class="dataList"]/li/a/@href',
    #     'url_prefix': 'http://www.ccgp-tianjin.gov.cn',
    #     'page_no_key': 'page',
    #     'data': {
    #         'method': 'view',
    #         'id': 1664,
    #         'step': 1,
    #         'view': 'Infor',
    #         'st': 1
    #     },
    # },
    {
        'start_url': 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=1&ps=50',
        'page_f': 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi={}&ps=50',
        'last_page_xp': 'size: (\d.*?),',
        'xp_page': False,
        'url_xp': '//ul[@class="vT-srch-result-list-bid"]/li/a/@href',
        'divide_by': 50,
        'total_count_key': 'total',

    },
]