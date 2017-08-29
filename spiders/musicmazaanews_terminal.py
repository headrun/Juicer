
from juicer.utils import *

class MusicMazaaNewsTerminalSpider(JuicerSpider):
        name = 'musicmazaanews_terminal'

        def parse(self, response):
           hdoc = HTML(response)
           item = Item(response, HTML)
           got_page(self.name, response)

           title = xcode(textify(hdoc.select('//div[@class="newsTitle"]/h1/text()'))).replace("\u2022", "")
           #item.set('title',title)

           published_date = xcode(textify(hdoc.select('//div[@class="newsTitle"]/div/text()[1]'))).replace("\xe2\x80\xa2", "").replace("\u2022", "").replace("Posted on", "").replace(" ", "")
           #item.set('published_date', published_date)

           image_url = textify(hdoc.select('//div[@class="newsDesc"]/img/@src'))
           if '.com' in image_url:
                image_url = image_url.split('.com/')[1]
                image_url = "http://images.musicmazaa.com/" + image_url
           else:
                image_url = "http://musicmazaa.com" + image_url
           #item.set('image_url', image_url)

           description = xcode(textify(hdoc.select('//div[@class="newsDesc"]//p/text()')))
           if description:
                item.set('description', description)
                item.set('image_url', image_url)
                item.set('published_date', published_date)
                item.set('title',title)


           yield item.process()

