from juicer.utils import *

class ReviewcentreTerminalSpider(JuicerSpider):
    name = 'reviewcentre_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('reviews')[-1]
        sk = sk.split('.html')[0]
        item.set('sk', sk)
        item.textify('title', '//h1[@id="PageTitle"]')
        item.textify('rating', '//span[@property="v:average"]')
        item.textify('recommended percentage', '//div[@id="ItemUserRecommend"]')
        item.textify('reviews count', '//span[@property="v:count"]')
        reviews = []
        nodes = hdoc.select('//div[@class="ReviewCommentContent"]')
        for node in nodes:
            details = {}
            details['name'] = textify(node.select('.//p[@class="UserName"]'))
            details['revw_title'] = textify(node.select('.//div[@class="ReviewCommentContentRight"]//h3//a'))
            details['revw_headline'] = textify(node.select('.//p[@class="Headline"]//span'))
            details['revw_desc'] = textify(hdoc.select('.//div[@class="ReviewCommentContentRight"]//p[@class="Headline"]//following-sibling::p'))
            reviews.append(details)
        '''revw_next = hdoc.select('//div[@class="Pagination"]//a[contains(text(),"Next")]/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'reviews':reviews, 'item':item})
        yield Request(get_request_url(response), self.parse_reviews, response)

    def parse_reviews(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        reviews = response.meta.get('reviews')
        item = response.meta.get('item')
        nodes = hdoc.select('//div[@class="ReviewCommentContent"]')
        for node in nodes:
            details = {}
            details['name'] = textify(node.select('.//p[@class="UserName"]'))
            details['revw_title'] = textify(node.select('.//div[@class="ReviewCommentContentRight"]//h3//a'))
            details['revw_headline'] = textify(node.select('.//p[@class="Headline"]//span'))
            details['revw_desc'] = textify(node.select('.//div[@class="ReviewCommentContentRight"]//h3//following-sibling::p[2]'))
            reviews.append(details)
        revw_next = hdoc.select('//div[@class="Pagination"]//a[contains(text(),"Next")]/@href')
        if revw_next:
            yield Request(revw_next, self.parse_reviews, response, meta={'reviews':reviews, 'item':item})
        else:
        '''
        item.set('reviews', reviews)
        yield item.process()
