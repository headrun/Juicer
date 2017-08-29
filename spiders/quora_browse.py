from juicer.utils import *

class QuoraSpider(JuicerSpider):
    name = 'quora_browse'
    allowed_domains = ['quora.com']
    start_urls = ['http://www.quora.com/Nathan-Mcdonald', 'http://www.quora.com/Matt-Schiavenza']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = get_request_url(response)
        get_page('quora_terminal', url)
