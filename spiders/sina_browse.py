from juicer.utils import *

class SinaSpider(JuicerSpider):
    name = 'sina_browse'
    allowed_domains = ['sina.com.cn']
    start_urls = 'http://blog.sina.com.cn/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//p[@class="t2 clearfix fwit"]//a/@href',\
                                 '//span//a/@href[contains(., "/index.shtml")]',\
                                 '//span[contains(@class, "more")]//a/@href',\
                                 '//ul[contains(@class, "list_")]//following-sibling::table//div[@class="pagebox"]/span[@class="pagebox_next"][1]//a/@href'], response)

        for navigation_url in navigation_urls:
            get_page(self.name, navigation_url)

        terminal_urls = hdoc.select_urls(['//a/@href[contains(., "/s/blog_")]'], response)

        for terminal_url in terminal_urls:
            get_page('sina_terminal', terminal_url)
