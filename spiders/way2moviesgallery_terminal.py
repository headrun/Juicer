from juicer.utils import *

class Way2MoviesGalleryTerminalSpider(JuicerSpider):
    name = 'way2moviesgallery_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        if 'id=' and 'page=' in get_request_url(response):
            sk1 = get_request_url(response).split('id=')[-1].split('&')[0]
            sk2 = get_request_url(response).split('page=')[-1]
            sk = sk1 + '/' + sk2

        elif 'cat=' in get_request_url(response):
            sk = get_request_url(response).split('cat=')[-1].split('&')[0]

        elif 'cat=' and 'page=' in get_request_url(response):
            sk3 = get_request_url(response).split('cat=')[-1].split('&')[0]
            sk4 = get_request_url(response).split('page=')[-1]

            sk = sk3 + '/' + sk4

        else:
            sk = get_request_url(response).split('/')[-1].split('.html')[0].split('-')[-1]

        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//div[@style]//h2/text()[not(contains(., "Audio/Event Videos"))]'))).replace("\u2013", "") 
        item.set('title',title)

        images = []
        nodelist = hdoc.select('//div[contains(@class, "_thumb")]//a//img')
        for node in nodelist:
            image_url = textify(node.select('./@src')).split('-')[:-1]
            if 'Radio-Mirchi-' in image_url:
                image_url = '-'.join(image_url) + '.JPG'
                images.append(image_url)
            elif '.png' in image_url:
                image_url = '-'.join(image_url) + '.png'
                images.append(image_url)
            else:
                image_url = '-'.join(image_url) + '.jpg'
                images.append(image_url)

        next_url = textify(hdoc.select('//div[@class="navigation"]//a[contains(.,"next")]/@href'))
        if next_url:
            get_page(self.name, next_url)

        item.set('images', images)

        yield item.process()
