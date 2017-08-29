from juicer.utils import *
from dateutil import parser

class CosmenetReviews(JuicerSpider):
    name = 'cosmenet_reviews'
    start_urls = ['http://www.cosmenet.in.th/review/']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self,response):
        hdoc = HTML(response)

        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=7)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//div[@class="product-name"]/a/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://www.cosmenet.in.th' + node
            yield Request(node,self.parse_details,response)

        nxt_pg = textify(hdoc.select('//div[@class="review-list"]//a[@title="Next"]/@href')[0])
        if nxt_pg and 'http' not in nxt_pg: nxt_pg = 'http://www.cosmenet.in.th/review/' + nxt_pg
        yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        brand = textify(hdoc.select('//span[@itemprop="brand"]/text()'))
        title = textify(hdoc.select('//h1[@class="product_name"]/span/text()'))
        rank = textify(hdoc.select('//div[@class="rank-number"]/text()'))
        rank_type = textify(hdoc.select('//a[@class="rank-type"]/text()'))
        rank_type_url = textify(hdoc.select('//a[@class="rank-type"]/@href'))
        if 'http' not in rank_type_url: rank_type_url = 'http://www.cosmenet.in.th' + rank_type_url
        description = textify(hdoc.select('//div[@class="product_detail_text"]//text()'))
        product_effect = hdoc.select('//div[@class="row product-effect"]/div/@title').extract()
        product_overview = hdoc.select('//div[contains(@class,"col-sm")]//ul[@class="list"]')

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('rank_details',{'rank':rank,'type':xcode(rank_type),'url':rank_type_url})
        item.set('text',xcode(description))
        item.set('product_effect',xcode(product_effect))

        for overview in product_overview:
            item_overview = textify(overview.select('.//li/text()'))
            item.set('product_overview',xcode(item_overview))
        yield item.process()


        threads = hdoc.select('//div[@class="review-list"]//div[@class="item row"]')

        for thread in threads:
            author_name = textify(thread.select('.//span[@class="user_name"]/a/text()'))
            author_url = textify(thread.select('.//span[@class="user_name"]/a/@href'))
            if 'http' not in author_url: author_url = 'http://www.cosmenet.in.th' + author_url
            rating = textify(thread.select('.//div[@class="review-rate"]/@title')).split(u'\u0e14\u0e32\u0e27')[0]
            text = textify(thread.select('.//div[contains(@class,"review-detail")]/p//text()'))
            result_fromuser = textify(thread.select('.//ul[@class="result-from-user"]//text()'))
            date = textify(thread.select('.//span[@class="date"]/text()')).split(u'\u0e23\u0e35\u0e27\u0e34\u0e27\u0e40\u0e21\u0e37\u0e48\u0e2d')[-1]
            date_added = parse_date(date)
            if date_added >= self.cutoff_dt:
                dt_added  = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=7))
                sk = xcode(author_name) + str(dt_added) + xcode(text)

                item = Item(response)
                item.set('sk',md5(sk))
                item.set('url',response.url)
                item.set('title',xcode(title))
                item.set('author',{'name':xcode(author_name),'url':author_url})
                item.set('rating',xcode(rating))
                item.set('result_fromuser',xcode(result_fromuser))
                item.set('dt_added',dt_added)
                item.set('text',xcode(text))
                yield item.process()
