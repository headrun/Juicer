from juicer.utils import *
from dateutil import parser

class VanillaProductreviews(JuicerSpider):
    name = "vanilla_productreviews"
    start_urls = ['http://www.vanilla.in.th/ranking/latest/category/top']

    def parse(self,response):
        hdoc = HTML(response)

        nodes = hdoc.select('//ul[@class="category-list hide-phone-soft"]/li/a/@href').extract()

        for node in nodes[:3]:
            if 'http' not in node: node = 'http://www.vanilla.in.th' + node
            yield Request(node,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        review_links = hdoc.select('//strong[@class="name"]/a/@href').extract()

        for review_link in review_links[:3]:
            if 'http' not in review_link: review_link = 'http://www.vanilla.in.th' + review_link
            yield Request(review_link,self.reviews,response)

        try: next_page = hdoc.select('//i[@class="icon pagination right"]/parent::a/@href').extract()[0]
        except: next_page = ''
        if next_page != '':
            next_page = 'http://www.vanilla.in.th' + textify(next_page)
            #yield Request(next_page,self.parse_next,response)

    def reviews(self,response):
        hdoc = HTML(response)
        brand = textify(hdoc.select('//div//strong[contains(text(),"Brand")]/parent::span/following-sibling::span/a/text()'))
        brand_url = textify(hdoc.select('//div//strong[contains(text(),"Brand")]/parent::span/following-sibling::span/a/@href'))
        item_name = textify(hdoc.select('//div//strong[contains(text(),"Item Name")]/parent::span/following-sibling::span/text()'))
        category = textify(hdoc.select('//div//strong[contains(text(),"Category")]/parent::span/following-sibling::span/a/text()'))
        product_details = {'brand':brand,'brand_url':brand_url,'item_name':item_name,'category':category}
        all_reviews = hdoc.select('//button[contains(text(),"View All")]/parent::a/@href').extract()
        yield Request(all_reviews,self.review_details,response,meta={'product_details':product_details})

    def review_details(self,response):
        hdoc = HTML(response)
        is_next = True
        product_details = response.meta['product_details']
        product_title = textify(hdoc.select('//font[@class="gold"]/text()'))
        avg_rating = textify(hdoc.select('//ul[@class="stars review clearfix hide-phone"]/text()'))
        avg_rating = '.'.join(re.findall('\d+',avg_rating))

        threads = hdoc.select('//article[@class="product-review"]')

        for thread in threads:
            author_name = textify(thread.select('.//span[@class="username"]/strong//text()'))
            author_url = textify(thread.select('.//span[@class="username"]/strong/a/@href'))
            date = textify(thread.select('.//div[@class="date"]'))
            dt_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=7))
            rating = textify(thread.select('.//ul[@class="stars clearfix"]//text()'))
            comment = textify(thread.select('.//p[@class="thaiSTD comment"]//text()'))
            benifits = textify(thread.select('.//ul/li[@class="title colLeft"]/following-sibling::li/span/text()'))
            shopped_at = textify(thread.select('.//li[contains(text(),"Shopped at")]/following-sibling::li[@class="clearfix  colRight"]//text()')[0])
            reviewd_when = textify(thread.select('.//li[contains(text(),"Reviewed when")]/following-sibling::li[@class="clearfix  colRight"]/text()'))

            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
                import pdb;pdb.set_trace()
            sk = xcode(author_name) + str(dt_added) + xcode(comment)
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(product_title))
            item.set('avg_rating',avg_rating)
            item.set('product_details',product_details)
            item.set('author',{'name':author_name,'url':author_url})
            item.set('date',dt_added)
            item.set('rating',rating)
            item.set('text',xcode(comment))
            item.set('benifits',xcode(benifits))
            item.set('shopped_at',xcode(shopped_at))
            item.set('reviewd_when',xcode(reviewd_when))
            item.set('sk',md5(sk))
            item.set('xtags',['reviewss_sourcetype_manual','thailand_country_manual'])
            #yield item.process()

        nxt_page = textify(hdoc.select('//div[@class="pagination aligncenter"]//i[@class="icon pagination right"]/parent::a/@href'))

        if nxt_page and is_next:
            yield Request(nxt_page,self.review_details,response,meta={'product_details':product_details})

