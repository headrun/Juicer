from juicer.utils import *
from dateutil import parser

class Shangdu(JuicerSpider):
    name = "shangdu_china"
    start_urls = ['http://news.shangdu.com/301/','http://news.shangdu.com/201/','http://news.shangdu.com/401/','http://news.shangdu.com/sports/','http://news.shangdu.com/junshi/','http://news.shangdu.com/beijing/','http://news.shangdu.com/101/','http://news.shangdu.com/584/','http://news.shangdu.com/shenghuo/','http://news.shangdu.com/weather/','http://news.shangdu.com/668/','http://news.shangdu.com/10010/','http://news.shangdu.com/media/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="contentList"]//ul//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="newsColumnHeader"]//h1//text()'))
        text = textify(hdoc.select('//span[@itemprop="articleBody"]//text()'))
        dt_added = textify(hdoc.select('//span[@itemprop="datePublished"]//text()'))
        author = textify(hdoc.select('//div[@class="editor"]//text()'))
        if '|'in author:
            (a,author,b) = author.split(':')
            (author,extra_data) = author.split('|')
        else:
            author = author.split(u'\uff1a')
            author.pop(0)
            author = ''.join(author)
            if ']' in author:
                (author,extra_data) = author.split(']')
            author = author.strip()
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

