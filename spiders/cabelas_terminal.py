from juicer.utils import *

class CabelasTerminalSpider(JuicerSpider):
    name = 'cabelas_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.textify('product_heading','//div[@class="labledContainer"]//h1')
        item.textify('product_description','//div[@class="left"]//div[@id="description"]')
        item.textify('item number','//span[@class="itemNumber"]/text()[not(contains(string(), "Item:"))]')
        regular_price = textify(hdoc.select('//dd[@class="regular"]')) or textify(hdoc.select('//div[@class="price"]//dd[@class][not(contains(@class, "clr"))]'))
        item.set('regular_price', regular_price)
        item.textify('sales_price', '//dd[@class="sale"]')
        item.textify('currency','//div[@class="content"]//a[@style]')
        item.textify('size','//select[@class="js-dropdown"]//option[contains(text(),"Select SIZE")]//following-sibling::option')
        item.textify('model','//select[@class="js-dropdown"]//option[contains(text(),"Select MODEL")]//following-sibling::option')
        item.textify('color','//select[@class="js-dropdown"]//option[contains(text(),"Select COLOR")]//following-sibling::option')
        yield item.process()
        got_page(self.name, response)
