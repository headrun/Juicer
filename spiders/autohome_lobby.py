from juicer.utils import *
from dateutil import parser


class  AutoHomeLobby(JuicerSpider):
    name = "autohome_lobby"
    start_urls = ['http://chejiahao.autohome.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="qing-card"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="card-title-name"]//span//text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('.//div[@class="card-tags"]/a[@target="_blank"]/@href'))
            if 'http' not in link: link = 'http://chejiahao.autohome.com.cn' + link
            yield Request(link,self.parse_details,response)
        ext_links = hdoc.select('//div[@class="focusimg-pic"]//li/a/@href').extract()
        for lin in ext_links:
            if 'http' not in lin: lin = 'http:' + lin
            yield Request(lin,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="bigpage"]//a[@class="text-page-next"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://chejiahao.autohome.com.cn' + nxt_pg
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="article-title"]/h3//text()'))
        date = textify(hdoc.select('//div[@class="prompt-time"]//span//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text=textify(hdoc.select('//div[@class="article-content example"]//p//text()')) or textify(hdoc.select('//div[@id="video-des"]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()

