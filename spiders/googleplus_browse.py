from juicer.utils import *

class GooglePlusSpider(JuicerSpider):
    name = 'googleplus_browse'
    allowed_domains = ['https://plus.google.com/']
    start_urls = ['https://plus.google.com/100000772955143706751/posts']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        print ">>>>>>>>>>>>>>>>>>>", url
        get_page('googleplus_terminal', url)
