from juicer.utils import*
from dateutil import parser

class Merdeka_ID(JuicerSpider):
    name ='merdeka_id'
    start_urls = ['https://www.merdeka.com/']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list=[301]

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="col-footer col-kategori"]/ul//li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li[@class="clearfix"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="mdk-body-newsimg-date"]/text()'))
            if 'Bulan yang lalu' not in date:
                date= date.replace('Sekitar ','')
                if 'Menit yang lalu' in date or 'Jam yang lalu' in date or 'Hari yang lalu' in date or 'Minggu yang lalu' in date or 'Bulan yang lalu' in date:
                    date = date.replace('Menit yang lalu','minutes ago').replace('Jam yang lalu','hours ago').replace('Hari yang lalu','day ago')
                    date = date.replace('Minggu yang lalu','weeks ago').replace('Bulan yang lalu','month ago')
                    import pdb;pdb.set_trace()
                    date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
                    if date_added < get_current_timestamp()-86400*30:
                        is_nxt = False
                        continue
                    link = textify(node.select('.//h3/a/@href'))
                    if '/foto/' in link:
                        continue
                    if 'http' not in link:  link = 'https://www.merdeka.com'+link
                    yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@class="link_next"]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'https://www.merdeka.com'+ nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="mdk-dt-headline"]/h1//text()'))
        text = textify(hdoc.select('//div[@class="mdk-body-paragpraph"]/p[not(a)]//text()'))
        if not text:
            text = textify(hdoc.select('//div[@class="mdk-body-paragpraph"]/p//text()'))
        date = textify(hdoc.select('//span[@class="date-post"]/text()'))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec'}
        for key, value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        date = ''.join(re.findall('\d+.*',date))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//span[@class="reporter"]/a/text()'))
        author_url = textify(hdoc.select('//span[@class="reporter"]/a/@href'))
        if 'http' not in author_url: author_url = 'https://www.merdeka.com'+ author_url

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
