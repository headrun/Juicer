from juicer.utils import*
from dateutil import parser

class Practise(JuicerSpider):
    name = 'practise3'
    start_urls = ['http://www.theborneopost.com']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="menu"]//a/@href').extract()
        for categorie in categories:
            if 'http' not in categorie: categorie = 'http://www.theborneopost.com' + categorie
            yield Request(categorie,self.parse,response)

      # rss_link = textify(hdoc.select('//link[@rel="alternate"]/@href').extract()[-1])
        rss_link = textify(hdoc.select('//a[@class="ttip"]/@href'))
        f = open("rss_link_feed", "a")
        f.write(rss_link)
        f.write("\n")

        print rss_link

