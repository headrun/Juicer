from juicer.utils import *
from dateutil import parser
class IndiasNews(JuicerSpider):
    name = "indias_news"
    start_urls = ['http://www.indiasnews.net/']
    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//article//h3//a//@href')
        for url in urls:
            yield Request(url, self.parse_details, response)
    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="article_text"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="article_text"]/p/text()'))
        text2= textify(hdoc.select('//div[@class="article_text"]//h2//text()'))
        text= text2 + text
        dt_added = textify(hdoc.select('//div[@class="article_text"]//p[@class="meta"]//span//text()'))
        #date format is "05-05-2014" and day is the first then we have to
        #pass dayfirst=True to parse_date function
        #parse_date('05-07-2014') - Wrong
        #datetime.datetime(2014, 5, 7,0,0)
        #parse_date('05-07-2014', dayfirst=True) - Correct
        #datetime.datetime(2014, 7, 5, 0, 0)
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "TITLE===========",xcode(title)
        print "TEXT============",xcode(text)
        print "DATE============",dt_added
        print "URL=============",response.url

        item = Item(response)
        item.set('title', title)
        item.set('text',text)
        item.set('dt_added', dt_added)
        # item.set('author.name', author)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])
        # yield item.process() 

