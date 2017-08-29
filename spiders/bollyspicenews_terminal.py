
from juicer.utils import *

class BollySpiceNewsTerminalSpider(JuicerSpider):
        name = 'bollyspicenews_terminal'

        def parse(self, response):
            hdoc = HTML(response)
            item = Item(response, HTML)
            got_page(self.name, response)
            sk = get_request_url(response).split('/')[-2]
            item.set('sk', sk) 

            title = textify(hdoc.select('//h1[@class="singletitle"]//text()'))
            item.set('title', title)

            published_date = textify(hdoc.select('//div[@class="right"]/text()[contains(.,"Posted")]')).replace("Posted on in ", "")
            published_date = parse_date(published_date)
            item.set('published_date', published_date)

            image_url = []
            image_url = textify(hdoc.select('//div[@class="hnboxnewssingle"]//p//img/@src'))
            item.set('image_url', image_url)

            description = textify(hdoc.select('//div[@class="hnboxnewssingle"]//p//text()'))
            item.set('description',description)

            yield item.process()

