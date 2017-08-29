from juicer.utils import *

class DealerraterTerminalSpider(JuicerSpider):
    name = 'dealerrater_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('-')[-1]
        sk = sk.split('/')[0]
        manufacturers = textify(hdoc.select('//div[@id="reviewLeft"]/div[@id="dealerInfo"]/span/text()')).replace('Manufacturer:',' ')
        item.set('sk',sk)
        item.textify('title', '//h1')
        item.textify('st_address', '//span[@class="street-address"]')
        item.textify('locality', '//span[@class="locality"]')
        item.textify('postal-code', '//span[@class="postal-code"]')
        item.textify('region', '//span[@class="region"]')
        item.textify('telephoneno', '//span[@class="tel"]')
        item.set('manufacturers', manufacturers)
        review = []
        nodes = hdoc.select('//div[@class="hreview"]')
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//span[@class="reviewer"]'))
            details['reviewed_date'] = textify(node.select('.//span[@class="dtreviewed"]'))
            details['user_rating'] = textify(node.select('.//div[@class="userReviewTopRight"]//strong//span'))
            details['comment'] = textify(node.select('.//span[@class="description"]'))
            review.append(details)
        item.set('review', review)
        yield item.process()
        revw_next = hdoc.select('//center//h3//a/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'review':review , 'item':item})

    def parse_reviews(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        review = response.meta.get('review')
        sk = get_request_url(response).split('-')[-1]
        sk = sk.split('/')[0]
        manufacturers = textify(hdoc.select('//div[@id="reviewLeft"]/div[@id="dealerInfo"]/span/text()')).replace('Manufacturer:',' ')
        item.set('sk',sk)
        item.textify('title', '//h1')
        item.textify('st_address', '//span[@class="street-address"]')
        item.textify('locality', '//span[@class="locality"]')
        item.textify('postal-code', '//span[@class="postal-code"]')
        item.textify('region', '//span[@class="region"]')
        item.textify('telephoneno', '//span[@class="tel"]')
        item.set('manufacturers', manufacturers)
        review = []
        nodes = hdoc.select('//div[@class="hreview"]')
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//span[@class="reviewer"]'))
            details['reviewed_date'] = textify(node.select('.//span[@class="dtreviewed"]'))
            details['user_rating'] = textify(node.select('.//div[@class="userReviewTopRight"]//strong//span'))
            details['comment'] = textify(node.select('.//span[@class="description"]'))
            review.append(details)
        revw_next = hdoc.select('//center//h3//a/@href')
        if revw_next:
            yield Request(revw_next, self.parse_reviews, response, meta={'review':review, 'item':item})
        else:
            item.set('review', review)
            yield item.process()
