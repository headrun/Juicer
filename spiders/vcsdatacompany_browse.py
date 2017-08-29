
from juicer.utils import *

class VcsDataCompanyBrowseSpider(JuicerSpider):
    name = 'vcsdatacompany_browse'
    allow_domain = 'www.vcsdata.com'
    start_urls = ['http://www.vcsdata.com/pharmaceutical-companies.html?category=Pharmaceuticals/%20BioTech/%20Research',\
                  'http://www.vcsdata.com/fmcg.html?category=FMCG','http://www.vcsdata.com/callcentres.html?category=Call%20Centres',\
                  'http://www.vcsdata.com/engineering.html?category=Engineering','http://www.vcsdata.com/financialservices.html?category=Financial%20Services', \
                  'http://www.vcsdata.com/chemicals.html?category=Chemical',\
                  'http://www.vcsdata.com/consultants.html?category=Placement%20/%20HR%20/%20Training%20Consultants',\
                  'http://www.vcsdata.com/logistics.html?category=Courier/%20Logistics/%20Packaging/%20Transportation', \
                  'http://www.vcsdata.com/bpo-kpo.html?category=BPO%20/%20KPO', 'http://www.vcsdata.com/banking.html?category=Banks',\
                  'http://www.vcsdata.com/export-import.html?category=Export%20Houses', 'http://www.vcsdata.com/insurance.html?category=Insurance', \
                  'http://www.vcsdata.com/electrical.html?category=Electrical/Electronics', 'http://www.vcsdata.com/automobiles.html?category=Automobiles',\
                  'http://www.vcsdata.com/software-services.html?category=IT-Software%20Services', \
                  'http://www.vcsdata.com/advertising.html?category=Advertising/Event%20Mgmt/%20PR/MR',\
                  'http://www.vcsdata.com/hospitals.html?category=Hospitals/Healthcare', \
                  'http://www.vcsdata.com/law-legalconsultants.html?category=Law%20/%20Legal%20Consultants',\
                  'http://www.vcsdata.com/accounting-taxation.html?category=Accounting/Consulting/%20Taxation',\
                  'http://www.vcsdata.com/power-energy.html?category=Power/Energy', \
                  'http://www.vcsdata.com/telecommunication.html?category=Telecommunication/%20Mobile', \
                  'http://www.vcsdata.com/managementconsultants.html?category=Management%20/Engineering%20/Environ.%20Consultants', \
                  'http://www.vcsdata.com/engineering-institute.html?category=Institutes%20-%20Engineering', \
                  'http://www.vcsdata.com/management-institutes.html?category=Institutes%20-%20Management',\
                  'http://www.vcsdata.com/realestate.html?category=Construction%20/%20Real%20%20Estate', \
                  'http://www.vcsdata.com/foodprocessing.html?category=Food%20Processing/%20Beverages' ]

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        next_urls = hdoc.select_urls('//div[@id="pg"]//a[contains(text(),"Next")]/@href',response)
        for url in next_urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="result"]//a/@href', response)
        for url in terminal_urls:
            get_page('vcsdatacompany_terminal', url)
