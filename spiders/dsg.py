from juicer.utils import *

class DickssportinggoodsBrowseSpider(JuicerSpider):
    name = 'dsg_browse'
    allowed_domains = ['dickssportinggoods.com']
    start_urls = 'http://www.dickssportinggoods.com/home/index.jsp'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[@class="mainNavLink"]/@href',\
                                 '//ul[@id="leftNavUL"]//li//a[@class="leftnavlink"]/@href',\
                                 '//img//parent::a[@class="results"]/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//h2[@class="prodtitle"]//a/@href', response)
        for url in terminal_urls:
            get_page('dsg_terminal', url)

class DickssportinggoodsTerminalSpider(JuicerSpider):
    name = 'dsg_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('productId=')[1]
        sk = sk.split('&cp=')[0]
        item.set('sk', sk) 
        price = textify(hdoc.select('//div[@class="op"]/text()')).replace('Price:', '')
        yousaveprice = textify(hdoc.select('//span[@class="youSave"]/text()')).replace('You save:', '')
        availability = textify(hdoc.select('//div[@class="availability"]/text()')).replace('Availability:', '')
        item_number = textify(hdoc.select('//span[@class="printBlock"]/text()')).split('Number')[-1]
        item_number = item_number.split(':')[-1]
        item.textify('title', '//h1[@class="productHeading"]')
        item.set('item_number', item_number)
        item.set('price', price)
        item.set('yousaveprice', yousaveprice)
        item.set('availability', availability)
        item.textify('shippinginfo', '//div[@id="shippingInfo"]//span')
        item.textify('productinfo', '//fieldset[@id="FieldsetProductInfo"]')
        item.textify('image', '//div[@id="galImg"]//a//img/@src')
        item.textify('primarycategory','//div[@id="crumbs"]//a[2]')
        item.textify('secondarycategory','//div[@id="crumbs"]//a[3]')

        yield item.process()
        got_page(self.name, response)



