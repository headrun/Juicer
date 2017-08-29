from juicer.utils import *
import re

class Caijing(JuicerSpider):
    name = 'caijing'
    start_urls = ['http://www.caijing.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="head"]//div[@class="naviga"]//ul[@class="naviga1"]//li/a/@href').extract()

        for node in nodes:
            if 'http://yuanchuang.caijing.com.cn/' in node:
                yield Request(node,self.news_links,response)
            else:
                yield Request(node,self.parse_threads,response)

    def parse_threads(self,response):
        hdoc = HTML(response)
        threads= hdoc.select('//ul[@id="oNav"]//li/a/@href').extract()
        for thread in threads:
            yield Request(thread,self.news_links,response)

    def news_links(self,response):
        hdoc = HTML(response)
        is_next = True
        newslinks = hdoc.select('//ul[@class="list"]/li')
        tech_newslinks = hdoc.select('//div[@class="tech_list tech_list2"]/ul/li')
        if 'tech.caijing' in response.url:
            for tech_newslink in tech_newslinks:
                date = textify(tech_newslink.select('.//div[@class="list_author"]/text()'))
                tech_date = textify(re.findall('\d+',date)).replace(' ','-')
                tech_dt_added = get_timestamp(parse_date(xcode(tech_date)) - datetime.timedelta(hours=8))
                if tech_dt_added < get_current_timestamp()-86400*7:
                    is_next = False
                    continue
                tech_news_url = textify(tech_newslink.select('.//div[@class="list_title"]/a/@href'))
                yield Request(tech_news_url,self.details,response)
        else:
            for newslink in newslinks:
                date = textify(newslink.select('.//div[@class="time"]/text()'))
                news_date = textify(re.findall('\d+',date)).replace(' ','-')
                news_dt_added = get_timestamp(parse_date(xcode(news_date)) - datetime.timedelta(hours=8))
                if news_dt_added < get_current_timestamp()-86400*7:
                    is_next = False
                    continue
                news_url = textify(newslink.select('.//div[@class="wzbt"]/a/@href'))
                yield Request(news_url,self.details,response)

        nxt_pg = textify(hdoc.select('//div[@class="thepg"]//li[last()]/a/@href'))
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.news_links,response)

    def details(self,response):
        hdoc = HTML(response)
        date = textify(hdoc.select('//div[@class="ar_source"]//span[@id="pubtime_baidu"]/text()')).split(' ')[0]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        title = textify(hdoc.select('//div[@id="article"]/h2/text()'))
        article= textify(hdoc.select('//div[@class="ar_source"]//span[@id="source_baidu"]/a/text()'))
        article_url = textify(hdoc.select('//div[@class="ar_source"]//span[@id="source_baidu"]/a/@href'))
        date = textify(hdoc.select('//div[@class="ar_source"]//span[@id="pubtime_baidu"]/text()')).split(' ')[0]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@id="the_content"]//p'))
        editor = textify(hdoc.select('//div[@class="ar_writer"]/span[@id="editor_baidu"]/text()')).split(u'\u7f16\u8f91\uff1a')[-1].replace(')','')
        author = textify(hdoc.select('//div[@class="ar_writer"]/span[@id="uthor_baidu"]/text()')).split(u'\u3010\u4f5c\u8005\uff1a')[-1].replace(']','')
        article = {'name':xcode(article),'url':article_url}

        import pdb;pdb.set_trace()
        item = Item(response)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('text',xcode(text))
        if author: item.set('author.name',xcode(author))
        else: item.set('author.name',xcode(editor))
        item.set('article',article)
        item.set('url',response.url)
        #yield item.process()
