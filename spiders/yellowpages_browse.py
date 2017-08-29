from juicer.utils import *

class YellowPagesSpider(JuicerSpider):
    name = 'yellowpages_browse'
    allowed_domains = ['yellowpages.com']
    start_urls = 'http://www.yellowpages.com/sitemap'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//li[@class="state"]//h3//a/@href',\
                                '//ul[@class="cities-list"]//li//a/@href',\
                                '//ul[@class="categories-list"]//li//a/@href',\
                                '//a[contains(text(),"Next")]/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@id="results"]//div[@id]//h3//a/@href'], response)
        for url in terminal_urls:
            get_page('yellowpages_terminal', url)
