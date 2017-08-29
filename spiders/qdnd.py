from juicer.utils import*
from dateutil import parser

class Qdnd_VN(JuicerSpider):
    name = 'qdnd'
    start_urls = ['http://www.qdnd.vn/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="fpcat"]/a[@class="fplink"]/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,response)

        cates = ['http://www.qdnd.vn/cung-ban-luan', 'http://www.qdnd.vn/thuc-hien-hieu-qua-nghi-quyet-trung-uong-iv-khoa-xii-cua-dang']
        for cate in cates:
            yield Request(cate,self.parse_links,response)
    
    def parse_links(self,response):
        hdoc = HTML(response)
        sub_cate_links = hdoc.select('//li[@class="litwo"]/a/@href').extract() or hdoc.select('//div[@class="v3home-block-title ctrang21"]/a[@class="active"]/@href').extract()
        for sub_link in sub_cate_links:
            yield Request(sub_link,self.parse_main_links,response)
        if not sub_cate_links:
            sub_lin = hdoc.select('//a[@rel="v:url"]/@href').extract()
            yield Request(sub_lin,self.parse_main_links,response)

    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="pcontent3 contentCategory"] | //div[@class="col-md-12 col-xs-12 t2tophot"]')
        for  node in nodes:
            date = textify(node.select('.//span[@class="lit-pubinfo"]//text()'))
            date_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h1/a/@href | ./a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_id = textify(hdoc.select('//div[@class="ex_page"]/a[@class="boxdv1 active"]/following-sibling::a[1]/text()'))
        if nxt_id:
            nxt_pg = response.url +'/p/'+ nxt_id
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="post-title"]//text()'))
        add_text = textify(hdoc.select('//div[@class="post-summary"]//h2//text()'))
        main_text = textify(hdoc.select('//div[@class="post-content"]//p//text()'))
        text = add_text + ' ' +  main_text
        date = textify(hdoc.select('//span[@class="post-subinfo"]//text()'))
        dt_added = get_timestamp(parse(xcode(date)) - datetime.timedelta(hours=7))

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','vietnam_country_manual'])
        yield item.process()
