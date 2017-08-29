from juicer.utils import *

class PlaxoBrowseSpider(JuicerSpider):
    name = 'plaxo_browse'
    allowed_domains = ['plaxo.com']
    start_urls = 'http://www.plaxo.com/directory/'

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select_urls(['//div[@class="letterLinks"]//a/@href',\
                                 '//ul//li//h3//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//p[@class="name"]//a/@href'], response)
        for url in terminal_urls:
            sk = url
            get_page('plaxo_terminal', url)
