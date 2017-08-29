from juicer.utils import *

class DrugstoreTerminalSpider(JuicerSpider):
    name = 'drugstore_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/qxp')[-1]
        sk = sk.split('?')[0]
        item.set('sk', sk)
        item.textify('title', '//span[@class="captionText"]')
        item.textify('price', '//div[@id="productprice"]//span')
        rating = textify(hdoc.select('//div[@id="divRating"]')).replace('(', '')
        rating = rating.replace(')', '')
        item.set('rating', rating)
        item.textify('suggested_price', '//div[@id="divPricing"]//span//s')
        item.textify('product_details', '//td[@class="contenttd"]//p')
        item.textify('ingredients', '//table[@cellpadding="3"]//td')
        reviews = []
        nodes = hdoc.select('//div[@class="pr-review-wrap"]')
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//p[@class="pr-review-author-name"]//span'))
            details['reviewer_location'] = textify(node.select('.//p[@class="pr-review-author-location"]//span'))
            details['reviewer_description'] = textify(node.select('.//p[@class="pr-review-author-affinities"]//span'))
            details['revw_rating'] = textify(node.select('.//span[@class="pr-rating pr-rounded"]'))
            details['revw_headline'] = textify(node.select('.//p[@class="pr-review-rating-headline"]'))
            details['revw_description'] = textify(node.select('.//div[@class="pr-review-text"]//p'))
            details['bottom_line'] = textify(node.select('.//div[@class="pr-review-footer"]//div//p'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
