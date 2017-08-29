from juicer.utils import *

class ServicemagicSpider(JuicerSpider):
    name = 'servicemagic_browse'
    allowed_domains = ['servicemagic.com']
    start_urls = 'http://www.servicemagic.com/c.html'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a/@href[contains(., "/emc")]',\
                                 '//div[@class="arial11"]//a[@class="hiCatNaked"]/@href',\
                                 '//td[@class="arial11"]//a[not(contains(@style, "padding"))][not(contains(text(), "Contractors"))]/@href',\
                                 '//b[contains(text(), "Next")]//parent::a[@class="otherLinks"]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//a[@class="otherLinks fn org"]/@href'], response)

        for url in terminal_urls: get_page('servicemagic_terminal', url)
