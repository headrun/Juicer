from juicer.utils import *

class BankbazaarForums(JuicerSpider):
    name = "bb_forum"
    start_urls = ['https://forums.bankbazaar.com']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//h2/a/@href').extract()
        for node in nodes:
            print node
