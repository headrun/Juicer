from juicer.utils import*
from dateutil import parser

class ChinaCom(JuicerSpider):
    name = "china_com"
    start_urls = ['http://news.china.com.cn/live/index.html']
    def parse(self,response):
        hdoc = HTML(response)
        url = 'http://sports.china.com.cn/live/2014-11/21/content_29958166.htm'
        #urls = hdoc.select_urls('//div[@id="content"]//td//ul//li//a//@href',response)
        #for url in urls:
        yield Request(url,self.parse_terminal,response)

    def parse_terminal(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        if not title:
            title = textify(hdoc.select('//td[@class="fb24"]//text()'))
        text=textify(hdoc.select('//div[@id="artbody"]/p/text()'))
        if not text:
            text = textify(hdoc.select('//td[@class="f14_000000"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//td//p/text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        (extra_data,dt_added,time) = dt_added.split(' ')
        dt_added = dt_added + " " + time
        author = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        if ' ' in author:
            author_info = []
            author_info = author.split(' ')
            author_info.pop(0)
            author = ' '.join(author_info)
            author = author.strip()
        else:
            author = ""

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        #yield item.process()
