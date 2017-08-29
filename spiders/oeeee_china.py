from juicer.utils import *
from dateutil import parser

class Oeeee(JuicerSpider):
    name = 'oeeee_china'
    start_urls = ['http://news.nandu.com/media/index.html','http://news.nandu.com/politics/index.html','http://news.nandu.com/world/index.html','http://news.nandu.com/society/index.html','http://news.nandu.com/depth/index.html','http://news.nandu.com/culture/index.html','http://ent.nandu.com/index.html','http://sports.nandu.com/index.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="main"]//div[@class="roll_news"]//h3//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@class="content BSHARE_POP"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        if not dt_added:
            dt_added = textify(hdoc.select('//div[@class="info"]//div[@class="fl"]/text()'))
        author = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        author = self.extract_author(author)
        if not author:
            author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
            author = self.extract_author(author)
        if not author:
            author = textify(hdoc.select('//div[@class="clearfix tag"]//div[@class="fl"]//text()'))
            author = author.split(u'\u4f5c\u8005\uff1a')
            author.pop(0)
            author = ''.join(author)
            author = self.extract_author(author)
            if not author:
                author = textify(hdoc.select('//div[@class="clearfix tag"]//div[@class="fr"]//text()'))
                author = self.extract_author(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))
        print '\n'
        print response.url
        print xcode(title)
        print xcode(author)
        print dt_added
        print xcode(text)


        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()

    def extract_author(self,author):
        self.author = author.split(u'\uff1a')
        self.author.pop(0)
        author = ''.join(self.author)
        return author
