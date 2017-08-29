from juicer.utils import*
from dateutil import parser

class Dongguan(JuicerSpider):
    name = 'dongguan'
    start_urls = ['http://www.dongguan.net.cn/index.html']
    custom_settings = {'REDIRECT_ENABLED': True}
    handle_httpstatus_list = [404,522,301]

    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="n-box1"]//li/a/@href').extract()
        for cat in categories:
            yield Request(cat,self.parse_links,meta={'dont_redirect':True})

    def parse_links(self,response):
        hdoc = HTML(response)
        more_links = hdoc.select('//div[@class="t-5"]/span//a/@href').extract()
        for link in more_links:
            yield Request(link,self.parse_main_links,response)
        if not more_links:
            is_nxt = True
            nodes = hdoc.select('//li/h3')
            for node in nodes:
                date = textify(node.select('./following-sibling::p[1]//text()'))
                dt = ''.join(re.findall('\d{4}-\d{2}-\d{2}',date))
                date_added = get_timestamp(parse_date(xcode(dt))- datetime.timedelta(hours=8))
                if date_added < get_current_timestamp()-86400*30:
                    is_nxt = False
                    continue
                link = textify(node.select('./a/@href'))
                yield Request(link,self.parse_details,response)
            nxt_pg = textify(hdoc.select('//ul[@class="pagelist"]//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
            if 'http' not in nxt_pg: nxt_pg = response.url + nxt_pg
            if nxt_pg and is_nxt:
                yield Request(nxt_pg,self.parse_links,response)
                

    def parse_main_links(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//li/h3')
        for node in nodes:
            date = textify(node.select('./following-sibling::p[1]//text()'))
            dt = ''.join(re.findall('\d{4}-\d{2}-\d{2}',date))
            date_added = get_timestamp(parse_date(xcode(dt))- datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./a/@href'))
            yield Request(link,self.parse_details,response)
        nxt_pg = textify(hdoc.select('//ul[@class="pagelist"]//a[contains(.,"%s")]/@href'%u'\u4e0b\u4e00\u9875'))
        if 'http' not in nxt_pg: nxt_pg = response.url + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse_main_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="u-5"]//text()'))
        date=textify(hdoc.select('//div[@class="info"]//text()'))
        dt = ''.join(re.findall('\d{4}-\d{2}-\d{2}',date))
        dt_added = get_timestamp(parse_date(xcode(dt))- datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="con"]//p//text()'))
        junk_txt = textify(hdoc.select('//p[@style="text-align:right;"]//text()'))
        text = text.replace(junk_txt,'')
        ext_txt = textify(hdoc.select('//div[@class="txt fl"]//text()'))
        text = ext_txt + ' ' + text
        author = textify(hdoc.select('//p[@style="text-align:right;"]/a/text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', xcode(dt_added))
        item.set('xtags',['news_sourcetype_manual','china_country_manual'])
        yield item.process()
