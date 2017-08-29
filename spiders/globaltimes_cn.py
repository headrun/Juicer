from juicer.utils import*
from dateutil import parser

class Globaltimes_CN(JuicerSpider):
    name = 'globaltimes_cn'
    start_urls = ['http://www.globaltimes.cn/china/','http://www.globaltimes.cn/business/','http://www.globaltimes.cn/world/','http://www.globaltimes.cn/opinion/','http://www.globaltimes.cn/life/','http://www.globaltimes.cn/arts/','http://www.globaltimes.cn/sci-tech/','http://www.globaltimes.cn/odd/','http://www.globaltimes.cn/sports/','http://www.globaltimes.cn/beijing/','http://www.globaltimes.cn/video/','http://www.globaltimes.cn/photos/']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="row-content"]')
        for node in nodes:
            date = textify(node.select('.//p//smaill//text()'))
            dt=''.join(re.findall('\| (.*?)$', date))
            date_added = get_timestamp(parse_date(xcode(dt))- datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h4/a[@target="_blank"]/@href'))
            yield Request(link,self.parse_details,response)

        if not nodes:
            links = hdoc.select('//div[@class="row-title"]/a/@href').extract()
            for link in links:
                yield Request(link,self.parse_photo_links,response)
        nxt_pg = textify(hdoc.select('//div[@class="row-fluid text-center pages"]//a[contains(text(), "Next")]/@href'))
        nxt_link = re.sub(r'index(.*)', '', response.url)
        if 'http' not in nxt_pg: nxt_pg = nxt_link + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_photo_links(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@class="row-fluid"]//p/a[@target="_blank"]/@href').extract()
        for link in links:
            yield Request(link,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="row-fluid text-center pages"]//a[contains(text(), "Next")]/@href'))
        nxt_link  = re.sub(r'index(.*)', '', response.url)
        if 'http' not in nxt_pg: nxt_pg = nxt_link + nxt_pg
        if nxt_pg:
            yield Request(nxt_pg,self.parse_photo_links,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="row-fluid article-title"]//h3//text()')) or textify(hdoc.select('//div[contains(@class, "fluid article-title")]//h3//text()'))
        date = textify(hdoc.select('//div[@class="span8 text-left"]//text()')) or textify(hdoc.select('//div[contains(@class, "text-left")]//text()'))
        dt = ''.join(re.findall('\: (.*?)$', date))
        if 'Last Updat' in dt:
            dt = dt.partition('Last Updated:')[0]
        dt_added  = get_timestamp(parse_date(xcode(dt))- datetime.timedelta(hours=8))
        ext_txt = textify(hdoc.select('//div[@class="row-fluid article-title"]//h4//text()'))
        text = textify(hdoc.select('//div[@class="span12 row-content"]//text()'))
        text = ext_txt + ' ' + text
        auth = textify(hdoc.select('//div[@class="span8 text-left"]//text()'))
        if 'By' in auth or 'by' in auth: 
            auth = auth.partition('Source:')[0]
            author = auth.replace('By','').replace('by','')
            if author:
                item = Item(response)
                item.set('url',response.url)
                item.set('title', xcode(title))
                item.set('text', xcode(text))
                item.set('dt_added', xcode(dt_added))
                item.set('author',{'name':xcode(author)})
                item.set('xtags',['news_sourcetype_manual','china_country_manual'])
                yield item.process()

        else:
            item = Item(response)
            item.set('url',response.url)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', xcode(dt_added))
            item.set('dt_added', xcode(dt_added))
            yield item.process()



