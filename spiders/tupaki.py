from juicer.utils import*
from dateutil import parser

class Tuapki(JuicerSpider):
    name = 'tupaki'
    start_urls = ['http://english.tupaki.com','http://www.tupaki.com']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="more"]//a/@href | //li//a[contains(@href, "moviereviews")]/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = response.url + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//li[@class="clearfix"]/a/@href').extract() or hdoc.select('//div[@class="col col1"]//li/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)     

        nxt_pg = textify(hdoc.select('//ul[@class="paginate pag2 clearfix"]//a[contains(text(), "Next")]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="movrevhead col col1"]//h1[@title]//text()')) or textify(hdoc.select('//div[@class="movrevhead col col1"]//h1//text()'))
        date=textify(hdoc.select('//p[@class="metatilt"]//text()'))
        date=date.replace('GMT+0530 (IST)','')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        text = textify(hdoc.select('//div[contains(@class, "descpt ")]//p//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield item.process()
