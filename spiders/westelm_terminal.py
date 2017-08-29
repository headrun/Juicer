from juicer.utils import *

class WestelmTerminalSpider(JuicerSpider):
    name = 'westelm_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('/')[-2]
        sk = sk.split('-')[-1]
        item.set('sk',sk)
        title = textify(hdoc.select('//h1')).split('\n')[0]
        item.set('title', title)
        item.textify('image', '//div[@class="hero-image"]//a/img/@src')
        description = xcode(textify(hdoc.select('//div[@class="scroll-contents"]//p')))
        item.set('description', description)
        dimensions = textify(hdoc.select('//div[@class="scroll-contents"]//p'))
        item.set('dimensions', dimensions)
        item.textify('primarycategory','//ul[@id="breadcrumb-list"]//li[1]//a')
        item.textify('secondarycategory','//ul[@id="breadcrumb-list"]//li[2]//a')
        item.textify('tertiarycategory','//ul[@id="breadcrumb-list"]//li[3]//a')
        price = textify(hdoc.select('//span[@class="price-state price-standard"]//span[@class="price-amount"]')).split(' ')[0]
        item.set('price', price)
        yield item.process()
        got_page(self.name, response)
