from juicer.utils import *
from dateutil import parser

class Jschina(JuicerSpider):
    name = "jschina_china"
    start_urls = ['http://news.jschina.com.cn/scroll/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="NewsList"]//td[@class="ww14"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="title"]//text()'))
        text = textify(hdoc.select('//div[@id="content"]//p/text()')[:-3])
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item =Item(response)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('url',response.url)
        yield item.process()


