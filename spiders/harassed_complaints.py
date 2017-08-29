from juicer.utils import *
from dateutil import parser

class HarassedComplaints(JuicerSpider):
    name  = 'harassed_complaints'
    start_urls = 'http://www.harassed.in/complaints'

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        links = hdoc.select('//div[@id="allAdss"]/div[@class="item-list"]')
        for link in links:
            dt = textify(link.select('.//span[@class="date"]/text()'))
            date_added = get_timestamp(parse_date(xcode(dt))-datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            complaint_link = textify(link.select('.//h5[@class="add-title"]/a/@href'))
            yield Request(complaint_link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//li/a[@class="pagination-btn"]/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="auto-heading"]//text()'))
        date = textify(hdoc.select('//div[@class="col-sm-9 page-content col-thin-right"]//span[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=5,minutes=30))
        author = textify(hdoc.select('//span[contains(text(),"person")]/preceding-sibling::span/text()'))
        auth_info_text = hdoc.select('//div[@class="media-body"]/span[@class="media-heading"]/text()').extract()
        auth_info_title = hdoc.select('//div[@class="media-body"]/span[@class="data-type"]/text()').extract()
        auth_info = []
        for key,value in zip(auth_info_title,auth_info_text):
            auth_info.append(str(key) + ':' + str(value))
        other_details = textify(hdoc.select('//aside[@class="panel panel-body panel-details"]/ul/li/p//text()').extract())
        text = textify(hdoc.select('//div[@class="ads-details-info col-md-8"]/p//text()')) or textify(hdoc.select('//meta/@content'))

        item = ITEM(response)
        item.set('url', response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('author',{'name':xcode(author),'other_info':xcode(auth_info)})
        item.set('date', xcode(dt_added))
        item.set('other_details',xcode(str(other_details)))
        item.set('xtags',['forums_sourcetype_manual','india_country_manual'])
        yield item.process()

