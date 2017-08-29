from juicer.utils import *

class ToptableTerminalSpider(JuicerSpider):
    name = 'toptable_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('id=')[1]
        title = textify(hdoc.select('//h1[@itemprop="name"]')) or textify(hdoc.select('//span[@itemprop="name"]'))
        item.set('title', title)
        item.textify('address', '//p[@itemprop="address"]//span')
        item.textify('image', '//div[@class="media-area"]//img/@src')
        overall_rating = textify(hdoc.select('//div[@class="col-50"]//li[@class="primary"]//span')).split('overall rating:')[-1]
        no_of_rating = textify(hdoc.select('//li[@class="small-text"]')).split('based on ')[-1]
        item.textify('description', '//div[@class="inner expander-content"]//p')
        item.textify('checklist', '//div[@class="inner expander-content"]//ul[@class="check-list"]//li')
        item.textify('cuisine', '//tr//th[contains(text(),"cuisine:")]//following-sibling::td')
        item.textify('price', '//tr//th[contains(text(),"price:")]//following-sibling::td')
        item.textify('opening times', '//tr//th[contains(text(),"opening times:")]//following-sibling::td//div')
        item.textify('dress code', '//tr//th[contains(text(),"dress code:")]//following-sibling::td')
        item.set('overall_rating', overall_rating)
        item.set('no_of_rating', no_of_rating)
        item.set('sk', sk)
        nodes = hdoc.select('//div[@class="container border-bottom"]')
        reviews = []
        for node in nodes:
            details = {}
            details['reviewer'] = textify(node.select('.//h4//a//span[not(contains(text(),":"))]'))
            details['rev_desc'] = textify(node.select('.//div[@class="inner-vertical"]//p'))
            details['ovr_rtng'] = textify(node.select('.//div[@class="inner-vertical"]//li[@class="primary"]//span'))
            reviews.append(details)
        item.set('reviews', reviews)
        yield item.process()
