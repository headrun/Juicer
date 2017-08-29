from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from juicer.items import JuicerItem
import re

class EWallpapersEuSpider(BaseSpider):
    name = 'ewallpapers.eu'
    allowed_domains = ['ewallpapers.eu']
    start_urls = [
        'http://www.ewallpapers.eu//all/'
    ]
    no_of_pages = 1
    page_count = 0

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        #Start fetching data
        for url in hxs.select('//table[@id="AutoNumber1"]//div[@class="image"]/a/@href').extract():
            yield Request(url, callback=self.parse_terminal)

        self.page_count += 1
        if self.page_count < self.no_of_pages:
            url = hxs.select('//table[@id="nb_text"]//a/@href')[-1].extract()
            yield Request(url, callback=self.parse)

    def parse_terminal(self, response):
        hxs = HtmlXPathSelector(response)
        item = JuicerItem()
        item['sk'] = response.url.split('/')[-1].split('.')[0]
        item['update_mode'] = 'custom'

        data = {}
        data['reference'] = response.url
        description = hxs.select('//table[@id="AutoNumber15"]//td[contains(text(), "Description")]/text()').extract()

        if description:
            description = description[0]
            data['title'] = re.findall('\xa0([^|]*)', description)
            data['description'] = re.findall('[|](.*)', description)

        data['images'] = []

        for image in hxs.select('//table[@id="WPSizeList"]//div//a[contains(text(), "View")]//parent::a/@href').extract():
            data['images'].append(image)

        data['date_added'] = ''
        data['tags'] = ''
        data['popularity'] = ''

        item['data'] = data

        return item

SPIDER = EWallpapersEuSpider()
