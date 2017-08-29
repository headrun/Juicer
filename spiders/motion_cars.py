
#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from juicer.utils import *
class MotorCars(JuicerSpider):
    name = 'motioncars'
    start_urls = ['http://motioncars.inquirer.net/category/autobuzz', 'http://motioncars.inquirer.net/category/drives', 'http://motioncars.inquirer.net/category/features', 'http://motioncars.inquirer.net/category/classifieds', 'http://motioncars.inquirer.net/category/motorsports', 'http://motioncars.inquirer.net/category/columns']
    def parse(self, response):
        hxs  = HtmlXPathSelector(response)
        links = hxs.select('//div[@class="post"]/h1/a/@href').extract()
        for link in links:
                yield Request(link, callback=self.parse_car)
        next_page_link = hxs.select('//div[@class="navigation"]/a[contains(text(),"Next Page")]/@href').extract()[0]
        if next_page_link:
                yield Request(next_page_link, callback=self.parse)
                print "next_page_link", next_page_link
    def parse_car(self, response):
        hxs = HtmlXPathSelector(response)
        title = textify(hxs.select('//div[@id="article_title"]//h1/text()'))
        date = hxs.select('//div[@class="postDate"]//text()').extract()[0]
        date = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
        data = hxs.select('//div[@id="pp_entry"]/p//text()').extract()
        data = " ".join(data)

        author = textify(hxs.select('//dv[@id="article_title"]//h2//a[@href="http://motioncars.inquirer.net/byline/jason-k-ang"]/text()'))

        item = Item(response)
        item.set('title', title)
        item.set('text', data)
        item.set('author.name', author)
        item.set('dt_added', date)
        item.set('url', response.url)

        if date>1396596227:
            yield item.process()
