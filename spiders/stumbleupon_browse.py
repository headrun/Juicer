from juicer.utils import *

class StumbleuponBrowseSpider(JuicerSpider):
    name = 'stumbleupon_browse'
    allowed_domains = ['stumbleupon.com']
    start_urls = ['http://www.stumbleupon.com/stumbler/geoff', 'http://www.stumbleupon.com/stumbler/skyblue101']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        print ">>>>>>>>>>>>>>>>>>>", url
        get_page('stumbleupon_terminal', url)
