from juicer.utils import *

class YipitTerminalSpider(JuicerSpider):
    name = 'yipit_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response)
        item.set('sk', sk)
        item.textify('title', '//h2[@itemprop="name"]')
        item.textify('address', '//p[@itemprop="address"]')
        item.textify('tags', '//span[@class="tag_wrap"]//a')
        item.textify('price', '//div[@class="container first"]//ul//li/text()')
        availability = textify(hdoc.select('//div[@class="formbutton buttonexpired"]')) or textify(hdoc.select('//div[@class="container first"]//ul//li//a'))
        item.set('availability', availability)
        item.textify('actual_price', '//ul[@class="info"]//span[contains(text(),"Worth")]//parent::li/text()')
        item.textify('discount', '//ul[@class="info"]//span[contains(text(),"Discount")]//parent::li/text()')
        item.textify('savings', '//ul[@class="info"]//span[contains(text(),"Savings")]//parent::li/text()')
        item.textify('negotiated_by', '//p[@class="light-gray-small-text"]//a')
        number_of_purchased =  textify(hdoc.select('//ul[@class="purchased"]//li')).replace(' purchased', '')
        item.set('number_of_purchased', number_of_purchased)
        yield item.process()
