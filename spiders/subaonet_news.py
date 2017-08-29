from juicer.utils import*
from dateutil import parser

class Subaonet_CN(JuicerSpider):
    name = 'subaonet_news'
    start_urls = ['http://www.subaonet.com/news/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[@class="wen"]/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//li[@style="margin-top:0px; margin-bottom:0px"]/a/@href').extract()
        for link in nodes:
            yield Request(link,self.parse_details,response)
        if not nodes:
            other_links = hdoc.select('//div[@class="Newslist_Title"]/a/@href').extract() or hdoc.select('//div[@class="title_bt"]/a/@href').extract() or hdoc.select('//span[@class="Navigation_02"]/a[@target="_blank"]/@href').extract()
            for link in other_links:
                yield Request(link,self.parse_links,response)

        nxt_pg = textify(hdoc.select('//div[@class="page mar-l-8"]//li/a[@class="next"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="bt"]//h1//text()'))
        date=textify(hdoc.select('//span[@class="date"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="article-content fontSizeSmall BSHARE_POP"]//p//text()'))
        auth = textify(hdoc.select('//span[@class="bqbj_r"]//text()'))
        author = auth.replace(u'\u8d23\u4efb\u7f16\u8f91\uff1a','').replace('[','').replace(']','')

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('author',{'name':xcode(author)}
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()


