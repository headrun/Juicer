from juicer.utils import*
from dateutil import parser

class Bingfeeds(JuicerSpider):
    name = 'bing_feeds'
    start_urls = ['http://www.bing.com/search?q=feed%3akulkas+loc%3aid&go=Search&qs=n&pq=feed%3akulkas+loc%3aid&sc=8-18&sp=-1&sk=&cvid=D9DF2863A8FD4C31BE9CDD85448B0026&first=31&FORM=PERE2']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ol[@id="b_results"]/li/h2/a/@href').extract()
        for url in urls:
            print url
