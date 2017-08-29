from juicer.utils import * #-> We are importing every module (*->all modules)
from dateutil import parser
import json
import requests
from scrapy.http import FormRequest



class EbelaIndia(JuicerSpider):
    name = 'ebela_in'
    start_urls = ['https://ebela.in/entertainment?ref=hm-Footer','https://ebela.in/sports?ref=hm-Footer','https://ebela.in/state?ref=hm-Footer','https://ebela.in/national?ref=hm-Footer','https://ebela.in/international?ref=hm-Footer','https://ebela.in/business?ref=hm-Footer','https://ebela.in/health?ref=hm-Footer']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        """
        links = hdoc.select('//div[@class="black_conetent_text_large"]/a/@href')
        for link in links:
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="story_topstory_head"]/text()'))
        text = textify(hdoc.select('//div[contains(@class,"story_description")]//text() | //div[@class="story_detail_section"]//text()'))
        date = textify(hdoc.select('//script[@type="application/ld+json"]/text()'))
        date = re.findall('.*datePublished".*',date)[-1]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

        item = ITEM(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))


        """
