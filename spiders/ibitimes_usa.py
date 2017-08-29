from juicer.utils import*
from dateutil import parser

class Ibitimes_USA(JuicerSpider):
    name = 'ibitimes_usa'
    start_urls = ['http://www.ibtimes.com/business','http://www.ibtimes.com/technology','http://www.ibtimes.com/world','http://www.ibtimes.com/national','http://www.ibtimes.com/media-culture','http://www.ibtimes.com/markets-finance/millennial-money','http://www.ibtimes.com/sports']

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//div[@class="info info-flex"]')
        for node in nodes:
            date = textify(node.select('.//div[a[@rel="author"]]//text()'))
            dt = ''.join(re.findall('\on (.*?)$', date))
            date_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('./h3/a/@href'))
            if 'http' not in link: link = 'http://www.ibtimes.com' + link
            yield Request(link,self.parse_details,response)

        ext_links = hdoc.select('//div[@class="info"]//a/@href').extract()
        for links in ext_links:
            if 'http' not in links: links = 'http://www.ibtimes.com' + links
            yield Request(links,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//ul[@class="pager clearfix"]//li[contains(@class, "pager-next next")]//a/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.ibtimes.com' + nxt_pg
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@itemprop="headline"]//text()'))
        text = textify(hdoc.select('//div[@class="article-body"]//p[not(em)]//text()'))
        date=textify(hdoc.select('//time[@itemprop="datePublished"]//text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author1 = textify(hdoc.select('//span[@class="reg"]/following-sibling::span[@itemprop="author"]/a//text()'))
        author1_url = textify(hdoc.select('//span[@class="reg"]/following-sibling::span[@itemprop="author"]/a/@href'))
        if 'http' not in author1_url: author1_url = 'http://www.ibtimes.com' + author1_url
        author2 = textify(hdoc.select('//span[@class="reg"]//preceding-sibling::span//span[@itemprop="name"]//text()'))
        author2_url = textify(hdoc.select('//span[@class="reg"]//preceding-sibling::span[@itemprop="author"]/a[@rel="author"]/@href'))
        if 'http' not in author2_url: author2_url = 'http://www.ibtimes.com' + author2_url
        if author1 and author2:
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('text',xcode(text))
            item.set('dt_added',xcode(dt_added))
            item.set('author',{'name':xcode(author1)})
            item.set('author_url',xcode(author1_url))
            item.set('author',{'name':xcode(author2)})
            item.set('author_url',xcode(author2_url))
            item.set('xtags',['news_sourcetype_manual','usa_country_manual'])
            yield item.process()

        if not author1:
            author = textify(hdoc.select('//span[@class="author"]//span[@itemprop="name"]//text()'))
            author_url = textify(hdoc.select('//span[@class="author"]//a[@rel="author"]/@href'))
            if 'http' not in author_url: author_url = 'http://www.ibtimes.com' + author_url
            if author:
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('text',xcode(text))
                item.set('dt_added',xcode(dt_added))
                item.set('author',{'name':xcode(author)})
                item.set('author_url',xcode(author_url))
                item.set('xtags',['news_sourcetype_manual','usa_country_manual'])
                yield item.process()

