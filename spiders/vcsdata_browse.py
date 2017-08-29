
from juicer.utils import *

class VcsDataBrowseSpider(JuicerSpider):
    name = 'vcsdata_browse'
    allow_domain = 'vcsdata.com'
    start_urls = ['http://www.vcsdata.com/software-services.html?category=IT-Software%20Services', 'http://www.vcsdata.com/fmcg.html?category=FMCG',\
                  'http://www.vcsdata.com/bpo-kpo.html?category=BPO%20/%20KPO', \
                  'http://www.vcsdata.com/realestate-construction.html?category=Construction%20/%20Real%20%20Estate',\
                  'http://www.vcsdata.com/pharmaceutical-companies.html?category=Pharmaceuticals/%20BioTech/%20Research']

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div[@id="pg"]//a[contains(text(),"Next")]/@href',response)
        for url in next_urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="result"]//a/@href', response)
        for url in terminal_urls:
            get_page('vcsdata_terminal', url)
