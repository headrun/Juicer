from juicer.utils import *

class EsomarBrowseSpider(JuicerSpider):
    name = 'esomar_browse'
    allowed_domains = ['http://directory.esomar.org/']
    start_urls = 'http://directory.esomar.org/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[contains(text(), "View all countries")]/@href',\
                                 '//div[@class="allcountries"]//td//a/@href'], response)

        for url in urls: get_page(self.name, url)

        next_url = textify(hdoc.select_urls('//a[@title="Go to next page"]/@href', response))
        next_url = next_url.split(' ')[0]
        get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//div[@class="directorylistitem"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-1].split('_')[0]
            get_page('esomar_terminal', url, sk=sk)
