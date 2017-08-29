from juicer.utils import*
from dateutil import parser

class Prokal_ID(JuicerSpider):
    name = 'prokal_id'
    start_urls = ['http://www.prokal.co/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@align="center"]/span/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes=  hdoc.select('//div[@class="media"]')
        for node in nodes:
            date = textify(node.select('.//small/text()'))
            if 'jam lalu' in date or 'hari lalu' in date or 'tahun lalu' in date or 'minggu lalu' in date or 'bulan lalu' in date:
                date = date.replace('jam lalu','hours ago').replace('hari lalu','day ago').replace('tahun lalu','year ago').replace('minggu lalu','week ago').replace('bulan lalu','month ago')
            date = date.strip('-')
            dt = date.strip('\r\t\n')
            date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./div[@class="media-left"]/a/@href'))
            yield Request(link,self.parse_details,response)
            add_link = textify(node.select('.//h3/a/@href'))
            yield Request(add_link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//li[@class="next page"]/a[i[@class="fa fa-angle-right"]]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@style]/small/following-sibling::div[contains(@style, "font-family")]/text()'))
        add_txt = textify(hdoc.select('//h3/text()'))
        text = textify(hdoc.select('//div[@id="bodytext"]//text()'))
        text_final = add_txt  + ' ' + text
        dt = textify(hdoc.select('//div[@style]/div[@style]/preceding-sibling::small/text()'))
        date = ''.join(re.findall('\d+.*',dt))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text_final))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
