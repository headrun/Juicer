from juicer.utils import *
from dateutil import parser

class Hz66(JuicerSpider):
    name = "hz66_china"
    start_urls = ['http://news.hz66.com/Category_18/Index.aspx','http://news.hz66.com/Category_75/Index.aspx','http://news.hz66.com/Category_74/Index.aspx','http://news.hz66.com/Category_227/Index.aspx','http://news.hz66.com/Category_24/Index.aspx','http://news.hz66.com/Category_25/Index.aspx','http://news.hz66.com/Category_26/Index.aspx','http://news.hz66.com/Category_27/Index.aspx','http://news.hz66.com/Category_28/Index.aspx','http://news.hz66.com/Category_29/Index.aspx','http://news.hz66.com/Category_21/Index.aspx','http://news.hz66.com/Category_56/Index.aspx','http://news.hz66.com/Category_76/Index.aspx','http://news.hz66.com/Category_49/Index.aspx','http://news.hz66.com/Category_50/Index.aspx','http://news.hz66.com/Category_51/Index.aspx','http://news.hz66.com/Category_53/Index.aspx','http://news.hz66.com/Category_54/Index.aspx','http://news.hz66.com/Category_52/Index.aspx','http://news.hz66.com/Category_57/Index.aspx','http://news.hz66.com/Category_55/Index.aspx']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//div[@id="list1"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//font[@class="title1"]//text()'))
        text = textify(hdoc.select('//div[@id="articleContnet"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@id="articleContnet"]//text()'))
        dt_added = textify(hdoc.select('//span[@class="s4"]//text()')[0])
        dt_added = dt_added.split(u'\uff1a')
        dt_added = dt_added[2]
        author = textify(hdoc.select('//td[@class="s4"]//span[@class="article_info"]//text()'))
        if not author:
            author = textify(hdoc.select('//div[@class="s2"]//text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author =' '.join(author)
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()

