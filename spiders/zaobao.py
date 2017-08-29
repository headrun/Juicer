from juicer.utils import*
from dateutil import parser

class Zaobao(JuicerSpider):
    name = 'zaobao'
    start_urls = ['http://www.zaobao.com.sg/','http://www.zaobao.com.sg/realtime']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        import pdb;pdb.set_trace()
        nodes = hdoc.select('//ul[@class="bananas"]/li')
        for node in nodes:
            date = textify(node.select('.//span[@class="datestamp"]//text()')) or textify(node.select('.//a/em/text()').extract())[:2]+':'+textify(node.select('.//a/em/text()').extract())[2:]
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('.//a/@href'))
            if 'http' not in link:
                 link = 'http://www.zaobao.com.sg' + link 
                 yield Request(link,self.parse_details,response)

            next_pg = textify(hdoc.select('//div[@class="item-list"]//li[contains(@class, "pager-next")]/a/@href'))
            if 'http' not in next_pg:
                next_pg = 'http://www.zaobao.com.sg' + next_pg
                yield Request(next_pg,self.parse,response)
    
    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//div[@class="body-content"]/h1/text()'))
        text = textify(hdoc.select('//div[@id="FineDining"]/p//text()'))
        date = textify(hdoc.select('//span[@class="datestamp"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)


    

