from juicer.utils import *

class MenupagesTerminalSpider(JuicerSpider):
    name = 'menupages_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        features = textify(hdoc.select('//dl[@class="features"]//dd')).replace('\r\n\t\t\t\t','')
        serves = textify(hdoc.select('//dl[@class="serves"]//dd')).replace('\r\n\t\t\t\t','')
        delivery_area = textify(hdoc.select('//dl[@class="features"]//dd/text()')).replace('\r\n\t\t\t\t','')
        item.textify('restaurant name', '//h2[@class="fn org"]')
        item.textify('address', '//span[@class="addr street-address"]')
        item.textify('cuisine', '//li[@class="cuisine category"]')
        item.textify('locality', '//span[@class="locality"]')
        item.textify('review_count', '//span[@class="count"]')
        item.textify('food rating', '//th[@class="food-rating"]//span')
        item.textify('value rating', '//th[@class="value-rating"]//span')
        item.textify('service rating', '//th[@class="service-rating"]//span')
        item.textify('atmosphere rating', '//th[@class="atmosphere-rating"]//span')
        item.textify('phone', '//dd[@class="value"]')
        item.textify('postal code', '//span[@class="postal-code"]')
        item.textify('region', '//span[@class="region hide-microformat"]')
        item.textify('note', '//dl[@class="notes"]//dd//span[@class="note"]')
        item.textify('working hours', '//dl[@class="hours"]//dd//span[@class="note"]')
        item.set('sk', sk)
        item.set('serves', serves)
        item.set('features', features)
        item.set('delivery area', delivery_area)
        reviews = []
        revw_next = hdoc.select('//li[@class="first"]//a/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'reviews':reviews, 'item':item})
        yield Request(get_request_url(response), self.parse_reviews, response) 

    def parse_reviews(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        reviews = response.meta.get('reviews')
        item = response.meta.get('item')
        nodes = hdoc.select('//li[@class="comment hreview"]')
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//div[@class="comment-info"]//p//em'))
            details['review_date'] = textify(node.select('.//span[@class="dtreviewed"]'))
            details['comment'] = textify(node.select('.//h6[@class="summary"]'))
            details['rvw_desc'] = textify(node.select('.//p[@class="description"]'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
