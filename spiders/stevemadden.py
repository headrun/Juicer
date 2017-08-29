from juicer.utils import *

class StevemaddenBrowseSpider(JuicerSpider):
    name = 'stevemadden_browse'
    allowed_domains = ['stevemadden.com']
    start_urls = 'http://www.stevemadden.com/sitemap.aspx'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//a[@class="siteMapLink"]/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//a[@class="itemImageContainer"]/@href', response)
        for url in terminal_urls:
            sk = url.split('id=')[1]
            get_page('stevemadden_terminal', url)

class StevemaddenTerminalSpider(JuicerSpider):
    name = 'stevemadden_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('id=')[1]
        item.set('sk', sk) 
        image = textify(hdoc.select('//a[@class="thumb-view view-Nav selected"]//img[@class="view-image-thumb-nonflash"]/@src'))
        item.textify('title', '//h1')
        item.textify('item-original-price', '//div[@class="item-price-wrapper"]//span[@class="item-original-price"]')
        item.textify('item-price', '//div[@class="item-price-wrapper"]//span[@class="item-price"]')
        item.textify('description', '//div[@id="description"]')
        color = []
        nodes = hdoc.select('//select[@class="item-page-ddl item-style-ddl"]')
        for node in nodes:
            color.append(textify(node.select('.//option')))
        item.set('color', color)
        sizes = []
        nodelist = hdoc.select('//select[@class="item-page-ddl item-size-ddl"]')
        for node in nodelist:
            size = textify(node.select('.//option')).replace('Size: Please select size', '')
            size = size.replace(' ', ',')[1:]
            sizes.append(size)
        item.set('sizes', sizes)
        item.set('image', "http:"+image)

        yield item.process()
        got_page(self.name, response)

