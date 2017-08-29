from juicer.utils import *

class TimesdealTerminalSpider(JuicerSpider):
    name = 'timesdeal_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        title =  xcode(textify(hdoc.select('//figcaption//h1/text()'))).replace('\u2019', '')
        item.set('title', title)

        actual_price = textify(hdoc.select('//div[@class="priceInfo"]//p[@class="orgPrice"]/text()')).strip()
        if actual_price:
            item.set('actual_price', int(actual_price))

        price = textify(hdoc.select('//div[@class="priceInfo"]//p[@class="youpay"]/text()')).strip()
        if price:
            item.set('price', int(price ))

        saving_amount = textify(hdoc.select('//div[@class="priceInfo"]//p[@class="yousave"]/text()')).strip()
        if saving_amount:
            item.set('saving_amount', int(saving_amount))

        discount = textify(hdoc.select('//span[@class="discoutB"]/text()')).strip()
        discount = discount.replace('%', '')
        if discount:
            item.set('discount', int(discount))

        advance_amount = textify(hdoc.select('//span[@class="price"]/text()')).strip()
        if advance_amount:
            item.set('advance_amount', int(advance_amount ))

        image_url = textify(hdoc.select('//div[@class="detailpage"]//img/@src'))
        item.set('image_url', image_url)

        address = textify(hdoc.select('//div[@class="address"]/text()')).strip()
        item.set('address', address)

        phone = textify(hdoc.select('//div[@class="address"]//b[contains(text(), "Phone")]/text()')).replace('Phone : ', '').strip()
        item.set('phone', phone)

        time = textify(hdoc.select('//div[@class="address"]//b[contains(text(), "Time")]/text()')).replace('Time : ', '').strip()
        item.set('time', time)

        email = textify(hdoc.select('//div[@class="address"]//b[contains(text(), "Email")]/text()')).replace('Email : ', '').strip()
        item.set('email', email)

        descripton = hdoc.select('//div[@id="mcs_container"]//ul[@id="content"]//li//text()')
        descripton = [textify(d).strip() for d in descripton]
        item.set('descripton', descripton)

        highlights = hdoc.select('//div[@id="mcs_container_1"]//ul[@id="content"]//li/text()')
        highlights = [textify(h).strip() for h in highlights]
        item.set('highlights', highlights)

        merchants_info = xcode(textify(hdoc.select('//div[@class="txtFull"]//p[contains(@id, "lessDesc")]/text()'))).replace('\u2019', '').strip()
        item.set('merchants_info', merchants_info)

        yield item.process()
