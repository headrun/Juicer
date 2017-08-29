from juicer.utils import*
from dateutil import parser


class prnewswire_In(JuicerSpider):
    name = 'prnewswire_in'
    start_urls = ['http://www.prnewswire.co.in/news-releases/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="headlines-maindiv"] | //div[@class="column"]')
        for node in nodes:
            date = textify(node.select('./div[@class="headlines-subdiv1"]//text() | .//h6/text()'))
            date_added =get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./div[@class="headlines-subdiv2"]/h2/a/@href| ./h2/a/@href'))
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//link[@rel="next"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@id="h1Headline"]/text()'))
        text = textify(hdoc.select('//div[@class="news-col topics"]/div/p//text()'))
        date = ''.join(hdoc.select('//p/span[@class="xn-location"]/following-sibling::span[@class="xn-chron"]//text()').extract()[0])
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        if title == '' or text == '' or date == '':
            import pdb;pdb.set_trace()
            
'''            
        print '/n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'dt_added',xcode(dt_added)'''
