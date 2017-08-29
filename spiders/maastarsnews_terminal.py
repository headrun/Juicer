
from juicer.utils import *

class MaaStarsNewsTerminalSpider(JuicerSpider):
        name = 'maastarsnews_terminal'

        def parse(self, response):
           hdoc = HTML(response)
           item = Item(response, HTML)
           got_page(self.name, response)
           sk = get_request_url(response).split('/')[-2]
           item.set('sk', sk) 

           title = xcode(textify(hdoc.select('//div[@class="post"]/h1/text()'))).replace("\u2019", "") 
           item.set('title', title)

           published_date = textify(hdoc.select('//span[@class="postDate"]/text()'))
           item.set('published_date', published_date)

           image_url = textify(hdoc.select('//div[@class="entry-content"]//img/@src[not(contains(.,".gif"))]'))
           item.set('image_url', image_url)

           description = xcode(textify(hdoc.select('//div[@class="entry-content"]/p[not(contains(., "Disclaimer"))]/text()'))).replace("0x91", "").replace("0x92", "") 
           item.set('description', description)

           yield item.process()
