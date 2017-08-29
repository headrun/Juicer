from juicer.utils import *

class IdenticaBrowseSpider(JuicerSpider):
    name = 'identica_browse'
    allowed_domains = ['http://identi.ca']
    start_urls = ['http://identi.ca/nj3ma']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        print ">>>>>>>>>>>>>>>>>>>", url
        get_page('identica_terminal', url)
