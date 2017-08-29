from juicer.utils import*
from dateutil import parser

class Baophuyen_VN(JuicerSpider):
    name = 'baophuyen_vn'
    start_urls = ['http://www.baophuyen.com.vn/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@l="0"]/preceding-sibling::a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.baophuyen.com.vn' + cat
            yield Request(cat,self.parse_links,response)
        cates = ['http://www.baophuyen.com.vn/160/goc-tre.html', 'http://www.baophuyen.com.vn/92/quoc-te.html','http://www.baophuyen.com.vn/89/phong-su-ky-su.html']
        for cate in cates:
            yield Request(cate,self.parse_links,response)


    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="title"]')
        for node in nodes:
            date = textify(node.select('.//div[@class="date"]//text()'))
            date = ''.join(re.findall('\d+.*',date))
            date=''.join(re.findall('\d{2}/\d{2}/\d{4}', date))
            date=datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%B %d %Y')
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//a/@href'))
            if 'http' not in link: link = 'http://www.baophuyen.com.vn' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagination"]/ul//a[contains(.,">")]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.baophuyen.com.vn' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="newsDetail"]/div[@class="title"]//text()'))
        text= textify(hdoc.select('//div[@class="text"]//p//text()'))
        date=textify(hdoc.select('//div[@class="newsDetail"]/div[@class="date"]//text()'))
        date = ''.join(re.findall('\d+.*',date))
        date=''.join(re.findall('\d{2}/\d{2}/\d{4}', date))
        date=datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%B %d %Y')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
       

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
        yield item.process()



