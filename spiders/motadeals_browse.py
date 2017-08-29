from juicer.utils import *

class MotaDealsBrowseSpider(JuicerSpider):
    name = 'motadeals_browse'
    allow_domain = ['motadeals.com']
    start_urls = ['http://www.motadeals.com/','http://www.motadeals.com/ahmedabad.html','http://www.motadeals.com/chandigarh.html','http://www.motadeals.com/delhi/ncr.html',\
                  'http://www.motadeals.com/hyderabad.html','http://www.motadeals.com/kolkata.html','http://www.motadeals.com/mumbai.html','http://www.motadeals.com/pune.html',\
                  'http://www.motadeals.com/bengaluru.html','http://www.motadeals.com/chennai.html','http://www.motadeals.com/goa.html','http://www.motadeals.com/jaipur.html',\
                  'http://www.motadeals.com/lucknow.html','http://www.motadeals.com/others.html' ]

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)


        urls = hdoc.select_urls(['//ul[@class="sublist"]//a/@href','//li//a[contains(text(), "Past Deals")]/@href'],response)
        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls(['//div[@class="pItemContent"]//h3//a/@href', '//div[@class="dItemContent"]//h3//a/@href'], response)
        for url in terminal_urls:
            get_page('motadeals_terminal', url)

