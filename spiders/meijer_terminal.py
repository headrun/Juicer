from juicer.utils import *


class MeijerTerminalSpider(JuicerSpider):
    name = 'meijer_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('R-')[1]
        item.set('sk', sk)
        item.textify('title', '//h1[@id="product-name"]')
        item.textify('image_url', '//div[@id="SP_ProductImage"]//img/@src')
        item.textify('description', '//div[@class="tab_contents"]')
        item.textify('price', '//div[@class="no-sale-price"]/text()[not(contains(string(), "Only:"))]')
        item.textify('availability', '//ul[@class="AvailableList"]//li')
        item.textify('colors', '//p[@class="product_variants_row"]')
        reviews = []
        nodes = hdoc.select('//div[@class="pr-review-wrap"]')
        for node in nodes:
            details = {}
            details['author'] = textify(node.select('.//p[@class="pr-review-author-name"]//span'))
            details['location'] = textify(node.select('.//p[@class="pr-review-author-location"]//span'))
            details['rating'] = textify(node.select('.//span[@class="pr-rating pr-rounded"]'))
            details['comment_title'] = textify(node.select('.//p[@class="pr-comments-header"]/em'))
            details['comment'] = textify(node.select('.//p[@class="pr-comments"]'))
            details['was this a gift'] = textify(node.select('.//li[@class="pr-other-attribute-value"]'))
            details['posted_date'] = textify(node.select('.//div[@class="pr-review-author-date pr-rounded"]'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
        got_page(self.name, response)
