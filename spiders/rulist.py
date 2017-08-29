from juicer.utils import *

class Spider(JuicerSpider):
    name = 'rulist'
    start_urls = ['http://www.rulist.com/index.php?lang=0']

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        yield Request(hdoc.select('//p[@class="category"]/a[1]/@href[contains(., "sub.php")]'), self.parse_sub, response)

    def parse_sub(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[contains(@href, "list.php")][1]/@href'), self.parse_listing, response)

    def parse_listing(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[contains(@href, "details.php")]/@href'), self.parse_details, response)
        #yield Request(hxs.select('//a[contains(@href, "list.php")]/@href'), self.parse_listing, response)

    def parse_details(self, response):
        item = Item(response, HTML)
        hdoc = HTML(response)
        item.textify('title', '//span[@class="company"]/text()')
        address = xcode(textify(hdoc.select('//span[@class="address"][1]/text()')))
        item.set('address', address)
        item.textify('phone', '//span[@class="address" and contains(text(), "Phone")]/text()', lambda x: x.split('Phone:', 1)[-1].strip())
        item.textify('email', '//span[@class="address" and contains(text(), "Send E-mail")]/@href', lambda x: x.split('mailto:', 1)[-1].strip().split('?')[0])
        item.textify('website', '//span[@class="address" and contains(text(), "Web Site")]/text()', lambda x: x.split('Web Site:', 1)[-1].strip())
        item.textify('category', '//div[@class="internal"]/a[@class="nav"]/text()')
        sk = response.url.split('?')[-1]
        sk = sk.split('=')[-1]
        item.set('sk', sk)
        yield item.process()
