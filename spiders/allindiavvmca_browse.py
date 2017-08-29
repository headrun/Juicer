
from juicer.utils import *

class AllIndiaVVMcaBrowseSpider(JuicerSpider):
    name = 'allindiavvmca_browse'
    allow_domain = 'allindia.vidyavision.com'
    start_urls = 'http://allindia.vidyavision.com/mcacolleges.asp'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = "http://allindia.vidyavision.com/mcacolleges.asp?page=%d"
        next_urls = [url % i for i in range(1, 30)]
        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//td[@align="center"]/a[@class="bluemediumlinks"]/@href', response)
        for terminal_url in terminal_urls:
            get_page('allindiavvmca_terminal', terminal_url)
