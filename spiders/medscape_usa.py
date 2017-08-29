from juicer.utils import*
from dateutil import parser

class Medscape_usa(JuicerSpider):
    name = 'medscape_usa'
    start_urls = [ 'http://www.medscape.com/today']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list=[301]

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="bucketContent"]/ul/li/a/@href').extract()
        for cat in categories[:2]:
            if 'http' not in cat: cat = 'http://www.medscape.com' + cat
            yield Request(cat,self.parse_subcate,response)

    def parse_subcate(self,response):
        hdoc = HTML(response)
        sub_cate = textify(hdoc.select('//div[@id="specialtyTopics"]//div[@class="morelink"]/a/@href'))
        if 'http' not in sub_cate: sub_cate = 'http://www.medscape.com' + sub_cate
        yield Request(sub_cate,self.parse_sublinks,response,meta={'dont_redirect':True})

    def parse_sublinks(self,response):
        hdoc = HTML(response)
        sub_links = hdoc.select('//div[@id="left"]/div[@class="leftBucket"][1]/div[@class="leftBucketContent"]//ul/li/a/@href').extract()
        for link in sub_links[:2]:
            if 'http' not in link: link = 'http://www.medscape.com' + link
            yield Request(link,self.parse_mainlinks,response)

    def parse_mainlinks(self,response):
        hdoc = HTML(response)
        main_links = hdoc.select('//div[@class="morelink"]/a/@href').extract()
        for main_link in main_links:
            if 'http' not in main_link: main_link = 'http://www.medscape.com' + main_link
            yield Request(main_link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="archives"]//li/a/@href').extract()
        for link in nodes:
            yield Request(link,self.parse_maindetails,response)

        nxt_pg = textify(hdoc.select('//div[@id="next20"]/a/@href'))
        if 'http' not in nxt_pg: nxt_pg= 'http://www.medscape.com' + nxt_pg
        if nxt_pg:
            yield Request(nxt_pg,self.parse_details,response)

    def parse_maindetails(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()

