from juicer.utils import*
from dateutil import parser

class Sindonews_ID(JuicerSpider):
    name = 'sindonews_id'
    start_urls = ['http://www.sindonews.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="main-menu"]//li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_sub_cat,response)

    def parse_sub_cat(self,response):
        hdoc = HTML(response)
        sub_cat = hdoc.select('//nav[@class="grid_32 main-nav"]//a/@href').extract() or hdoc.select('//nav[@class="grid_32"]//a/@href').extract()
        for cate in sub_cat:
            yield Request(cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        add_link = hdoc.select('//div[@class="more-blue"]/a/@href').extract()
        yield Request(add_link,self.parse_main_links,response)
        if not add_link:
            is_nxt = True
            nodes = hdoc.select('//span[@class="link-box"]')
            for node in nodes:
                date = textify(node.select('.//div/time/text()'))
                date = ''.join(re.findall('\d+.*',date))
                date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
                for key,value in date_dict.iteritems():
                    if key in date: date = date.replace(key,value)
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))

                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./h3/a/@href'))
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u203a'))
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)



    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="lnk-t"]')
        for node in nodes:
            date = textify(node.select('.//time/text()'))
            date = ''.join(re.findall('\d+.*',date))
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./p/a/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u203a'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)
    

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]/text()')) or textify(hdoc.select('//div[@class="judul-photo"]/h1/text()')) or textify(hdoc.select('//h1[@itemprop="name"]/text()'))
        text = textify(hdoc.select('//div[@id="content"]//p//text()')) or textify(hdoc.select('//div[@id="content"]//text()'))
        date = textify(hdoc.select('//div[@class="judul-video"]//time/text()')) or textify(hdoc.select('//div[@class="judul-photo"]//time/text()')) or textify(hdoc.select('//time/text()')) 
        date = ''.join(re.findall('\d+.*',date))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//a[@rel="author"]/span/text()')) or textify(hdoc.select('//div[@class="author"]/a/text()'))
        author_url = textify(hdoc.select('//a[@rel="author"]/@href')) or textify(hdoc.select('//div[@class="author"]/a/@href'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
#        yield item.process()

        
