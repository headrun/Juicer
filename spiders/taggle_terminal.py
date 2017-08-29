from juicer.utils import *

class TaggleTerminalSpider(JuicerSpider):
    name = 'taggle_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk)
        image = textify(hdoc.select('//img[@id="coverPhoto"]/@src'))
        warranty = textify(hdoc.select('//div[@class="warranty"]/text()'))
        item.textify('title', '//h1//a')
        item.textify('actualprice', '//span[@class="actualPrice"]')
        item.textify('discountprice', '//span[contains(text(),"Discount")]//following-sibling::span[@class="listPrice"]')
        item.set('warranty', warranty)
        #item.textify('warranty', '//div[@class="warranty"]')
        item.set('image',"http://www.taggle.com" + image)
        item.textify('productdetails','//div[@class="offerDiscr offer-landing"]')
        item.textify('description', '//div[@class="discrContent"]//p/text()[not(contains(string(),"Detailed"))]')
        yield item.process()
