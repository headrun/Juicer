from juicer.utils import *
from dateutil import parser

class Sumbarprov(JuicerSpider):
    name = 'sumbarprov'
    start_urls = ['http://sumbarprov.go.id/web/full']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//ul[@class="dropdown-menu"]/li/a/@href').extract()
        for link in links:
            yield Request(link,self.parse_news_links,response)

    def parse_news_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="post"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="post-timestamp"]//text()'))
            if 'jam yang lalu' in date or 'hari yang lalu' in date or 'bulan yang lalu' in date or 'menit yang lalu'  in date or 'minggu yang lalu' in date:
                date = date.replace('jam yang lalu','hours ago').replace('hari yang lalu',' day ago').replace('bulan yang lalu','month ago').replace('menit yang lalu' ,'minutes ago').replace('minggu yang lalu','weeks ago')
                date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
                for key,value in date_dict.iteritems():
                    if key in date: date = date.replace(key,value)
                date = date.partition('|')[0]
                if 'month ago' in date:
                    continue
                dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
                if dt_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                newslink = textify(node.select('./h3/a/@href'))
                yield Request(newslink,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination pagination-large"]//li/a[@rel="next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_news_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="col-md-8"]//h3[not(i)]/text()'))
        text = textify(hdoc.select('//div[@style="overflow-x:auto;"]//p//text() | //div[@style="overflow-x:auto;"]//ol//text()'))
        date = textify(hdoc.select('//i[@class="fa fa-calendar"]/following-sibling::text()'))
        date = ''.join(re.findall('(.*) \|',date))
        date = date.replace('Posted on','')
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        auth = textify(hdoc.select('//i[@class="fa fa-user"]/following-sibling::a//text()'))
        junk = textify(hdoc.select('//i[@class="fa fa-tags"]/following-sibling::a//text()'))
        author = auth.replace(junk,'')
        
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',dt_added)
        item.set('author', {'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
