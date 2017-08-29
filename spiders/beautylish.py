from juicer.utils import *

class BeautylishBrowseSpider(JuicerSpider):
    name = 'beautylish_browse'
    allowed_domains = ['beautylish.com']
    start_urls = 'http://www.beautylish.com'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        urls = hdoc.select_urls(['//div[@id="nav"]//ul//li[@class="lava"][1]//a[@class="nav"]/@href', '//div[@class="grid_2"]//ul//li//a/@href'], response)

        for url in urls:
            get_page(self.name, url)

        terminal_urls = hdoc.select_urls('//div[@class="gridwrap_10"]//ul[@class="body"]//li//a/@href', response)
        for url in terminal_urls:
            get_page('beautylish_terminal', url)

class BeautylishTerminalSpider(JuicerSpider):
    name = 'beautylish_terminal'


    def parse(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk) 
        item.textify('title', '//h1[@class="h1"]')
        item.textify('image', '//img[@id="product-image"]/@src')
        product = textify(hdoc.select('//span[@id="tags"]//div//a')).replace('Done Editing', '')
        item.set('product', product)
        item.textify('description', '//div[@class="inner "]//p')
        likes = textify(hdoc.select('//div[@class="inlineblock"]//a')).split('\n')[0]
        item.set('likes', likes)
        data = []
        nodes = hdoc.select('//div[@class="body media mb0"]')
        for node in nodes:
            details = {}
            details['username'] = textify(node.select('.//a[@class="fn fwb url"]'))
            details['userimage'] = textify(node.select('.//span[@class="img"]//a//img/@src'))
            details['reviewtitle'] = textify(node.select('.//div[@class="meta meta_title neutral"]'))
            details['reviewdate'] = textify(node.select('.//li[@class="meta neutral"]'))
            details['reviewdescription'] = textify(node.select('.//p'))
            data.append(details)
        item.set('data', data)
        yield item.process()
        revw_next = hdoc.select('//a[contains(text(),"next")]/@href')
        yield Request(revw_next, self.parse_reviews, response, meta={'data':data, 'item':item})

    def parse_reviews(self, response):
        hdoc = HTML(response)

        item = Item(response, HTML)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk) 
        data = response.meta.get('data')
        item = response.meta.get('item')
        nodes = hdoc.select('//div[@class="body media mb0"]')
        for node in nodes:
            details = {}
            details['username'] = textify(node.select('.//a[@class="fn fwb url"]'))
            details['reviewtitle'] = textify(node.select('.//div[@class="meta meta_title neutral"]'))
            details['userimage'] = textify(node.select('.//span[@class="img"]//a//img/@src'))
            details['reviewdate'] = textify(node.select('.//li[@class="meta neutral"]'))
            details['reviewdescription'] = textify(node.select('.//p'))
            data.append(details)
        revw_next = hdoc.select('//a[contains(text(),"next")]/@href')
        if revw_next:
            yield Request(revw_next, self.parse_reviews, response, meta={'data':data, 'item':item})
        else:
            item.set('data', data)
            yield item.process()
            got_page(self.name, response)

