from juicer.utils import *
from dateutil import parser

class Eeo(JuicerSpider):
    name = 'eeo'
    start_urls = ['http://www.eeo.com.cn/']

    def parse(self,response):
        import pdb;pdb.set_trace()

        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="left"]/a/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://www.eeo.com.cn' + node
            yield Request(node,self.categories,response)

    def categories(self,response):
        hdoc = HTML(response)
        category = hdoc.select('//div[@class="left m6 ml3"]/a/@href').extract()

        for category_url in category:
            if 'http' not in category_url: category_url = 'http://www.eeo.com.cn' + category_url
            yield Request(category_url,self.news,response)

    def news(self,response):
        hdoc = HTML(response)
        is_next = True
        news_links = hdoc.select('//ul[@class="new_list"]//li')

        for news in news_links:
            dt = textify(news.select('.//span/text()'))
            dt = textify((dt.replace(u'\u6708','-')).replace(u'\u65e5',''))
            urls = textify(news.select('.//a/@href'))
            if urls:
                year = urls.split('/')[3]
                date = year + '-' + dt
                dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
                if dt_added <  get_current_timestamp()-86400*200:
                    is_next = False
                    continue

            if 'http' not in urls: urls = 'http://www.eeo.com.cn' + urls
            yield Request(urls,self.details,response)

        nxt_pg = textify(hdoc.select('//a[@class="next"]/@href'))
        if nxt_pg and is_next:
            if 'http' not in nxt_pg: nxt_pg = 'http://www.eeo.com.cn' + nxt_pg
            yield Request(nxt_pg,self.news,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="wz_bt "]/text()'))
        _date = textify(hdoc.select('//span[@id="pubtime_baidu"]/text()')) or textify(hdoc.select('//div[@class="wz_gongneng "]/div[@class="icos"]/text()'))
        _dt_added = get_timestamp(parse_date(xcode(_date)) - datetime.timedelta(hours=8))
        source = textify(hdoc.select('//span[@id="source_baidu"]/text()'))
        author = textify(hdoc.select('//span[@id="author_baidu"]/text()'))
        editor = textify(hdoc.select('//span[@id="editor_baidu"]/text()'))
        text1 = textify(hdoc.select('//div[@class="wz_dd mt8 "]/text()'))
        text2 = textify(hdoc.select('//div[@id="text_content"]//p//text()'))
        if text1: text = text1 + text2
        else:text = text2

        print'\n'
        print 'url:',response.url
        print 'title:',xcode(title)
        print 'dt_added:',_dt_added
        print 'source:',xcode(source)
        print 'author:',xcode(author)
        print 'editor:',xcode(editor)
        print 'text:',xcode(text)

        item = Item(response)
        item.set('url',response.url)
        item.set('title',title)
        item.set('dt_added',dt_added)
        item.set('author.name',xcode(author))
        item.set('text',xcode(text))

