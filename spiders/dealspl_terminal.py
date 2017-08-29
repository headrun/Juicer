from juicer.utils import *

class TerminalSpider(JuicerSpider):
    name = 'dealspl_terminal'
    allow_domain = ['dealspl.us']

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk) 
        got_page(self.name, response)
        title = xcode(textify(hdoc.select('//h1[@class="deal-title"]')))
        item.set('title',title)
        list_price = textify(hdoc.select('//span[@class="DealListPrice"]')).replace('$', '') 
        item.set('list_price',list_price)
        deal_price = textify(hdoc.select('//span[@class="nprice-g"]')).replace('$', '') 
        item.set('deal_price', deal_price)
        shipping = textify(hdoc.select('//span[@class="DealPriceShipping"]'))
        item.set('shipping',shipping)
        desc = textify(hdoc.select('//td[@colspan="2"]'))
        item.set('desc',desc)
        image = textify(hdoc.select('//td[@class="dLeft"]//img[@class="img-scaling"]/@src'))
        item.set('image',image)

        yield item.process()

