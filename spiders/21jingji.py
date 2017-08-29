from juicer.utils import *
import re

class Jingji(JuicerSpider):
    name = 'jingji'
    start_urls = ['http://m.21jingji.com/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes =  hdoc.select('//div[@class="nav"]/ul//li/a/@href').extract()

        for node in nodes:
            node_id = node.split('=')[-1]
            yield Request(node,self.news_links,response,meta={'page':1,'node_id':node_id})

    def news_links(self,response):
        hdoc = HTML(response)
        page = response.meta['page']
        node_id = response.meta['node_id']
        main_news_urls = hdoc.select('//div[@class="news_list"]//a')

        for main_url in main_news_urls:
            try: _date = textify(main_url.select('.//div[@class="news_date"]/text()')[0])
            except: pass
            _dt_added = get_timestamp(parse_date(xcode(_date)) - datetime.timedelta(hours=8))


            if _dt_added <  get_current_timestamp()-86400*2:
                continue
            other_url = textify(main_url.select('.//@href')[0])
            yield Request(other_url,self.details,response)

        url = 'http://m.21jingji.com/reader/getListAjaxV3?more=1&page=%s&id=%s'%(page,node_id)
        yield Request(url,self.news_urls,response,meta={'page':page,'node_id':node_id})

    def news_urls(self,response):
        hdoc = HTML(response)
        is_next = True
        news_urls = hdoc.select('//div[@class="news_list"]')

        for news_url in news_urls:
            news_date = textify(news_url.select('.//div[@class="news_date"]/text()')[0])
            news_dt_added = get_timestamp(parse_date(xcode(news_date)) - datetime.timedelta(hours=8))
            if news_dt_added < get_current_timestamp()-86400*3:
                is_next = False
                continue

            news_links = textify(news_url.select('.//a/@href')[0])
            yield Request(news_links,self.details,response)

        if news_urls and is_next:
            page = response.meta['page']
            node_id = response.meta['node_id']
            page += 1
            url = 'http://m.21jingji.com/reader/getListAjaxV3?more=1&page=%s&id=%s'%(page,node_id)
            yield Request(url,self.news_urls,response,meta={'page':page,'node_id':node_id})

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="titleHead"]/h1/text()'))
        date=textify(hdoc.select('//div[@class="newsDate"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="txtContent"]//p//text()'))
        auth1 = textify(hdoc.select('//div[@class="newsInfo"]//a[1]//text()'))
        auth2 = textify(hdoc.select('//div[@class="newsInfo"]//a[2]//text()'))
        author_url1 = textify(hdoc.select('//div[@class="newsInfo"]//a[1]//@href'))
        author_url2 = textify(hdoc.select('//div[@class="newsInfo"]//a[2]//@href'))
        
        
        

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('author',{'name':xcode(auth1)})
        item.set('author',{'name':xcode(auth2)})
        item.set('dt_added',xcode(dt_added))
        item.set('text',xcode(text))
        item.set('xtags',['china_country_manual','news_sourcetype_manual'])
        yield item.process()
