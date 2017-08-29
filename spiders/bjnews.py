from juicer.utils import *

class Bjnews(JuicerSpider):
    name = 'bjnews'
    start_urls = ['http://www.bjnews.com.cn/']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="nav"]//ul//li/a/@href').extract()

        for node in nodes[:1]:
            node = 'http://www.bjnews.com.cn/opinion/'
            if 'health' in node or 'edu' in node or 'travel' in node or 'fashion' in node or 'auto' in node:
                yield Request(node,self.sub_cat,response)
            else:
                yield Request(node,self.news_links,response)

    def sub_cat(self,response):
        hdoc = HTML(response)
        cat_links = textify(hdoc.select('//div[@class="cnav"]/div[@class="lf"]/a/@href'))
        yield Request(cat_links,self.news_links,response)

    def news_links(self,response):
        hdoc = HTML(response)
        is_next = True
        new_links = hdoc.select('//div[@class="lleft"]//div[@class="news"]')

        for news_link in new_links:
            main_date = textify(news_link.select('.//dt/text()'))
            main_dt_added = get_timestamp(parse_date(xcode(main_date)) - datetime.timedelta(hours=8))

            if main_dt_added <  get_current_timestamp()-86400*40:
                is_next = False
                continue

            news_url = textify(news_link.select('.//a/@href'))
            #yield Request(news_url,self.details,response)

        nxt_pg = textify(hdoc.select('//div[@id="page"]/a[@class="next"]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://www.bjnews.com.cn' + nxt_pg
            print nxt_pg
            yield Request(nxt_pg,self.news_links,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="nleft"]/h1/text()'))
        category = textify(hdoc.select('//dl[@class="ntit"]//em/a/text()'))
        category_url = textify(hdoc.select('//dl[@class="ntit"]//em/a/@href'))
        date = textify(hdoc.select('//dl[@class="ntit"]//span[@class="date"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="content"]//p//text()[not(ancestor::p/span/text())]'))
        text1 = textify(hdoc.select('//div[@class="desc"]/p[@class="ctdesc"]/text()'))
        if text1:
            text = text1 + text
        else:
            text = text
        editor = textify(hdoc.select('//span[@id="editor_baidu"]/text()')).split(u'\uff1a')[-1]
        source = textify(hdoc.select('//div[@class="nleft"]//span[@id="source_baidu"]/a/text()'))
        source_url = textify(hdoc.select('//div[@class="nleft"]//span[@id="source_baidu"]/a/@href'))


        if title != '':
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('author.name',xcode(editor))
            item.set('text',xcode(text))
            item.set('xtags',['china_country_manual','news_sourcetype_manual'])
            #yield item.process()
