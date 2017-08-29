from juicer.utils import *
from dateutil import parser

class Newssc(JuicerSpider):
    name = "newssc_china"
    start_urls = ['http://scnews.newssc.org/2009bwyc/','http://scnews.newssc.org/2009mlsh/','http://scnews.newssc.org/2009cdxw/','http://scnews.newssc.org/2009szxw/','http://world.newssc.org/gj/','http://world.newssc.org/shxw/','http://china.newssc.org/zxbd/','http://china.newssc.org/shxw/','http://finance.newssc.org/gdxw/index.shtml','http://sports.newssc.org/yw/','http://schouse.newssc.org/wybg/index.shtml','http://schouse.newssc.org/jrkp/index.shtml','http://schouse.newssc.org/ttxw/index.shtml','http://local.newssc.org/szxq/index.shtml','http://health.newssc.org/jkrd/index.shtml','http://sp.newssc.org/yw/index.shtml','http://fz.newssc.org/shyf/index.shtml','http://fz.newssc.org/jjyf/index.shtml','http://fz.newssc.org/fzzt/index.shtml','http://fz.newssc.org/djsf/index.shtml','http://fz.newssc.org/gssw/index.shtml','http://fz.newssc.org/xzzf/index.shtml']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//a[contains(@href, "newssc.org/system/")]//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td[contains(@class,"title_")]//text()'))
        if not title:
            title = textify(hdoc.select('//div[@id="main_left_title"]//text()'))
        if not title:
            title = textify(hdoc.select('//h1//text()'))
        text = textify(hdoc.select('//td[@class="content14"]//p//text()'))
        if not text:
            text = textify(hdoc.select('//td[@class="black_h"]//p//text()'))
        if not text:
            text =textify(hdoc.select('//section//p//text()'))
        if not text:
            text = textify(hdoc.select('//div[@id="news_content"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@id="pubtime_baidu"]//text()'))
        author = textify(hdoc.select('//span[@id="editor_baidu"]//text()'))
        if not author:
            author = textify(hdoc.select('//td[@class="content14"]/text()'))
        if not author:
            author = textify(hdoc.select('//td[@align="right"]/text()'))
        author = author.split(u'\uff1a')
        author.pop(0)
        author = ''.join(author)
        if ']' in author:
            author = author.split(']')
            author = author[0]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode( author))
        item.set('url', response.url)
        yield item.process()
