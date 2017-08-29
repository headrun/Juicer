from juicer.utils import *

class PurelandsupplyTerminalSpider(JuicerSpider):
    name = 'purelandsupply_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk',sk)
        item.textify('title', '//h1[@class="ProductNameText"]')
        item.textify('list_price', '//b[contains(text(), "List Price:")]//parent::td/text()')
        sale_price = textify(hdoc.select('//b[contains(text(), "Sale Price:")]')).split(' ')[-1]
        item.set('sale_price', sale_price)
        availability = textify(hdoc.select('//b[contains(text(), "in stock")]')).split('units')[0]
        availability = availability.replace(')', '')
        availability = availability.replace('(', '')
        item.set('availability', availability)
        img_url = textify(hdoc.select('//div[@align="center"]//img/@src')).split('\n\n\n')[0]
        item.set('image_url', img_url)
        description =  textify(hdoc.select('//td[@valign="top"]//div/text()')).strip()
        item.set('description', description)
        yield item.process()
        got_page(self.name, response)
