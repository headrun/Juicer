from juicer.utils import *

class NextagtravelSpider(JuicerSpider):
    name = 'nextagtravel_browse'
    allowed_domains = ['travel.nextag.com']
    start_urls = 'http://travel.nextag.com/Hotels-2703100/hotels-html'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="browse-container"]//ul//li//h3//a/@href',\
                                 '//td[@class="parent"]//h3//a/@href',\
                                 '//li[@class="smallmargin"]//h3//a/@href',\
                                 '//ul[@class="browseUL"]//li//h3//a/@href',\
                                 '//span[@id="next"]//a/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="sr-name-c"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-2].split('-')[-1]
            get_page('nextagtravel_terminal', url, sk=sk)
