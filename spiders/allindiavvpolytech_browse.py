
from juicer.utils import *

class AllIndiaVVPolyTechBrowseSpider(JuicerSpider):
    name = 'allindiavvpolytech_browse'
    allow_domain = 'allindia.vidyavision.com'
    start_urls = 'http://allindia.vidyavision.com/polytechniccolleges.asp'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = "http://allindia.vidyavision.com/polytechniccolleges.asp?page=%d"
        next_urls = [url % i for i in range(1, 24)]
        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//td[@align="center"]/a[@class="bluemediumlinks"]/@href', response)
        for terminal_url in terminal_urls:
            get_page('allindiavvpolytech_terminal', terminal_url)
