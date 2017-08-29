from juicer.utils import *

class TimesdealBrowseSpider(JuicerSpider):
    name = 'timesdeal_browse'
    allowed_domains = ['timesdeal.com']
    start_urls = 'http://timesdeal.com/bangalore-deals'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//ul[@class="rightlinks"]//a[not(contains(@href, "/all-india-deals"))]/@href',\
                                 '//nav[@class="topmenuLnks"]//a/@href'], response)

        for url in urls:
            print "browse_url>>>>>>>>>>>>>>>>>", url
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="blk215"]//a[contains(text(), "View this Deal")]/@href',\
                                          '//div[@class="splDeal"]//a[contains(text(), "View this Deal")]/@href',\
                                          '//section[@class="seldeal "]//a[not(contains(@href, "javascript"))]/@href',\
                                          '//section[@class="seldeal nobrd"]//a[not(contains(@href, "javascript"))]/@href'], response)

        for url in terminal_urls:
            print "terminal_url>>>>>>>>>>>>>>", url
            get_page('timesdeal_terminal', url)
