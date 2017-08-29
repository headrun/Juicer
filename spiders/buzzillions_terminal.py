from juicer.utils import *

class BuzzillionsTerminalSpider(JuicerSpider):
    name = 'buzzillions_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk',sk)
        item.textify('title', '//span[@class="fn"]')
        item.textify('reviews count', '//div[@id="bz-model-prodRating"]//h5')
        description = textify(hdoc.select('//div[@class="bz-model-description"]//p'))
        item.set('description', description)
        item.textify('specifications', '//div[@class="bz-model-specifications"]//table//tr//td')
        ratings = {}
        ratings['1-star'] = textify(hdoc.select('//td[contains(text(),"1 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['2-star'] = textify(hdoc.select('//td[contains(text(),"2 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['3-star'] = textify(hdoc.select('//td[contains(text(),"3 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['4-star'] = textify(hdoc.select('//td[contains(text(),"4 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['5-star'] = textify(hdoc.select('//td[contains(text(),"5 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        item.set('ratings', ratings)
        saving = textify(hdoc.select('//div[@class="bz-priceDrop"]//span')).replace('SALE\n                 ', ' ')
        savings = saving.split('off')[0]
        item.set('savings', savings)
        reviews = []
        nodes = hdoc.select('//div[@class="hReview bz-model-review"]')
        for node in nodes:
            details = {}
            details['comment'] = textify(node.select('.//h3[@class="summary"]'))
            details['rating'] = textify(node.select('.//span[@class="rating"]'))
            details['rev_description'] = textify(node.select('.//div[@class="bz-model-review-comments-container"]//p'))
            month = textify(node.select('.//span[@class="month"]'))
            date = textify(node.select('.//span[@class="day"]'))
            year = textify(node.select('.//span[@class="year"]'))
            details['review_date'] = date + ' ' + month + ' ' + year
            details['name'] = textify(node.select('.//span[@class="bz-model-review-name fn nickname"]'))
            details['locality'] = textify(node.select('.//span[@class="bz-model-review-location locality"]'))
            reviews.append(details)
        revw_next = hdoc.select('//div[@id="bz-pagination-bottom-page"]//a[contains(text(),"Next ")]/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'reviews':reviews, 'item':item})

    def parse_reviews(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        reviews = response.meta.get('reviews')
        item = response.meta.get('item')
        item.textify('title', '//span[@class="fn"]')
        item.textify('reviews count', '//div[@id="bz-model-prodRating"]//h5')
        description = textify(hdoc.select('//div[@class="bz-model-description"]//p'))
        item.set('description', description)
        item.textify('specifications', '//div[@class="bz-model-specifications"]//table//tr//td')
        ratings = {}
        ratings['1-star'] = textify(hdoc.select('//td[contains(text(),"1 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['2-star'] = textify(hdoc.select('//td[contains(text(),"2 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['3-star'] = textify(hdoc.select('//td[contains(text(),"3 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['4-star'] = textify(hdoc.select('//td[contains(text(),"4 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        ratings['5-star'] = textify(hdoc.select('//td[contains(text(),"5 star")]//following-sibling::td[@class="bz-histogram-value"]'))
        item.set('ratings', ratings)
        saving = textify(hdoc.select('//div[@class="bz-priceDrop"]//span')).replace('SALE\n                 ', ' ')
        savings = saving.split('off')[0]
        item.set('savings', savings)
        reviews = []
        nodes = hdoc.select('//div[@class="hReview bz-model-review"]')
        for node in nodes:
            details = {}
            details['comment'] = textify(node.select('.//h3[@class="summary"]'))
            details['rating'] = textify(node.select('.//span[@class="rating"]'))
            details['rev_description'] = textify(node.select('.//div[@class="bz-model-review-comments-container"]//p'))
            month = textify(node.select('.//span[@class="month"]'))
            date = textify(node.select('.//span[@class="day"]'))
            year = textify(node.select('.//span[@class="year"]'))
            details['review_date'] = date + ' ' + month + ' ' + year
            details['name'] = textify(node.select('.//span[@class="bz-model-review-name fn nickname"]'))
            details['locality'] = textify(node.select('.//span[@class="bz-model-review-location locality"]'))
            reviews.append(details)
        revw_next = hdoc.select('//div[@id="bz-pagination-bottom-page"]//a[contains(text(),"Next ")]/@href')
        if revw_next:
            yield Request(revw_next, self.parse_reviews, response, meta={'reviews':reviews, 'item':item})
        else :
            item.set('reviews', reviews)
            yield item.process()
