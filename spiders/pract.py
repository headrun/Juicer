from juicer.utils import*
from dateutil import parser

class PractBing(JuicerSpider):
    name = 'practbing'
    start_urls = ['http://www.bing.com/search?q=feed%3Atoyota+loc%3Asg&go=Search&qs=n&form=QBRE&pq=feed%3Atoyota+loc%3Asg&sc=8-18&sp=-1&sk=&cvid=744FBCB415F94A71942782EC14D2569C']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="b_content"]//a/@href').extract()
        for url in urls:
            next_page = textify(hdoc.select('//li[@class="b_pag"]//a/@href'))
            yield Request(urls,self.parse,response)

            print url
