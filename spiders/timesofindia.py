from juicer.utils import*
from dateutil import parser

class TimesofIndia(JuicerSpider):
    name = 'timesofindia'
    start_urls = ['http://timesofindia.indiatimes.com/']


    def parse(self,response):
        hdoc = HTML(response)
        cateegories = hdoc.select('//li[@id="nav-city"]//a/@href | //li[@id="nav-india"]/a/@href | //li[@id="nav-world"]//a/@href | //li[@id="nav-business"]//a/@href | //li[@id="nav-sports"]//a/@href | //li[@id="nav-entertainment"]//a/@href | //li[@id="nav-tv"]//a/@href | //li[@id="nav-life"]//a/@href').extract()
        for cat in cateegories:
            cat =['http://timesofindia.indiatimes.com/business/india-business']
#            if 'http' not in cat: cat = 'http://timesofindia.indiatimes.com' + cat
            yield Request(cat,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//ul[@id="content"]//li[@data-msid] | //ul[@class="list5 clearfix"]/li')
        for node in nodes:
            date = textify(node.select('.//span[@class="strupd"]/text()'))  or textify(node.select('.//span[@class="strupd"]/text()')) 
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                continue
            link = textify(node.select('./span/a/@href')) or textify(node.select('./span/a/@href'))
            if 'http' not in link: link = 'http://timesofindia.indiatimes.com' + link
            #yield Request(link,self.parse_details,response)


        if not nodes:
             other_nodes = hdoc.select('//div[@id="fsts"]')
             for nod in other_nodes:
                date = textify(nod.select('./span[@id="dtfrmt1"]/script/text()')) or textify(nod.select('.//span[contains(@id, "dtfrmt")]/script/text()'))
                date=date.split(',')[0]
                date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
                if date_added < get_current_timestamp()-86400*30:
                    continue
                link = textify(nod.select('./h2/a/@href'))
                if 'http' not in link: link = 'http://timesofindia.indiatimes.com' + link
                #yield Request(link,self.parse_details,response)
        add_links = hdoc.select('//div[@id="artlist_posnxt"]//span/a/@href').extract()
        for linke in add_links:
            if 'http' not in linke: linke = 'http://timesofindia.indiatimes.com' + linke
#            yield Request(link,self.parse_details,response)
           
        next_page = textify(hdoc.select('//div[@style="float:right"]/a/@href'))  or textify(hdoc.select('//div[@class="pagenumber1"]//span[@style="font-size:12px"]/following-sibling::a[1]/@href'))
        if 'http' not in next_page: next_page = response.url + next_page
 #       import pdb;pdb.set_trace()
        yield Request(next_page, self.parse_links, response)
        if not next_page:
            nxt_pg = textify(hdoc.select('//ul[@class="pagination"]/li[@class="current"]/a/@href'))
            if 'http' not in nxt_pg:
                nxt_pg = 'http://timesofindia.indiatimes.com' + nxt_pg
                for i in range(2, 100):
                    nxt_pg = nxt_pg.split('?')[0] + '?curpg=%s' % i
                    yield Request(nxt_pg,self.parse_links,response, dont_filert=True)
                    print nxt_pg
                    import pdb;pdb.set_trace()

        
        
        
        
        '''
        categories = hdoc.select('//li[contains(@class, "nav-")]/a/@href').extract()
        for category in categories:
            if 'http' not in category: category = 'http://timesofindia.indiatimes.com' + category
            if 'happytrips' in category or 'blogs' in category  or 'photogallery' in category or 'videos' in category or 'epaperbeta' in category or 'now.tv' in category or 'live' in category or 'magicbricks' in category or 'http://www.gadgetsnow.com?' in category:
                continue
            yield Request(category,self.parse_subcate,response)

    def parse_subcate(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        sub_categories = hdoc.select('//div[contains(@class, "secout")]//div[contains(@class, "name")]/a/@href').extract() or hdoc.select('//div[@class="widget-heading clearfix"]/a/@href').extract() or hdoc.select('//div[@class="tech_blue_nav"]//a/@href').extract()
        for sub_cate in sub_categories:
            if 'http' not in sub_cate: sub_cate = 'http://timesofindia.indiatimes.com' + sub_cate
            yield Request(sub_cate,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        is_next =  True
        import pdb;pdb.set_trace()
        nodes = hdoc.select('//div[@id="fsts"]')
        for node in nodes:
            date = textify(node.select('.//span[contains(@id, "dtfrmt")]//text()'))
            date = textify(re.findall("\'.*'",date))
            print date
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            print date_added
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./h2/a/@href'))
            if 'http' not in link: link = 'http://timesofindia.indiatimes.com' + link
            print link
            #yield Request(link,self.parse_finaldata,response)

        next_pg = textify(hdoc.select('//div[@class="pagenumber1"]//span[@style="float:left;font-weight:bold;"]/a/@href'))
        if next_pg  and is_next:
            yield Request(next_pg,self.parse_links,response)
            import pdb;pdb.set_trace()


    def parse_finaldata(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]/text()'))
        text = textify(hdoc.select('//div[@class="Normal"]//text()'))
        author = textify(hdoc.select('//span[@itemprop="author"]//text()'))
        date = textify(hdoc.select('//span[@class="time_cptn"]/span[@itemprop="datePublished"]/text()')) or textify(hdoc.select('//span[@class="time_cptn"]//text()')) 
        date = date.replace('.', ':')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace()  

        item.set('url', response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('author', {'name':xcode(author)})'''
