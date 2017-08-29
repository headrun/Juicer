from juicer.utils import *

class MydalaTerminalSpider(JuicerSpider):
    name = 'mydala_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response)
        item.set('sk', sk)
        title =  textify(hdoc.select('//h1[@class="darkgrey-txt font-bold"]/text()'))
        print "title>>>>>>>>>>>>", title
        item.set('title', title)

        actual_price = textify(hdoc.select('//div[contains(text(), "VALUE")]//parent::div/text()')).split('VALUE')[1].strip()
        print "actual_price>>>>>>>>>>>>", actual_price
        if actual_price:
            item.set('actual_price', int(actual_price))

        discount = textify(hdoc.select('//div[contains(text(), "DISCOUNT")]//parent::div/text()')).split('DISCOUNT')[1].strip()
        discount = discount.replace('%', '')
        print "discount>>>>>>>>>>>>", discount
        if discount:
            item.set('discount', int(discount))

        saving_amount = textify(hdoc.select('//div[contains(text(), "SAVE")]//parent::div/text()')).split('SAVE')[1].strip()
        print "saving_amount>>>>>>>>>>>>", saving_amount
        if saving_amount:
            item.set('saving_amount', int(saving_amount))

        price = textify(hdoc.select('//div[contains(@class, "buy-value pink")]/text()')).strip()
        print "price>>>>>>>>>>>>", price
        if price:
            item.set('price', int(price))

        image_url = hdoc.select('//div[@class="thumbs"]//a//img/@src')
        image_url = [textify(i) for i in image_url]
        item.set('image_url', image_url)

        features = hdoc.select('//div[contains(@class, "highlights-wrapper fltLeft ")]//ul//li/text()')
        features = [textify(i) for i in features]
        print "features>>>>>>>>>>>", features
        item.set('features',features )

        payments = hdoc.select('//div[contains(@class, "text-14 mediumgrey-txt")]/text()')
        payments = [textify(i) for i in payments ]
        print "payments>>>>>>>>>>>", payments
        item.set('payments',payments )

        description = xcode(textify(hdoc.select('//div[@id="tabs-1"]//p/text()'))).replace('\u2022', '')
        print "description>>>>>>>>>>>", description
        item.set('description', description)

        #yield item.process()
