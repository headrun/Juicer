from juicer.utils import *

class GnaviSpider(JuicerSpider):
    name = 'gnavi_browse'
    allowed_domains = ['http://rds.gnavi.co.jp/']
    start_urls = 'http://www.gnavi.co.jp/en/sitemap/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//dl[@id="locationList"]//a/@href',\
                                 '//li[@class="next"]//a/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//dt[@class="jp"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('.jp/')[-1].split('/')[0]
            get_page('gnavi_terminal', url, sk=sk)
