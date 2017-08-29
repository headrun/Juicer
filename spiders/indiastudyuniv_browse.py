
from juicer.utils import *

class IndiaStudyUnivBrowseSpider(JuicerSpider):
    name = 'indiastudyuniv_browse'
    allow_domain = 'http://www.indiastudychannel.com/'
    start_urls = 'http://www.indiastudychannel.com/universities/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = "http://www.indiastudychannel.com/universities/Index.aspx?PageNumber=%d"
        next_urls = [url % i for i in range(1, 12)]
        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//table[@cellpadding="7"]//td[@align="left"]/a/@href', response)
        for terminal_url in terminal_urls:
            get_page('indiastudyuniv_terminal', terminal_url)

