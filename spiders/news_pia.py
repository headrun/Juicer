from juicer.utils import*
from dateutil import parser
import re

class News_pia_ph(JuicerSpider):
    name = 'news_pia'
    start_urls = ['http://news.pia.gov.ph/regional/CENTRAL']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//li[@class="mega-menu-dropdown"]/a/@href | //ul[@class="col-md-4 mega-menu-submenu"]/li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)
        cates = ['http://pia.gov.ph/blog/welcome/reflections', 'http://pia.gov.ph/blog/welcome/features']
        cate = 'http://news.pia.gov.ph/regional/R03'
        for cate in cates:
            yield Request(cate,self.parse_add_links,response)
    
    
    def parse_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        #main_date = hdoc.select('//div[@class="well margin-bottom-10"]/h4/following-sibling::text()').extract()

        date=hdoc.select('//div[@class="well margin-bottom-10"]/h4/following-sibling::text()').extract()[0]
        date_dict = {'Enero':'Jan','Disyembre':'Dec','Dis':'Dec','Oktubre':'Oct','Nobyembre':'Nov','Okt':'Oct','Enero':'Jan','Nob':'Nov',        'Setyembre':'Sep','Setiembre':'Sep','Set':'Sep','Sept':'Sep','Agosto':'Aug','Ago':'Aug','Hulyo':'July','Hul':'July','Hunyo':'June','Hun':'June','Mayo':'May','Marso':'March','Pebrero':'Feb','Peb':'Feb'}
        for key,value in date_dict.iteritems():
            if key in date: date = date.replace(key,value)
        date = re.findall('((Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|Nov|Dec)\ \d+)', ''.join(date))
        try:date = list(date)[0]
        except:pass
        if not date:
            date = re.findall('((Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|Nov|Dec)\. \d+)', ''.join(date))
        try:date = list(date)[0]
        except:pass 

        date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        if date_added < get_current_timestamp()-86400*30:
            nodes = hdoc.select('//div[@class="well margin-bottom-10"] | //div[@class="blog-post"]')
            for node in nodes:
                is_nxt = False
                continue
                link = textify(node.select('./h4/a/@href | ./h2/a/@href'))
                yield Request(link,self.parse_details,response)



        if not date:
            date =  hdoc.select('//div[@class="well margin-bottom-10"]/h4/following-sibling::text()').extract()[1]
            date = ''.join(date).split('(PIA)')
            import pdb;pdb.set_trace()
            yield Request(date,self.parse_datecutoff,response'''

    def parse_datecutoff(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        is_nxt = True
        '''
        #date_dict = {'Ene':'Jan','Dis':'Dec','Disyembre':'Dec','Oktubre':'Oct','Nob':'Nov','Okt':'Oct','Enero':'Jan','Nobyembre':'Nov',
        'Setyembre':'Sep','Setiembre':'Sep','Set':'Sep','Sept':'Sep','Agosto':'Aug','Ago':'Aug','Hulyo':'July','Hul':'July','Hunyo':'June',
        'Hun':'June','Mayo':'May','Marso':'March','Pebrero':'Feb','Peb':'Feb'}
        #for key,value in date_dict.iteritems():
            #if key in date: date = date.replace(key,value)'''
        date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        import pdb;pdb.set_trace()
        if date_added < get_current_timestamp()-86400*30:
            nodes = hdoc.select('//div[@class="well margin-bottom-10"] | //div[@class="blog-post"]')
            for node in nodes:
                is_nxt = False
                continue
                link = textify(node.select('./h4/a/@href | ./h2/a/@href'))
                yield Request(link,self.parse_details,response)
        nxt_pg = hdoc.select('//ul[@class="pagination"]/li//a//@href').extract()[-2] 
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_links,response)

    def parse_add_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="well margin-bottom-10"] | //div[@class="blog-post"]')
        for node in nodes:
            date = textify(node.select('.//i[@class="icon-calendar-empty"]/following-sibling::text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h4/a/@href | ./h2/a/@href'))
            #yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]/li/a[@rel="next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_add_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

