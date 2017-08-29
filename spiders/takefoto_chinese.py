from juicer.utils import *
from dateutil import parser

class Takefoto(JuicerSpider):
    name = "takefoto_chinese"
    start_urls = ['http://www.takefoto.cn/category/news/sports','http://www.takefoto.cn/category/news/hot','http://www.takefoto.cn/category/news/favorable','http://www.takefoto.cn/category/news/bagua','http://www.takefoto.cn/category/news/beijing','http://www.takefoto.cn/category/news/domestic','http://www.takefoto.cn/category/news/international','http://www.takefoto.cn/category/news/city','http://www.takefoto.cn/category/news/remind','http://www.takefoto.cn/category/news/entertainment','http://www.takefoto.cn/category/news/culture','http://www.takefoto.cn/category/news/site','http://www.takefoto.cn/category/news/history-today-news','http://www.takefoto.cn/category/news/technology','http://www.takefoto.cn/category/news/economy','http://www.takefoto.cn/category/news/net','http://www.takefoto.cn/category/news/public-opinion','http://www.takefoto.cn/category/news/police-act','http://www.takefoto.cn/category/news/wealth','http://www.takefoto.cn/category/news/wanxiang','http://www.takefoto.cn/category/news/shehui','http://www.takefoto.cn/category/news/takefoto','http://www.takefoto.cn/category/news/beiwan','http://www.takefoto.cn/category/news/focus','http://www.takefoto.cn/category/news/haowai','http://www.takefoto.cn/category/news/dazhaopian']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        urls = hdoc.select('//div[@class="list_item"]')
        for url in urls:
            date = textify(url.select('.//span[@class="post_tag"]//text()'))
            _dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if _dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(url.select('./h2//a/@href'))
            if 'http' not in link: link = 'http://www.takefoto.cn' + link
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.takefoto.cn' +  nxt_pg
        if nxt_pg and is_next:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="arc_title page_w mb20"]//text()'))
        text = textify(hdoc.select('//div[contains(@id, "post")]//p//text()'))
        dt = textify(hdoc.select('//div[@class="time-source"]/span//text()'))
        date = ''.join(re.findall('\d{4}-\d{2}-\d{2}',dt))
        auth = textify(hdoc.select('//div[@class="time-source"]/span[2]//text()'))
        if u'\u7f16\u8f91' in auth:
            author = textify(hdoc.select('//div[@class="time-source"]/span[2]//text()')).strip(u'\u7f16\u8f91')
            author = author.replace(':','')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('url', response.url))
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name',xcode(author))
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()
