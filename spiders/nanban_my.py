from juicer.utils import*
from dateutil import parser

class Nanban_MY(JuicerSpider):
    name = 'nanban_my'
    start_urls = ['http://www.nanban2u.com.my/index.php']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="menu navigation"]//li/a/@href').extract()
        for cat in categories:
            if 'http' not in cat:   cat = 'http://www.nanban2u.com.my/' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

