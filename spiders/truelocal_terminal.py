from juicer.utils import *

class TruelocalTerminalSpider(JuicerSpider):
    name = 'truelocal_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk',sk)
        item.textify('title', '//div[@id="business-quick-info"]//h1')
        item.textify('street', '//li[@id="business-address"]//strong')
        item.textify('address', '//li[@id="business-address"]/text()')
        item.textify('phoneno', '//strong//span[@class="tl-phone-full"]')
        item.textify('faxno', '//span[@class="tl-phone-full"]')
        description = textify(hdoc.select('//div[@id="business-summary"]//pre')).replace('\r\n', '')
        item.set('description', description)
        review_no = textify(hdoc.select('//a[@href="#reviews"]/text()')).replace('REVIEWS', '')
        item.set('review_no', review_no)
        yield item.process()
