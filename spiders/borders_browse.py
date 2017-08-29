from juicer.utils import *

class BordersBrowseSpider(JuicerSpider):
    name = 'borders_browse'
    allowed_domains = ['borders.com']
    start_urls = ['http://www.borders.com']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="grandparent"]//li[@id="musicTab"]/preceding-sibling::li[@class="parent"]//a/@href',
                                 '//a[contains(text(),"next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        for url in  hdoc.select_urls('//img[@class="jtip prod-item"]//parent::a/@href', response):
            get_page('borders_terminal', url)
