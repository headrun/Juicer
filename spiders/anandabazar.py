from juicer.utils import*
from dateutil import parser

class Anandabazar_IN(JuicerSpider):
    name = 'anandabazar'
    start_urls = ['http://www.anandabazar.com/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="new-footer-desktop-item"]/a/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http:' + cat
            #yield Request(cat,self.parse_main_link,response)
        add_cat = ['http://www.anandabazar.com/bangladesh-news?ref=hm-topnav', 'http://www.anandabazar.com/women?ref=hm-topnav','http://www.anandabazar.com/lifestyle?ref=hm-topnav']
        for cate in add_cat:
            yield Request(cate,self.parse_main_link,response)


    def parse_main_link(self,response):
        hdoc = HTML(response)
        main_link = textify(hdoc.select('//center/a[@class="btn btn-default aro_btn Morenews"]/@href')) or textify(hdoc.select('//center/a[@class="aro_khobor button [radius round tiny small large]"]/@href')) or textify(hdoc.select('//center/a[@class="btn btn-default aro_btn"]/@href'))
        if 'http' not in main_link: main_link  = 'http://www.anandabazar.com' + main_link
        yield Request(main_link,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="col-xs-12 col-sm-12 col-md-8"]')
        for node in nodes:
            link = textify(node.select('./h3//a/@href'))
            if 'http' not in link: link = 'http://www.anandabazar.com' + link
#            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pagination"]/li[1]//a/text()'))
        if 'http' not in nxt_pg:
            domain = ''.join(re.findall('(http:.*?archive)', response.url))
            nxt_pg = domain +  nxt_pg
        import pdb;pdb.set_trace()
        if nxt_pg.isdigit():
            #nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li[2]//a//@href'))
            pg_num = ''.join(re.findall("page=(.*)&sl", response.url))
            if pg_num:
                pg_num = int(pg_num) + 1
                next_page = response.url.split('?page')[0] + '?page=' + str(pg_num)
        #else:
            nxt_pg = textify(hdoc.select('//ul[@class="pagination"]//li[3]//a//@href'))
        if 'http' not in nxt_pg: 
            domain = ''.join(re.findall('(http:.*?archive)', response.url))
            nxt_pg = domain +  nxt_pg
            yield Request(nxt_pg,self.parse_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        import pdb;pdb.set_trace()
