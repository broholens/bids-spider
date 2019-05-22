from utils import Parser


class Bid:
    """招标类。传入一个网站的配置字典, 使用get_info获取其所有信息"""
    def __init__(self, **kwargs):
        self.decode = kwargs.get('decode', 'utf-8')
        self.start_url = kwargs['start_url']
        self.page_f = kwargs.get('page_f')
        self.last_page_xp = kwargs.get('last_page_xp')
        self.xp_page = kwargs.get('xp_page', True)
        self.url_xp = kwargs['url_xp']
        self.url_prefix = kwargs.get('url_prefix', '')
        self.total_page = kwargs.get('total_page')
        self.data = kwargs.get('data')
        self.page_no_key = kwargs.get('page_no_key')
        self.post_url = kwargs.get('post_url')
        self.divide_by = kwargs.get('divide_by')
        self.total_count_key = kwargs.get('total_count_key')
        self.parser = Parser(decode=self.decode)

    def get_info(self):
        """获取该网站所有信息并存入数据库"""
        if self.total_page is None:
            self.total_page = self.parser.get_total_page(self.start_url, self.last_page_xp, self.xp_page)
        if self.data is None:
            self.get_urls()
        else:
            self.post_data()

    def get_urls(self):
        """get方法获取每一页信息"""
        pages = [self.page_f.format(i) for i in range(1, self.total_page)]
        for page in pages:
            print(page)
            urls = self.parser.get_bid_urls(page, self.url_xp, self.url_prefix)
            self.parser.save_text(urls)

    def post_data(self):
        """post方法获取每一页信息"""
        for i in range(1, self.total_page+1):
            print(self.post_url, i)
            self.data.update({self.page_no_key: i})
            urls = self.parser.get_bid_urls(self.post_url, self.url_xp, self.url_prefix, True, self.data)
            self.parser.save_text(urls)