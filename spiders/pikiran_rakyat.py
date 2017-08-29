from juicer.utils import*
from dateutil import parser

class Pikiran_ID(JuicerSpider):
    name = 'pikiran_rakyat'
    start_urls = ['http://www.pikiran-rakyat.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[contains(@class, "leaf")]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.pikiran-rakyat.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="entry-main"]') or hdoc.select('//div[@class="col col-lg-6"]')
        for node in nodes:
            date = textify(node.select('./div[@class="entry-meta"]/span/span/text()')) or textify(node.select('./div[span[@class="glyphicon glyphicon-time"]]/text()'))
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h2/a/@href')) or textify(node.select('.//h4/a/@href'))
            if 'http' not in link: link = 'http://www.pikiran-rakyat.com' + link
            yield Request(link,self.parse_details,response)

        nxt_pg =  textify(hdoc.select('//ul[@class="pagination"]/li[@class="next"]/a[@title="Go to next page"]/@href')) or textify(hdoc.select('//ul[@class="pagination"]/li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.pikiran-rakyat.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="page-header"]//text()'))
        text = textify(hdoc.select('//div[@class="content"]//div[@class="field-item even"]//text()'))
        if not text:
            text = textify(hdoc.select('//span//following-sibling::div//div[@class="field-item even"]//text()'))
        date = textify(hdoc.select('//div[@class="col-sm-9"]/div[span[@property="dc:date dc:created"]]//text()'))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@class="items-penulis"]/span/a/text()'))
        author_url = textify(hdoc.select('//div[@class="items-penulis"]/span/a/@href'))
        if 'http' not in author_url: author_url = 'http://www.pikiran-rakyat.com' + author_url
        if author:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('author', {'name':xcode(author)})
            item.set('author_url',xcode(author_url))
            item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
            yield item.process()
        else:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
            yield item.process()
