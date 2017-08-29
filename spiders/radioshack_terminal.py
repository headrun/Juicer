from juicer.utils import *

class RadioshackTerminalSpider(JuicerSpider):
    name = 'radioshack_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('Id=')[-1]
        sk= sk.split('&filterName=')[0]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="title fn"]')
        item.textify('model', '//h2[@class="model"]')
        item.textify('catalog_number', '//span[@class="catalog number"]')
        item.textify('price', '//div[@class="product-price-tag"]//span[@class="price"]')
        item.textify('regular_price', '//div[@class="product-price-tag"]//dl[@class="price"]//dt[contains(text(),"Reg:")]//following-sibling::dd[1]')
        item.textify('saving', '//div[@class="product-price-tag"]//dd[@class="red"]')
        valid_date = textify(hdoc.select('//div[@class="product-price-tag"]//div[@class="sale-term"]')).split(':')[-1]
        item.set('valid_date', valid_date)
        availability = textify(hdoc.select('//span[@class="instock"]')) or textify(hdoc.select('//div[@class="instock"]'))
        item.set('availability', availability)
        item.textify('description', '//div[@id="left-col"]//p')
        item.textify('desc_point', '//div[@id="left-col"]//ul//li')
        item.textify('disclaimer_note', '//div[@class="disclaimerCopy"]')
        phone = textify(hdoc.select('//div[@id="right-col"]/text()')).split('By phone:')[-1]
        item.set('phone', phone)
        item.textify('warranty', '//div[@id="right-col"]//ul//li')
        item.textify('review_rating', '//span[@class="pr-rating pr-rounded average"]')
        item.textify('review_count', '//p[@class="pr-snapshot-average-based-on-text"]//span')
        item.textify('recommended', '//p[@class="pr-snapshot-consensus-value pr-rounded"]')
        nodes = hdoc.select('//div[@class="pr-review-wrap"]')
        reviews = []
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//p[@class="pr-review-author-name"]//span'))
            details['reviewer_location'] = textify(node.select('.//p[@class="pr-review-author-location"]//span'))
            details['reviewer_affinities'] = textify(node.select('.//p[@class="pr-review-author-affinities"]//span'))
            details['reviewer_rating'] = textify(node.select('.//span[@class="pr-rating pr-rounded"]'))
            details['revw_title'] = textify(node.select('.//p[@class="pr-review-rating-headline"]'))
            details['revw_comment'] = textify(node.select('.//p[@class="pr-comments"]'))
            details['bottom_line'] = textify(node.select('.//div[@class="pr-review-bottom-line-wrapper"]//p'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
