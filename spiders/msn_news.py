from juicer.utils import *
from dateutil import parser

class MsnNews(JuicerSpider):
    name = "msn_news"
    start_urls = ['http://www.msn.com/en-in']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        categories = hdoc.select('//div[@id="topnav"]//li/a[contains(@href,"/en-in/")]/@href').extract()
        for sub_category in categories[:2]:
            if 'http' not in sub_category: sub_category = 'http://www.msn.com' + sub_category
            yield Request(sub_category,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[contains(@class, "normalsection")]/h2/a/@href').extract() or hdoc.select('//div[contains(@class, "normalsection")]//li/a/@href').extract() or hdoc.select('//div[@id="topnav"]//li/a/@href').extract()
        for link in links:
            if 'http' not in link: link = 'http://www.msn.com' + link
            yield Request(link,self.parse_data,response)

    def parse_data(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul/li/a[contains(@href,"/en-in/news/")]/@href').extract()
        for url in urls:
            if 'http' not in url: url = 'http://www.msn.com' + url
            yield Request(url,self.parse_details,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//p//text()'))
        text = text.replace('CRNCY VOD 532792', ' ')
#       author = textify(hdoc.select('//span[@class="authorname-txt"]//text()')) or textify(hdoc.select('//span[@class="auth"]//text()'))
        date = textify(hdoc.select('//span[@class="time"]/text()')) or textify(hdoc.select('//time/text()'))
        if not text:
            text = textify(hdoc.select('//section[@class="articlebody"]//p/text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="field-item even"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="richtext"]//text()'))
        if not text:
            text = textify(hdoc.select('//span/p/text()'))
        dt_added = get_timestamp(parse_date(xcode(date))) 
        #dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=10))


        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
       #print 'author', xcode(author)
        print 'dt_added', xcode(dt_added)

'''        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()'''

