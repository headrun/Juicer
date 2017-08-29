from juicer.utils import *

class Spider(JuicerSpider):
    name = 'paulweiss'
    allowed_domains = ['paulweiss.com']
    start_urls = ['http://www.paulweiss.com/lawyers/']

    def parse(self, response):
        hdoc = HTML(response)
        for url in hdoc.select('//div[@class="alpha"]/a[contains(@href, "LastName=")]/@href').extract():
            ref_url = "http://www.paulweiss.com/lawyers/%s" % url
            yield Request(ref_url, callback=self.parse_listings)

    def parse_listings(self, response):
        hdoc = HTML(response)
        for url in hdoc.select('//table[@id="list"]//td[@class="list"]//b/ancestor::a/@href').extract():
            ref_url = "http://www.paulweiss.com%s" % url 
            yield Request(ref_url, callback=self.parse_details)

    def parse_details(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        url = response.url
        sk = response.url.split('/')[-2]
        image = hdoc.select('//div[@class="biophoto"]/img/@src').extract()[0]
        title = hdoc.select('//div[@class="bioname"]/text()').extract()[0]
        title = title.replace('\r\n', '')
        title = title.replace('\t', '')
        item.textify('location', '//div[@class="leftcontent"]//a//h3')
        item.textify('email', '//div[@class="email"]//a')
        item.textify('related practices', '//h3[contains(text(), "Related Practices")]//following-sibling::a[1]/text()')
        item.set('image', image)
        item.set('title', title)
        item.set('sk', sk)
        item.set('url', url)
        yield item.process()
