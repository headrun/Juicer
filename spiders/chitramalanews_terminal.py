
from juicer.utils import *

class ChitramalaNewsTerminalSpider(JuicerSpider):
        name = 'chitramalanews_terminal'

        def parse(self, response):
           hdoc = HTML(response)
           item = Item(response, HTML)
           got_page(self.name, response)
           sk = get_request_url(response).split('-')[-1].split('.html')[-2]
           #item.set('sk', sk)

           title = xcode(textify(hdoc.select('//div[@class="in_headline_title"]//h2/text()'))).replace("\u2022", "") 
           #item.set('title',title)

           published_date = xcode(textify(hdoc.select('//div/small/text()'))).replace("\u2022", "")
           #item.set('published_date', published_date)

           image_url = textify(hdoc.select('//div[@class="atv_img"]/img/@src'))
           if image_url:
                image_url = 'http://www.chitramala.in/' +  image_url
                #item.set('image_url', image_url)

           description1 = xcode(textify(hdoc.select('//span[@class="Main_Description_Style"]/text()')))
           description2 = xcode(textify(hdoc.select('//span[@class="Main_Description_Style"]//p/text()')) or textify(hdoc.select('//div[@class="main_content"]//p/text()')))
           description = description1 + description2
           if description:
                item.set('description', description)
                item.set('image_url', image_url)
                item.set('published_date', published_date)
                item.set('title',title)
                item.set('sk', sk)

           yield item.process() 

