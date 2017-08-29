from juicer.utils import *
from dateutil import parser

class Fawan(JuicerSpider):
    name = "fawan_china"
    start_urls = ['http://www.fawan.com/Article/gj/','http://www.fawan.com/Article/jrtt/','http://www.fawan.com/Article/yw/','http://www.fawan.com/Article/ztbd/','http://www.fawan.com/Article/bs/','http://www.fawan.com/Article/jj/','http://www.fawan.com/Article/fz/','http://www.fawan.com/Article/sq/','http://www.fawan.com/Article/rx/','http://www.fawan.com/Article/gn/','http://www.fawan.com/Article/zhxx/','http://www.fawan.com/Article/ty/','http://www.fawan.com/Article/yl/','http://www.fawan.com/Article/fzfk/','http://www.fawan.com/Article/xwc/','http://www.fawan.com/Article/jkxwc/','http://www.fawan.com/Article/jszk/','http://www.fawan.com/Article/bjjj/','http://www.fawan.com/Article/sddcbd/','http://www.fawan.com/Article/youthszk/','http://www.fawan.com/Article/fw3czk/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="article_list mtop10"]//ul//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//div[@id="articleContnet"]//p//text()')[1:])
        author = textify(hdoc.select('//div[@class="article_info"]//text()')[1])

        dt_added = textify(hdoc.select('//div[@class="article_info"]//text()')[4])
        if not dt_added:
            dt_added = textify(hdoc.select('//div[@class="article_info"]//text()')[4])
        dt_added = dt_added.split(u'\uff1a')
        dt_added.pop(0)
        dt_added = ' '.join(dt_added)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

