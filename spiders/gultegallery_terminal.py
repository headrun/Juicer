from juicer.utils import *

class GulteGalleryTerminalSpider(JuicerSpider):
    name = 'gultegallery_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('photos/')[-1].split('/')[2:]
        sk = '/'.join(sk)
        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//div[@class="title"]//h1/text()'))).replace("\u2013", "")
        item.set('title',title)

        images = []
        nodelist = hdoc.select('//ul[@class="photoGallery med"]//a//img')
        for node in nodelist:
            image_url = textify(node.select('./@src')).replace('/thumb/', '/normal/')
            images.append(image_url)

        next_url = textify(hdoc.select('//li//a[contains(text(), "Next")]/@href'))
        if next_url:
            get_page(self.name, next_url)

        item.set('images', images)

        yield item.process()
