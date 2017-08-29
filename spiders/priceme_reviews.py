from juicer.utils import *
from dateutil import parser

class Pricemereviews(JuicerSpider):
    name = 'priceme_reviews'
    start_urls = ['http://www.priceme.co.nz/Mobile-Phones/c-11.aspx']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="product-grid-item"]/@href').extract()

        for node in nodes:
            if 'http' not in node: node = 'http://www.priceme.co.nz' + node
            yield Request(node,self.reviews,response)

        next_pg = textify(hdoc.select('//link[@rel="next"]/@href'))
        if 'http' not in next_pg and next_pg: next_pg = 'http://www.priceme.co.nz' + next_pg
        yield Request(next_pg,self.parse,response)

    def reviews(self,response):
        hdoc = HTML(response)
        review_link = textify(hdoc.select('//ul[@role="tablist"]//a[contains(text(),"Reviews")]/@href'))

        if 'http' not in review_link and review_link: review_link = 'http://www.priceme.co.nz' + review_link
        yield Request(review_link,self.review_details,response)

    def review_details(self,response):
        hdoc = HTML(response)
        product_title = textify(hdoc.select('//h1[@class="productInfo"]/text()')).strip('Reviews')
        threads = hdoc.select('//div[@id="catalogProductsDiv"]/div[@class="productInfoDiv_List"]')

        for thread in threads:
            review_title = textify(thread.select('.//h3[@itemprop="name"]/text()'))
            rating = textify(thread.select('.//div[@itemprop="ratingValue"]/text()'))
            text = textify(thread.select('.//span[@itemprop="description"]/text() | .//span[@class="rvContentSpan"]/text()'))
            date = textify(thread.select('.//meta[@itemprop="datePublished"]/@content'))
            dt_added = dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=13))

            print '\n'
            print response.url
            print 'title', xcode(product_title + ' ' + '##<>##' + ' ' + review_title)
            print 'dt_added',dt_added
            print 'rating',rating
            print 'text',xcode(text)

        next_page = textify(hdoc.select('//ul[@class="pagination PrettyPagerDiv"]/li/a[@class="pagerAtag"]/@href'))
        if next_page and 'http' not in next_page: next_page = 'http://www.priceme.co.nz' + next_page
        yield Request(next_page,self.review_details,response)
