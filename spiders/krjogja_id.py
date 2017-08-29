from juicer.utils import*
from dateutil import parser

class Krjogja_ID(JuicerSpider):
    name = 'krjogja_id'
    start_urls = ['http://krjogja.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[@class="drop"]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://krjogja.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="news-post article-post"]//div[@class="post-content"] | //div[@class="widget posts-widget"]//div[@class="post-content"] | //div[@class="inner-hover"]')
        for node in nodes:
            date = textify(node.select('./ul//following-sibling::li[i[@class="fa fa-clock-o"]]/text() | ./ul/li[i[@class="fa fa-clock-o"]]/text()'))
            date = ''.join(re.findall('\d+.*',date))
            if 'jam lalu' in date or 'hari lalu' in date or 'tahun lalu' in date or 'minggu lalu' in date or 'bulan lalu' in date or 'menit lalu' in date:
                date = date.replace('jam lalu','hours ago').replace('hari lalu','day ago').replace('tahun lalu','year ago').replace('minggulalu','week ago').replace('bulan lalu','month ago').replace('menit lalu','minutes ago')
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h2/a/@href')) 
            if 'http' not in link: link = 'http://krjogja.com' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination-list"]/li[@class="next"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://krjogja.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="title-post"]/h1//text()'))
        text = textify(hdoc.select('//div[@class="post-content"]//p//text()'))
        date = textify(hdoc.select('//div[@class="title-post"]/ul//text()'))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@class="title-post"]/ul//li/a/text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
