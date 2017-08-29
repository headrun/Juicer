import re
from juicer.utils import *

class DealsandyouBrowseSpider(JuicerSpider):
    name = 'dealsandyou_browse'
    allowed_domains = ['dealsandyou.com']
    start_urls = 'http://www.dealsandyou.com/sitemap2'

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@class="siteMap-part"]//ul/li/a/@href[contains(., "/showDeals/")]',\
                                 '//div[@class="view-cat"]//a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_url = hdoc.select_urls(['//div[@class="picturedeals"]/a[1]/@href'], response)

        for url in terminal_url: get_page('dealsandyou_terminal', url)
