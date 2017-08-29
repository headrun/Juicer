from juicer.utils import *

class EdmundsTerminalSpider(JuicerSpider):
    name = 'edmunds_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        item.textify('msrp', '//p[@class="msrp"]//a')
        item.textify('description', '//div[@class="summary tight-spacing"]//p')
        item.textify('review', '//div[@id="vehicle_review"]//p')
        item.textify('fuel economy', '//div[@class="fuel-economy rule"]/text()')
        item.textify('true cost', '//div[@class="tco rule"]')
        item.textify('image', '//div[@class="info"]//img/@src')
        url = hdoc.select('//div[@class="vehicle "]//p[@class="view-all"]//a/@href')
        yield Request(url, self.parse_details, response, meta={'item': item})

    def parse_details(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        sk = get_request_url(response)
        fs = textify(hdoc.select('//div[@id="mmy_details"]//ul//li'))
        item.set('features/specification', fs)
        yield item.set_many({'sk': sk, 'got_page': True }).process()
