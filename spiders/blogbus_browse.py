from juicer.utils import *

class BlogbusSpider(JuicerSpider):
    name = 'blogbus_browse'
    allowed_domains = ['blogbus.com']
    start_urls = ['http://pindao.blogbus.com/fengshang/', 'http://pindao.blogbus.com/xingzhe/', 'http://pindao.blogbus.com/sejie/', 'http://pindao.blogbus.com/shenghuo/']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//span[@class="more"]//a/@href[contains(., "/tag/")]',\
                                 '//span[@class="pager"]//a[@class="next"]/@href'], response)

        for navigation_url in navigation_urls:
            get_page(self.name, navigation_url)

        terminal_urls = hdoc.select_urls(['//span[@class="headlines"]//a[contains(@href, "pindao.blogbus.com")]/@href'], response)

        for terminal_url in terminal_urls:
            get_page('blogbus_terminal', terminal_url)
