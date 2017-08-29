from juicer.utils import*
from dateutil import parser

class Gatra_ID(JuicerSpider):
    name = 'gatra_id'
    start_urls = ['http://www.gatra.com/', 'http://www.gatra.com/carsplus-home']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "level")]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.gatra.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="catItemView groupSecondary"]') or hdoc.select('//div[@class="catItemView groupPrimary"]')
        for node in nodes:
            date = textify(node.select('.//dd[@class="create"]//text()')) or textify(node.select('.//span[@class="catItemDateCreated"]/text()'))
            date_added =  get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h3/a/@href')) or textify(node.select('.//h3/a/@href'))
            if 'http' not in link: link = 'http://www.gatra.com' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]/li/a[@title="Next"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.gatra.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h2[@class="itemTitle"]//text()'))  
        text = textify(hdoc.select('//div[contains(@class, "Text")]//p//text()')) or textify(hdoc.select('//div[contains(@class, "Text")]//div//text()'))

        junk_links =  textify(hdoc.select('//div[contains(@class, "Text")]//p//a/text()'))
        text = text.replace(junk_links,'')
        date = textify(hdoc.select('//span[@class="itemDateCreated"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//p[contains(text(), "ditor:")]/text()')) or textify(hdoc.select('//p/strong[contains(text(), "ditor:")]/text()')) or textify(hdoc.select('//p/span[contains(text(), "ditor:")]/text()')) or textify(hdoc.select('//p//span[contains(text(), "ditor:")]/text()')) or textify(hdoc.select('//hr/following-sibling::p//text()')) or textify(hdoc.select('//strong[contains(text(), "ditor:")]//text()')) or textify(hdoc.select('//div[@class="itemFullText"]//br[last()]/following-sibling::text()'))
        if not author:
            author = textify(hdoc.select('//div//p/strong//text()[2]')) or textify(hdoc.select('//div//strong//text()[2]'))
        main_author = author.replace('Editor:','').replace('editor:','')

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(main_author)})
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
