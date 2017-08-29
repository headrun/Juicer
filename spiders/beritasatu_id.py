from juicer.utils import*
from dateutil import parser

class Beritasatu_ID(JuicerSpider):
    name = 'beritasatu_id'
    start_urls = ['http://www.beritasatu.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="footer-kanal"]/a/@href').extract()
        for cat in categories:
            if 'beritasatu.com/pages/profile/' in cat:
                continue
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        cat_links = hdoc.select('//a[@class="btn btnindex"]/@href').extract()
        for cate in cat_links:
            yield Request(cate,self.parse_main_links,response)
        if not cat_links:
            is_nxt = True
            nodes = hdoc.select('//div[@class="right pl10"]')
            for node in nodes:
                date = textify(node.select('./div[@class="c6 mb5"]/text()'))
                date = ''.join(re.findall('\d+.*',date))
                date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
                for key,value in date_dict.iteritems():
                    if key in date: date = date.replace(key,value)
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('.//h2/a/@href'))
                yield Request(link,self.parse_details,response)
                
            if not nodes:
                add_links = hdoc.select('//div[@class="box-shadow prl10 ptb5"]//h2/a/@href').extract()
                for add_link in add_links:
                    yield Request(add_link,self.parse_details,response)

            nxt_pg = textify(hdoc.select('//a[contains(.,"Next")]/@href'))
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)

    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div//div[@class="mb10 bbcd pb5"]')
        for node in nodes:
            date = textify(node.select('./preceding-sibling::div/text()'))
            date = ''.join(re.findall('\d+.*',date))
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//preceding-sibling::a[u[@class="f16"]]/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = list(set(hdoc.select('//div[@class="clear mt10"]//preceding-sibling::div//a[contains(.,"Next")]/@href').extract()))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="hl__title"]/h1/text()')) or textify(hdoc.select('//h2[@class="f16 mtb10"]/text()'))
        if not title:
            title = textify(hdoc.select('//title/text()'))
            title = title.split('|')[0]
            title=title.replace('VIDEO:','')
        text=textify(hdoc.select('//div[@class="f14 c6 bodyp"]//text()')) or textify(hdoc.select('//div[@class="mt10 lh16 body_blog c6 lh20"]//text()'))
        junk_link = textify(hdoc.select('//p[a[@target="_blank"]]//text()'))
        txt=textify(hdoc.select('//div[@class="f14 c6 bodyp"]//p[last()]/text()'))
        text=text.replace(txt,'').replace(junk_link,'')
        date = textify(hdoc.select('//div[@class="mtb10"]/span/text()')) or textify(hdoc.select('//span[@class="c6"]/text()'))
        date = ''.join(re.findall('\d+.*',date))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@class="sub"]/text()')) or textify(hdoc.select('//div[@class="blog_author_profile"]//center/strong/text()'))
        author_url = textify(hdoc.select('//div[@class="blog_author_profile"]//a/@href'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author', {'name':xcode(author)})
        item.set('author_url',xcode(author_url))
        item.set('xtags',['news_sourcetype_manual','indonesia_country_manual'])
        yield item.process()
