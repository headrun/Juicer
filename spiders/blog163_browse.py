from juicer.utils import *

class Blog163Spider(JuicerSpider):
    name = 'blog163_browse'
    allowed_domains = ['163.com']
    start_urls = 'http://blog.163.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//ul[@class="nav-list"]//li//a/@href',\
                                 '//div[@class="hd"]//a/@href',\
                                 '//li[@class="next"]//a/@href',\
                                 '//a[@class="pg-txt"]/@href'], response)

        for navigation_url in navigation_urls:
            print "navigation_url>>>>>>>>>>>>>>>", navigation_url
            get_page(self.name, navigation_url)

        terminal_urls = hdoc.select_urls(['//a/@href[contains(., "/blog/static/")]'], response)

        for terminal_url in terminal_urls:
            print "terminal_url<>>>>>>>>>>>>>>>>>", terminal_url
            get_page('blog163_terminal', terminal_url)
