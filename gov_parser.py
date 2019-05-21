from utils import Parser


class Bid:
    """招标类。传入一个网站的配置字典, 使用get_info获取其所有信息"""
    def __init__(self, **kwargs):
        self.decode = kwargs.get('decode', 'utf-8')
        self.start_url = kwargs['start_url']
        self.page_f = kwargs['page_f']
        self.last_page_xp = kwargs['last_page_xp']
        self.xp_page = kwargs.get('xp_page', True)
        self.url_xp = kwargs['url_xp']
        self.url_prefix = kwargs.get('url_prefix', '')
        self.total_page = kwargs.get('total_page')
        self.parser = Parser(decode=self.decode)

    def get_info(self):
        """获取该网站所有信息并存入数据库"""
        if self.total_page is None:
            self.total_page = self.parser.get_total_page(self.start_url, self.last_page_xp, self.xp_page)
        pages = [self.page_f.format(i) for i in range(1, self.total_page)]
        for page in pages:
            urls = self.parser.get_tender_urls(page, self.url_xp, self.url_prefix)
            self.parser.save_text(urls)