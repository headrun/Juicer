from juicer.utils import*
from dateutil import parser

class Metrotvnews_ID(JuicerSpider):
    name = 'metro_tvnews_id'
    start_urls = ['http://www.metrotvnews.com/']

    def parse(self,response):
        hdoc = HTML(response)
        add_cate = ['http://pilkada.metrotvnews.com/', 'http://www.metrotvnews.com/index/']
        for cat in add_cate:
            yield Request(cat,self.parse_subcategories,response)
        categories = hdoc.select('//div[@class="submenu"]//div[@class="wrap"]/ul[@class="st-1"]/li/a/@href | //li[@title=".st-2"]/a/@href | //li[@title=".st-3"]/a/@href').extract()
        for cate in categories:
            yield Request(cate,self.parse_subcategories,response)

    def parse_subcategories(self,response):
        hdoc = HTML(response)
        sub_categories = hdoc.select('//div[@class="submenu"]//div[@class="wrap"]/ul[@class="st-1"]/li[not(@class)]//a/@href |  //div[@class="menu"]//li[not(@class)]/a/@href').extract()  or hdoc.select('//a[@class="category"]/@href').extract()
        for cat in sub_categories:
            yield Request(cat,self.parse_links,response)



    def parse_links(self,response):
        hdoc = HTML(response)
        main_link = textify(hdoc.select('//a[@class="bu2"]/@href')) or textify(hdoc.select('//ul[@class="list"]//following-sibling::div/a[@class="more1"]/@href')) or textify(hdoc.select('//a[@class="more-bottom"]/@href'))
        if not main_link:
            links = hdoc.select('//div[@class="cleft"]//h1/a/@href').extract()
            for link in links:
                yield Request(link,self.parse_details,response)

            nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u203a'))
            if nxt_pg:
                yield Request(nxt_pg,self.parse_links,response)
        yield Request(main_link,self.parse_sub_links,response)

    def parse_sub_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="ti1"]') 
        for node in nodes:
            date = textify(node.select('.//div[@class="date"]//text()')) 
            date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
            for key,value in date_dict.iteritems():
                if key in date: date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h2/a/@href')) 
            yield Request(link,self.parse_details,response)

        if not nodes:
            nodes1 = hdoc.select('//div[@class="topic"] | //div[@class="grid"]')
            for node1 in nodes1:
                dt = textify(node1.select('.//div[@class="reg"]/text()'))
                date = ''.join(re.findall(r'\d+.*',dt))
                date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
                for key,value in date_dict.iteritems():
                    if key in date: date = date.replace(key,value)
                date_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node1.select('.//h1/a/@href | .//h2/a/@href'))
                yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[@rel="next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_sub_links,response)
         
         
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[contains(@class, "detail")]//h1//text()')) or textify(hdoc.select('//div[@class="ti1"]/h2/text()'))
        text = textify(hdoc.select('//div[@class="tru"]//text()')) 
        if not text:
            text = textify(hdoc.select('//div[@class="w700 fl"]//strong/text() | //div[@class="w700 fl"]//strong/following-sibling::text() | //div[@class="w700 fl"]//span/following-sibling::text() | //div[@class="w700 fl"]//following-sibling::div/text() | //div[@class="w700 fl"]//p//text()')) or textify(hdoc.select('//div[@class="sum"]//text()'))
        junk_links = textify(hdoc.select('//div[@class="tru"]/div//text()'))  
        text = text.replace(junk_links,'')
        date = textify(hdoc.select('//div[@class="reg"]/text()'))
        date=''.join(re.findall('\d+.*',date))
        if not date:
            date = textify(hdoc.select('//div[@class="video"]//following-sibling::div[@class="icon2"]/div[span[@class="fa fa-calendar ico"]]/text()')) or textify(hdoc.select('//div[contains(@class, "detail")]//span[@class="tgl"]/text()'))
        date_dict = {'Januari':'Jan', 'Februari':'Feb', 'Mac':'March','Juli':'July','Maret':'March', 'Mei':'May', 'Julai':'July', 'Ogos':'Aug', 'Oktober':'Oct', 'Disember':'Dec','Desember':'Dec','Agustus':'August','Juni':'June','Maret':'March'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
        author = textify(hdoc.select('//div[@class="reg"]/text()'))
        author = author.split(u'\u2022')[0].strip()

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author',xcode(author)
