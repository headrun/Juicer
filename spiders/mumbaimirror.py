from juicer.utils import *

class Mumbaimirror(JuicerSpider):
    name = 'mumbaimirror'
    start_urls = ['http://www.mumbaimirror.com/mumbai/others']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//h4/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@style="float:right"]/a/@href'))
        yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="heading2"]/h1//text()'))
        text = textify(hdoc.select('//div[@class="Normal"]//text()'))
        date = textify(hdoc.select('//span[@class="byline"]//text()')).split('|')[-1].replace('.',':')
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//span[@id="authortext"]/text()'))
        if author == '':author = textify(hdoc.select('//span[@class="byline"]//text()')).split('|')[0]

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('date',xcode(date))
        item.set('dt_added',dt_added)
        item.set('author',xcode(author))
        item.set('text',xcode(text))

