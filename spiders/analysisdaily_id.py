from juicer.utils import*
from dateutil import parser

class Analysisdaily(JuicerSpider):
    name = 'analysisdaily'
    start_urls = ['http://news.analisadaily.com/','http://sepakbola.analisadaily.com/','http://sport.analisadaily.com/','http://tekno.analisadaily.com/','http://entertainment.analisadaily.com/','http://lifestyle.analisadaily.com/','http://ragam.analisadaily.com/']

    def parse(self,parse):
        hdoc = HTML(response)
        links = textify(hdoc.select('//div[@id="titles"]//a/@href'))
        for link in links:
            yield Request(links,self.parse_details,response)
        next_page = textify(hdoc.select('//a[@rel="next"]/@href'))
        if next_page:
            next_p = next_page[0]
            yield Request(next_p,self.parse_details,response)

        
    def parse_details(self,parse):
        hdoc = HTML(response):
        title = textify(hdoc.select('//div[@class="article yoyo col col-md-8 col-sm-7"]/h3/text()'))
        text = textify(hdoc.select())

