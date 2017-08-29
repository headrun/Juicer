from juicer.utils import *

class BulbsolutionsBrowseSpider(JuicerSpider):
    name = 'bulbsolutions_browse'
    allowed_domains = ['bulbsolutions.com']
    start_urls = 'http://www.bulbsolutions.com/pindex.asp'
    limit_start_urls = 2000

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//td[contains(text(),"Page:")]//a/@href'], response)
        for url in urls:
            get_page(self.name, url)

        urls = hdoc.select_urls('//div[@id="content"]//table[2]//td//a/@href', response)
        for url in urls:
            get_page('bulbsolutions_terminal', url)

class BulbsolutionsTerminalSpider(JuicerSpider):
    name = 'bulbsolutions_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response)
        item.set('sk', sk)
        saleprice  = textify(hdoc.select('//font[contains(text(),"Sale")]/text()')).split(' ')[-1]
        yousave  = textify(hdoc.select('//font[@class="productnamecolor colors_productname"]')).replace('You save',' ')
        item.textify('title', '//font[@class="productnamecolorLARGE colors_productname"]')
        item.set('saleprice', saleprice)
        item.set('yousave', yousave)
        item.textify('ourprice','//font[@class="text colors_text"]//b[contains(text(), "Our")]//parent::font//parent::font/text()')
        item.textify('description', ('//div[@id="ProductDetail_ProductDetails_div"]//div[1]', '//div[@id="ProductDetail_ProductDetails_div"]'))
        warranty = textify(hdoc.select('//div[@id="ProductDetail_TechSpecs_div"]//ul//li')).replace('Warranty', '')
        item.set('warranty', warranty)
        item.textify('productcode','//span[@class="product_code"]')
        item.textify('primarycategory','//td[@class="vCSS_breadcrumb_td"]//a[2]')
        item.textify('secondarycategory','//td[@class="vCSS_breadcrumb_td"]//a[3]')

        yield item.process()
        got_page(self.name, response)
