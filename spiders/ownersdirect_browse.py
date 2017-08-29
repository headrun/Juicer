from juicer.utils import *

class OwnersdirectSpider(JuicerSpider):
    name = 'ownersdirect_browse'
    allowed_domains = ['ownersdirect.co.uk']
    start_urls = 'http://www.ownersdirect.co.uk/site-map.htm'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="LeftSitemap"]//ul[1]//li[not(contains(text(),"view site map for "))]//a/@href',\
                                 '//span[@class="regionbedlinks"]//a/@href',\
                                 '//div[@class="pageing"]//a[contains(text(),"Next")]/@href'], response)
        for url in urls: get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//p[@class="linkslisttitle"]//a/@href', response)
        for url in terminal_urls:
            sk = url.split('/')[-1].split('.htm')[0]
            get_page('ownersdirect_terminal', url, sk=sk)
