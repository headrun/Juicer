from juicer.utils import *

class TencentBrowseSpider(JuicerSpider):
    name = 'tencent_browse'
    allowed_domains = ['t.qq.com']
    start_urls = ['http://t.qq.com/p/t/57735126031653']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[@class="pageBtn"][contains(text(), "Next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="userName"]//strong//a/@href[not(contains(., "/certification"))][not(contains(., "jump.t"))]'], response)
        for url in terminal_urls:
            get_page('tencent_terminal', url)
