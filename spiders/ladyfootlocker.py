from juicer.utils import *

class LadyfootlockerBrowseSpider(JuicerSpider):
    name = 'ladyfootlocker_browse'
    allowed_domains = ['ladyfootlocker.com']
    start_urls = 'http://www.ladyfootlocker.com/sitemap/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//li[@class="sub_item"]//a/@href', '//a[contains(text(),"Next")]/@href'], response)

        for url in urls: 
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//ul//li//a[@class="quickviewEnabled"]/@href', response)
        for url in terminal_urls:
            get_page('ladyfootlocker_terminal', url)

class LadyfootlockerTerminalSpider(JuicerSpider):
    name = 'ladyfootlocker_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('model--')[1]
        sk = sk.split('/')[0]
        item.set('sk', sk) 
        item.textify('title', '//div[@id="pdp_info"]//h1')
        item.textify('price', '//p[@id="pdp_priceRange"]')
        item.textify('selectedstyle', '//span[@id="productAttributes"]')
        item.textify('size', '//div[@id="pdp_sizeAvailableWrapper"]//following-sibling::ul//li//a')
        item.textify('productsku', '//span[@id="productSKU"]')
        item.textify('description', '//table[@class="product_description"]')
        item.textify('image', '//a[@id="productImage"]//img/@src')
        item.textify('primarycategory', '//div[@class="breadCrumb"]')

        yield item.process()
        got_page(self.name, response)

