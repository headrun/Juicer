from juicer.utils import *

class NextagtravelTerminalSpider(JuicerSpider):
    name = 'nextagtravel_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-2]
        sk = sk.split('-')[-1]
        item.set('sk', sk)
        item.textify('title', '//span[@id="h-name"]')
        address = textify(hdoc.select('//div[@id="h-location"]')).strip().split(',')[0]
        item.set('address', address)
        city = textify(hdoc.select('//div[@id="h-location"]')).strip().split(',')[1]
        item.set('city', city)
        state = textify(hdoc.select('//div[@id="h-location"]')).strip().split(',')[-2]
        item.set('state', state)
        country = textify(hdoc.select('//div[@id="h-location"]')).strip().split(',')[-1]
        item.set('country', country)
        item.textify('description', '//div[@id="h-description"]//p')
        amenities = xcode(textify(hdoc.select('//div[@id="div_amenities"]//ul//li'))).replace('\xe2\x80\xa2\xc2\xa0\xc2\xa0\xc2\xa0','')
        item.set('amenities', amenities)
        item.textify('images', '//div[@id="div_pictures"]//img/@src')
        yield item.process()
        got_page(self.name, response)
