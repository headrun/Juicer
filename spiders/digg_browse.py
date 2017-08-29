from juicer.utils import *

class DiggBrowseSpider(JuicerSpider):
    name = 'digg_browse'
    allowed_domains = ['digg.com']
    start_urls = ['http://digg.com/talsiach']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        get_page('digg_terminal', url)
