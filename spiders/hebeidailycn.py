from juicer.utils import *
from dateutil import parser
import re


class HebeiDailyCn(JuicerSpider):
    name = 'hebeidailycn'
    start_urls = ['http://www.hebeidaily.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//div[@class="nav"]//a/@href').extract()
        for category in categories[:2]:
            if 'http' not in category: category = 'http://www.hebeidaily.com.cn' + category
            yield Request(category,self.parse_details,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="tt"] | //ul[@class="list_time_edit"]/li')
        for node in nodes:
            dt = textify(node.select('./span//text()'))
            date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                continue
            link = textify(node.select('./a/@href'))
            if 'http' not in link: link = 'http://www.hebeidaily.com.cn' + link
            yield Request(link,self.parse_data,response)


    def parse_data(self,response):
        hdoc = HTML(response)
        dt_added = ''
        title = textify(hdoc.select('//div[@class="left"]/h1/text()'))
        parts = textify(hdoc.select('//div[@class="zuoze"]//text()'))
        date = re.findall('(.*)\uff1a(.*)\u6765', parts)

        if date:
            date = date[0][-1]
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="cc2"]//p//text()'))
        import pdb;pdb.set_trace()





