from juicer.utils import *
from dateutil import parser

class Seehua(JuicerSpider):
    name = 'seehua_my'
    start_urls = ['http://news.seehua.com/?cat=3','http://news.seehua.com/?cat=21','http://news.seehua.com/?cat=27','http://news.seehua.com/?cat=18','http://news.seehua.com/?cat=16','http://news.seehua.com/?cat=23','http://news.seehua.com/?cat=14','http://news.seehua.com/?cat=15','http://news.seehua.com/?cat=13','http://news.seehua.com/?cat=12','http://news.seehua.com/?cat=10','http://news.seehua.com/?cat=11','http://news.seehua.com/?cat=8']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        links = hdoc.select('//article[@class="item-list"]')
        for link in links:
            date = textify(link.select('./p[@class="post-meta"]/span[@class="tie-date"]/text()'))
            date = '-'.join(re.findall('\d+',date))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            news_link = textify(link.select('./h2/a/@href'))
            yield Request(news_link,self.details,response)

        next_pg = textify(hdoc.select('//span[@id="tie-next-page"]/a/@href'))
        if next_pg and is_next:
            yield Request(next_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="itemReviewed"]/span/text()'))
        text = textify(hdoc.select('//div[@class="entry"]/p//text()'))
        dt = textify(hdoc.select('//div[@class="post-inner"]//span[@class="tie-date"]/text()'))
        dt = '-'.join(re.findall('\d+',dt))
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))

