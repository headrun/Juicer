from juicer.utils import *

class GulteNewsTerminalSpider(JuicerSpider):
        name = 'gultenews_terminal'

        def parse(self, response):
            hdoc = HTML(response)
            item = Item(response, HTML)
            got_page(self.name, response)
            sk = get_request_url(response).split('/')[-2]
            item.set('sk', sk)

            title = textify(hdoc.select('//div[@class="article left"]//h1/text()'))
            item.set('title',title)

            published_date = textify(hdoc.select('//div[@class="article left"]//code/text()'))
            item.set('published_date', published_date)

            #image_urls = []
            #urls = hdoc.select('//div[@class="img"]//img/@src')
            #for url in urls:
            #    image_url = textify(url)
            #    print "image>>>>>>>>>>>>>>>>", image_url
            #    image_urls.append(image_url)

            #image_next = textify(hdoc.select('//a[@id="nextid"]/@href'))
            #if image_next:
            #    print "image_next>>>>>>>>>", image_next
            #    get_page(self.name, image_next)
            #print "image_urls>>>>>>>", image_urls

            image_url = textify(hdoc.select('//div[@class="img"]//img/@src'))
            item.set('image_url', image_url)

            description = xcode(textify(hdoc.select('//div[@class="content"]//p/text()')))
            item.set('description', description)

            yield item.process()
