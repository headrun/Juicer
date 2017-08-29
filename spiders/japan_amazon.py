from juicer.utils import*
from dateutil import parser

class Amazonproductreviews(JuicerSpider):
    name = 'amazon_productreviews'
    satrt_urls = ['http://www.amazon.co.jp/gp/product/B00CAGCVZE/ref=s9_ri_gw_g23_i1/378-7091547-9532309?pf_rd_m=AN1VRQENFRJN5&pf_rd_s=desktop-7&pf_rd_r=07QWSTPE7428MCT1HBY4&pf_rd_t=36701&pf_rd_p=205640389&pf_rd_i=desktop']

    '''def parse(self,response):
        hdoc = HTML(response)
        threads = hdoc.select('//div[@class="categoryRefinementsSection"]//span[@class="refinementLink"]/parent::a/@href').extract()

        for thread in threads[:2]:
            if 'http' not in thread: thread = 'http://www.amazon.in' + textify(thread)
            yield Request(thread,self.parse_products,response)

    def parse_products(self,response):
        hdoc = HTML(response)
        product_links = hdoc.select('//a[contains(@href,"customerReviews")]/@href').extract()

        for product_link in product_links[:3]:
            if 'http' not in product_link: product_link = 'http://www.amazon.in' + product_link
            yield Request(product_link,self.review_links,response)

        nxt_page = textify(hdoc.select('//span[@class="pagnRA"]/a[@title="Next Page"]/@href'))
        if 'http' not in nxt_page: nxt_page = 'http://www.amazon.in' + nxt_page
        yield Request(nxt_page,self.parse_products,response)

    def review_links(self,response):
        hdoc = HTML(response)
        review_link = textify(hdoc.select('//a[@class="a-link-emphasis a-nowrap"][contains(@href,"product-reviews")]/@href'))
        if review_link: 'http://www.amazon.in' + review_link
        yield Request(review_link,self.reviews,response)'''

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@id="cm_cr-review_list"]/div[@class="a-section review"]')
        product_title = textify(hdoc.select('//div[@class="a-row product-title"]//a/text()'))
        product_link = textify(hdoc.select('//div[@class="a-row product-title"]//a/@href'))
        if 'http' not in product_link: product_link = 'http://www.amazon.in' + product_link

        for node in nodes:
            _id = textify(node.select('.//@id[1]'))
            author = textify(node.select('.//span[contains(@class,"review-byline")]/a/text()')) or textify(node.select('.//span[contains(@class,"review-byline")]/text()'))
            author_link =textify(node.select('.//span[contains(@class,"review-byline")]/a/@href'))
            if 'http' not in author_link:author_link = 'http://www.amazon.in' + author_link
            date = textify(node.select('.//span[contains(@class,"review-date")]'))
            if 'on' in date:date = date.strip('on')
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            title = textify(node.select('.//a[contains(@class,"review-title")]/text()'))
            title_link = textify(node.select('.//a[contains(@class,"review-title")]/@href'))
            if 'http' not in title_link: title_link = 'http://www.amazon.in' + title_link
            text = textify(node.select('.//span[contains(@class,"review-text")]//text()'))
            rating = textify(node.select('.//i[contains(@class,"review-rating")]/span[contains(text(),"stars")]/text()'))
            if rating: rating = rating.split('out')[0]
            url = response.url + '#' + _id
            sk = hashlib.md5(url).hexdigest()

            #item = Item(response)
            print 'url',response.url + '#' + _id
            #item.set('sk', sk)
            print 'title', xcode(title + ' ' + '##<>##' + ' ' + product_title)
            #item.set('dt_added',dt_added)
            #item.set('author',{'name':author,'link':author_link})
            print 'title_link',title_link
            print 'rating',rating
            print 'text',xcode(text)
            #'xtags', ['india_country_manual', 'reviews_sourcetype_manual', 'ecomm_reviews_sourcetype_manual'])
            #yield item.process()

        next_pg = textify(hdoc.select('//li[@class="a-last"]/a[contains(text(),"Next")]/@href'))
        #if 'http' not in next_pg: next_pg = 'http://www.amazon.in' + next_pg
        #yield Request(next_pg,self.parse,response)


