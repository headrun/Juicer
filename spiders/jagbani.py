from juicer.utils import*

class JagbaniIN(JuicerSpider):
    name = 'jagbani'
    start_urls = ['http://jagbani.punjabkesari.in/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="cntr-menu"]//a/@href').extract()
        for category in categories:
            yield Request(category, self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//span[@class="story"]')
        for node in nodes:
            date =  str(textify(node.select('.//div[@class="time"]/text()')))
            date = date.replace(':AM', 'AM').replace(':PM', 'PM')
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./h2/a/@href'))
            yield Request(link, self.parse_finaldata,response)

        nxt_pg = textify(hdoc.select('//div[@class="kjpage"]/a[@class="page-numbers current"]/following-sibling::a[1]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://jagbani.punjabkesari.in' + nxt_pg
            yield Request(nxt_pg, self.parse_links,response)

    def parse_finaldata(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="ttlls"]//text()'))
        text = textify(hdoc.select('//div[@class="desc"]/article//text()'))
        date = textify(hdoc.select('//div[@class="time2"]/text()'))
        date = date.replace(':AM', 'AM').replace(':PM', 'PM').replace('-', ' ')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

        item = Item(response)
        item.set('url', response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added',dt_added)
