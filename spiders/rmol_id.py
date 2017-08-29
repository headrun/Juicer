from juicer.utils import*
from dateutil import parser

class Rmol_ID(JuicerSpider):
    name = 'rmol_id'
    start_urls  = ['http://rmol.co/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav"]/li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[contains(@class, "post-item post-sticky")]')
        if not nodes:
            nodes = hdoc.select('//div[contains(@class, "post-item")]')
        for node in nodes:
            date = textify(node.select('.//div//span[i[@class="fa fa-clock-o"]]/text()'))
            date = ''.join(re.findall(',(.*?),',date)).strip()
            date_dict = {'Januari':'Jan','JANUARI':'Jan','FEBRUARI':'Feb','Februari':'Feb', 'MAC':'March','Mac':'March','Juli':'July','JULI':'July','Maret':'March','MARET':'March', 'Mei':'May','MEI':'May','JULAI':'July', 'Julai':'July', ' Ogos':'Aug','OGOS':'Aug', 'Oktober':'Oct', 'OKTOBER':'October','DISEMBER':'Dec','Disember':'Dec','Desember':'Dec','DESEMBER':'Dec','Agustus':'August','AGUSTUS':'August','Juni':'June','JUNE':'June'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)

            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//div/h2/a/@href'))
            if 'w.rakyatmerdeka.tv' in link:
                continue
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="pagination"]/li[@class="next"]/a/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="intro"]//text()'))
        text = textify(hdoc.select('//div[@class="post newsContent"]//text()'))  or textify(hdoc.select('//div[@class="title titleWrap"]/following-sibling::div[@class="intro"]//text()'))
        date = textify(hdoc.select('//div[@class="newsDate"]/p/text()')) or textify(hdoc.select('//div[@class="titlex"]/following-sibling::p/span[i[@class="fa fa-clock-o"]]//text()')) 
        date = ''.join(re.findall('\d+.*',date))
        if '|' in date:
            date = date.split('|')[0]
        date_dict = {'Januari':'Jan','JANUARI':'Jan','FEBRUARI':'Feb','Februari':'Feb', 'MAC':'March','Mac':'March','Juli':'July','JULI':'July','Maret':'March','MARET':'March', 'Mei':'May','MEI':'May','JULAI':'July', 'Julai':'July', ' Ogos':'Aug','OGOS':'Aug', 'Oktober':'Oct', 'OKTOBER':'October','DISEMBER':'Dec','Disember':'Dec','Desember':'Dec','DESEMBER':'Dec','Agustus':'August','AGUSTUS':'August','Juni':'June','JUNE':'June'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@class="newsDate"]/p/text()'))
        if '|'  in author:
            auth = ''.join(author.split('|')[1])
            auth = auth.replace(':','')

            if auth:            
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('text',xcode(text))
                item.set('dt_added',xcode(dt_added))
                item.set('author', {'name':xcode(auth)})
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
