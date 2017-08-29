from juicer.utils import*
from dateutil import parser

class PractiseID(JuicerSpider):
    name = 'practise'
    start_urls =['http://www.jawapos.com/rss']

    def parse(self,response):   
        hdoc = HTML(response)   
        urls = hdoc.select('//h4/a[@target="_blank"]/@href').extract()
        for url in urls:
            if 'http' not in url: url = 'http://www.printweek.in'+ url
            print url
#            lnk = ''.join(re.findall("href='(.*)'",url))
        #links = hdoc.select('//div[@class="nodeControls"]/a/@href')
        #links = hdoc.select('//a[contains(@href, "feed")]').extract()
        #for link in links:
            #if 'http' not in link: link = 'http://economictimes.indiatimes.com' + link
            #print link


