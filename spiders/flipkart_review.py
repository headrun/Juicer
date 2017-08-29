from juicer.utils import *
from dateutil import parser

class Flipkartreview(JuicerSpider):
    name = 'flipkart_productreviews'
    start_urls = ['http://www.flipkart.com/asus-zenfone-5/product-reviews/ITME3WQUBZYWJ3FH?pid=MOBE3HYEBFRKHRGG&type=all&sort=most_recent']

    '''def parse(self,response):
        hdoc = HTML(response)
        model_links = hdoc.select('//div[@class="nav-section-cat-list"][1]/a[contains(@data-tracking-id,"All")]/@href').extract() or hdoc.select('//ul[@data-tracking-id]/a[@class="link fk-display-block"]/@href').extract()

        for model_link in model_links[:1]:
            if 'http' not in model_link: model_link = 'http://www.flipkart.com' + model_link
            yield Request(model_link,self.product_links,response)

    def product_links(self,response):
        hdoc = HTML(response)
        product_urls = hdoc.select('//a[@data-tracking-id="prd_title"]/@href').extract()

        for product_url in product_urls[:1]:
            if 'http' not in product_url: 'http://www.flipkart.com' + product_url
            yield Request(product_url,self.review_links,response)

        next_pg = textify(hdoc.select('//div[@id="pagination"]/a[@class="next"]/@href'))
        if 'http' not in next_pg: next_pg = 'http://www.flipkart.com' + next_pg
        yield Request(next_pg,self.product_links,response)

    def review_links(self,response):
        hdoc = HTML(response)
        reviewlink = hdoc.select('//p[@class="subText"]/a/@href').extract()
        if 'http' not in reviewlink: reviewlink = 'http://www.flipkart.com' + textify(reviewlink)
        yield Request(reviewlink,self.reviews,response)'''

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="fclear fk-review fk-position-relative line "]')
        product_title = textify(hdoc.select('//div[@class="product-info line"]//h1[@class="title"]/text()'))
        product_title = product_title.strip('Reviews of')

        for node in nodes:
            author_name = textify(node.select('.//a[@class="load-user-widget fk-underline"]/text()')) or textify(node.select('.//span[@class="fk-color-title fk-font-11 review-username"]/text()'))
            author_link = textify(node.select('.//a[@class="load-user-widget fk-underline"]/@href'))
            _id = textify(node.select('.//@review-id'))
            date = textify(node.select('.//div[@class="date line fk-font-small"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            title = textify(node.select('.//div[@class="line fk-font-normal bmargin5 dark-gray"]/strong/text()'))
            rating = textify(node.select('.//div[@class="fk-stars"]/@title'))
            text = textify(node.select('.//span[@class="review-text"]//text()'))


            item = Item(response)
            item.set('url',response.url + '#' + _id)
            item.set('title',xcode(title + ' ' + '##<>##' + ' ' + product_title))
            item.set('dt_added',dt_added)
            item.set('author',{'name':xcode(author_name),'link':author_link})
            item.set('rating',rating)
            item.set('text',xcode(text))

        nxt_pg = textify(hdoc.select('//a[@class="nav_bar_next_prev"][contains(text(),"Next Page")]/@href'))
        if 'http' not in nxt_pg: nxt_pg = 'http://www.flipkart.com' + nxt_pg
        yield Request(nxt_pg,self.parse,response)

