from juicer.utils import*
from dateutil import parser

class Tuoitrenews_VN(JuicerSpider):
    name = 'tuoitrenews_vn'
    start_urls = ['http://tuoitrenews.vn/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@id="nav"]//li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//dl[@class="lst-news"]/dd')
        for node in nodes:
            date = textify(node.select('.//span//text()'))
            date = date.replace('Published: ','').replace('Published:','')
            date_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a/@href'))
            yield Request(link,self.parse_details,response)
        if not nodes:
            lin = hdoc.select('//dl[@class="block-banner"]//dd/a/@href').extract()
            yield Request(lin,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pager"]//li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://tuoitrenews.vn' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//p[@class="title-type-1"]//text()'))
        text = textify(hdoc.select('//div[@class="content-inner"]//p//text()'))
        text = text.replace('Like us on Facebook or follow us on Twitter to get the latest news about Vietnam!','')
        dt = textify(hdoc.select('//p[@class="txt-type-1"][last()]//text()'))
        date = dt.replace('Updated :','').replace('GMT + 7','')
        dt_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
        author = textify(hdoc.select('//p[@class="txt-type-1"][1]//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
        #yield item.process()

        


