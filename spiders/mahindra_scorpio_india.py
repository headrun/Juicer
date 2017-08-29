from juicer.utils import *
from dateutil import parser
class MahindraScorpioIndia(JuicerSpider):
    name = 'mahindra_scorpio_india'
    start_urls = ['http://www.mahindrascorpio.com/mahindra-scorpio-news-reviews.aspx']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="reviews_ariticle_container clearfix"]//ul[@class="clearfix"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="st_header"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="storybody"]/p/text()')[1:])
        date_author = textify(hdoc.select('//div[@class="storybody"]/p[@class="st_dateline"]/text()'))
        #dt_added = textify(hdoc.select(''))
        #author = textify(hdoc.select())
        #dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE::::",xcode(title)
        print "TEXT:::::",xcode(text)
       # print "DATE:::",xcode(dt_added)
        print date_author
        print "URL::",response.url
        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        #item.set('dt_added', dt_added)
        #yield item.process()


