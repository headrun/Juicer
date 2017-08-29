from juicer.utils import *

class TripadvisorSpider(JuicerSpider):
    name = 'tripadvisor_browse'
    allowed_domains = ['tripadvisor.com']
    start_urls = 'http://www.tripadvisor.com/pages/site_map_lodging.html'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//td[@colspan="5"]//h3//a/@href',\
                                 '//ul[@class="geoList"]//li//a/@href',\
                                 '//div[@class="pgLinks"]//a[@class="guiArw sprite-pageNext "]/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="quality wrap"]//a[@class="property_title"]/@href', response)
        for url in terminal_urls:
            sk = url.split('-d')[-1].split('-')[0]
            get_page('tripadvisor_terminal', url, sk=sk)
