from juicer.utils import*
from dateutil import parser

class Arcgames_USA(JuicerSpider):
    name = 'arcgames_forum'
    start_urls = ['http://www.arcgames.com/en/social/forum']

    def parse(self,response):
        hdoc = HTML(response)
        categories =  hdoc.select('//td[@class="category-name"]/h3/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_threads,response)

    def parse_threads(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
