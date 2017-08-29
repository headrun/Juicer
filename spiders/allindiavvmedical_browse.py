
from juicer.utils import *

class AllIndiaVVMedicalBrowseSpider(JuicerSpider):
    name = 'allindiavvmedical_browse'
    allow_domain = 'allindia.vidyavision.com'
    start_urls = 'http://allindia.vidyavision.com/medicalcolleges.asp'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        url = "http://allindia.vidyavision.com/medicalcolleges.asp?page=%d"
        next_urls = [url % i for i in range(1, 34)]
        for next_url in next_urls:
            get_page(self.name, next_url)

        terminal_urls = hdoc.select_urls('//td[@align="center"]/a[@class="bluemediumlinks"]/@href', response)
        for terminal_url in terminal_urls:
            get_page('allindiavvmedical_terminal', terminal_url)

