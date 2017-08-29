from juicer.utils import *

class QingBrowseSpider(JuicerSpider):
    name = 'qing_browse'
    allowed_domains = ['qing.weibo.com']
    start_urls = ['http://qing.weibo.com/discovery.html']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="img"]//a/@href'], response)
        for url in urls:
            get_page('qing_terminal', url)
