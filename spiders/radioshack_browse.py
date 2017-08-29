from juicer.utils import *

class RadioshackSpider(JuicerSpider):
    name = 'radioshack_browse'
    allowed_domains = ['radioshack.com']
    start_urls = 'http://www.radioshack.com/home/index.jsp'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@id="mainNav"]//li[@class="col1"]//a/@href',\
                                 '//a[@class="catLink"]/@href',\
                                 '//div[@id="family-header"]//div[@class="pagination"]//img[@alt="Next Page"]//parent::a/@href'], response)

        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//h2[@class="productTitle"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('Id=')[-1].split('&filterName=')[0]
            get_page('radioshack_terminal', url, sk=sk)
