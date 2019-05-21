sites = [
    {
        'decode': 'utf-8',
        'start_url': 'http://www.zycg.gov.cn/article/llist?catalog=StockAffiche',
        'page_f': 'http://www.zycg.gov.cn/article/llist?catalog=StockAffiche&page={}',
        'last_page_xp': '//ul[@class="lby-list"]//a[last()-1]/text()',
        'xp_page': True,
        'url_xp': '//ul[@class="lby-list"]//a[starts-with(@href, "/article/show")]/@href',
        'url_prefix': 'http://www.zycg.gov.cn/',
    },
    {
        'decode': 'utf-8',
        'start_url': 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2018%3A11%3A19&end_time=2019%3A05%3A20&timeType=5&displayZone=%E5%85%A8%E9%83%A8&zoneId=&pppStatus=0&agentName=',
        'page_f': 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2018%3A11%3A19&end_time=2019%3A05%3A20&timeType=5&displayZone=%E5%85%A8%E9%83%A8&zoneId=&pppStatus=0&agentName=',
        'last_page_xp': 'size: (\d.*?),',
        'xp_page': False,
        'url_xp': '//ul[@class="vT-srch-result-list-bid"]/li/a/@href',
        'url_prefix': '',
    },
    {
        'decode': 'gbk',
        'start_url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_1.html',
        'page_f': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_{}.html',
        'url_xp': '//ul[@class="xinxi_ul"]/li/a/@href',
        'url_prefix': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/',
        'total_page': 1000
    },
]