from juicer.utils import *
from dateutil import parser

class Iqilu(JuicerSpider):
    name = "iqilu_china"
    start_urls = ['http://www.iqilu.com/html/scroll/']#['http://news.iqilu.com/china/','http://news.iqilu.com/guoji/','http://news.iqilu.com/shehui/','http://news.iqilu.com/xinwenzongheng/','http://news.iqilu.com/shandong/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        urls = hdoc.select('//div[@id="nr_left"]//ul//li')
        for url in urls[:2]:
            date = textify(url.select('./span[last()]/text()'))
            if date:date = '2015' + date
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added <  get_current_timestamp()-86400*5:
                is_next = False
                continue
            url1 = textify(url.select('.//a[@title]/@href'))
            #yield Request(url1,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="f14list"]/following-sibling::div/a[last()]/@href'))
        if nxt_pg and is_next:
            import pdb;pdb.set_trace()
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        import pdb;pdb.set_trace()
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@id="context"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="big_title"]//h3//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        author  = textify(hdoc.select('//span[@id="author_baidu"]//text()'))
        if ":" in author:
            (extra_data,author) = author.split(':')
        if u'\uff1a' in author:
            author = author.split(u'\uff1a')
            author.pop(0)
            author = ' '.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        print xcode(title)
        print dt_added
        print xcode(author)

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        #yield item.process()


