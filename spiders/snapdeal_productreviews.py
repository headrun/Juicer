from juicer.utils import *
from dateutil import parser

class SnapdealProductreviews(JuicerSpider):
    name = 'snapdeal_productreviews'
    start_urls = ['http://www.snapdeal.com/product/asus-zenfone-2-laser-55/681651791446']#['http://www.snapdeal.com/products/mobiles-mobile-phones?sort=plrty']#['http://www.snapdeal.com/products/appliances-air-conditioners?sort=plrty']#['http://www.snapdeal.com/products/women-apparel-sarees?sort=plrty']

    '''def parse(self,response):
        hdoc = HTML(response)
        product_links = hdoc.select('//p[@class="product-title"]/parent::a/@href').extract()

        for product in product_links:
            if 'http' not in product: product = 'http://www.snapdeal.com' + product
            yield Request(product,self.parse_reviewlinks,response)

        nxt_page = textify(hdoc.select('//link[@rel="next"]/@href'))
        if nxt_page:
            nxt_page = 'http://www.snapdeal.com' + nxt_page
            yield Request(nxt_page,self.parse,response)'''

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        review_links = hdoc.select('//span[contains(text(),"Most")]/parent::div/following-sibling::div//div[@class="commentlist first"]') or hdoc.select('//div[@id="defaultReviewsCard"]//div[@class="commentlist first"]')
        product_link = textify(hdoc.select('//h1[@class=" pdp-e-i-head"]/@title')) or response.meta['product_link']

        for review in review_links :
            author_name = textify(review.select('.//span[@class="_reviewUserName"]/@title'))
            author_reviews = textify(review.select('.//div[@class="userimg"]/small/text()'))
            title = textify(review.select('.//div[@class="head"]/text()'))
            _id = textify(review.select('.//@id'))
            text = textify(review.select('.//div[@class="text"]//p/text()'))
            rating = len(review.select('.//div[@class="rating"]/i[contains(@class,"sd-icon sd-icon-star active")]').extract())
            date = textify(review.select('.//div[@class="date LTgray"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

            if dt_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            print '\n'
            print 'url', response.url + '#' +_id
            print 'title', title + ' ' + '##<>##' + product_link
            print 'dt_added',dt_added
            print 'rating',rating
            print 'author',{'name':author_name,'no.of.reviews':author_reviews}
            print 'text',xcode(text)

        next_pg = textify(hdoc.select('//li[@class="last"]/a/@href')) or textify(hdoc.select('//div[@class="reviewareain"]//a[@class="btnload LTgray"]/@href'))
        if next_pg and 'java' not in next_pg and is_next:
            yield Request(next_pg,self.parse,response,meta={'product_link':product_link})
