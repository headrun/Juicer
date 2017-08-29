from juicer.utils import *

class SnapdealTerminalSpider(JuicerSpider):

    name = 'snapdeal_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        item.set('sk', sk)
        title = textify(hdoc.select('//div[@class="serviceDeal-right"]/div[@class="dealtitle-head"]')) or textify(hdoc.select('//div[@class="prodtitle-head"]'))
        item.set('title', title)
        description =  textify(hdoc.select('//div[@class="dealtitle"]')).replace('\r\n', ' ').strip() or textify(hdoc.select('//p[@class="MsoNormal"]//span/text()')).replace('\r\n', ' ').split('SIZE')[0] or textify(hdoc.select('//dt[@class="deal-detalis-tab-cont"]//p')).replace('\r\n', ' ').strip()
        item.set('description', description)

        features = hdoc.select('//ul[@class="key-features"]//li')
        features = [textify(f) for f in features]
        if features:
            item.set('features', features)

        image_url = textify(hdoc.select('//ul[@class="slides"]/li/img/@src')) or textify(hdoc.select('//li//a[@class="jqzoom"]//img/@src'))
        item.set('image_url', image_url)
        actual_price = textify(hdoc.select('//div[@class="dealbuy-price-outer"]//strike')) or textify(hdoc.select('//span[@id="original-price-id"]'))
        item.set('actual_price', actual_price)
        discount = textify(hdoc.select('//div[@class="dealbuy-price dealbuy-discount"]/span')) or textify(hdoc.select('//div[@class="prodbuy-price prodbuy-discount"]//span'))
        item.set('discount', discount)
        price = textify(hdoc.select('//div[@class="dealbuy-price"]/span')) or textify(hdoc.select('//span[@id="selling-price-id"]'))
        item.set('price', price)

        pay_advance = textify(hdoc.select('//div[@class="payInAdv-outer"]//span[not(contains(text(),"Rs"))]'))
        if pay_advance:
            item.set('pay_advance', pay_advance)

        reasons_to_buy = textify(hdoc.select('//div[@class="deal-reasons-details"]/div[@class="deal-detail-list"]/p'))
        if reasons_to_buy:
            item.set('reasons_to_buy', reasons_to_buy)

        pay_remaining = textify(hdoc.select('//div[@class="pay-remaining"]'))
        if pay_remaining:
            item.set('pay_remaining', pay_remaining)

        fine_print = textify(hdoc.select('//div[@class="deal-terms-details-outer"]/div[@class="deal-detail-list"]/p'))
        if fine_print:
            item.set('fine_print', fine_print)

        yield item.process()
