from juicer.utils import *

class WretchBrowseSpider(JuicerSpider):
    name = 'wretch_browse'
    allowed_domains = ['wretch.cc']
    start_urls = 'http://www.wretch.cc/user/peng1979'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        get_page('wretch_terminal', url)
