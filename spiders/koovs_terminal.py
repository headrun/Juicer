from juicer.utils import *

class KoovsTerminalSpider(JuicerSpider):
    name = 'koovs_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//div[@class="detail_right_inn"]/h1')
        price = textify(hdoc.select('//div[@class="price fontTahoma13"]/span[@id="ContentMain_lblYourPrice"]'))
        item.set('price', int(price))
        actual_price = textify(hdoc.select('//div[@id="price_details"]//span[@class="fontTahoma14"]/span[@id="ContentMain_lblmrp"]'))
        item.set('actual_price', int(actual_price))
        discount = textify(hdoc.select('//span[@class="fontArial15"]/span[@id="ContentMain_lblShowTagVal"]'))
        item.set('discount', int(discount))

        description = hdoc.select('//div[@class="tabcontent"]//ul//li')
        description = [ textify(d) for d in description ]
        item.set('description', description)

        size = []
        snode = hdoc.select('//div[@class="price detail_custom_text"]//select[@rel="Size"]//option')
        for node in snode:
            size.append(textify(node.select('.')))
        size = size[1:]
        if size:
            item.set('size', size)

        quantity = []
        nodelist = hdoc.select('//select[@id="qty"]//option')
        for node in nodelist:
            quantity.append(textify(node.select('.')))
        quantity = quantity[1:]
        item.set('quantity', quantity)

        rating = textify(hdoc.select('//span[contains(text(), "Ratings")]')).replace('Ratings', '')
        item.set('rating', int(rating))
        image_url = hdoc.select('//a[@title="Thumbnail Image"]//img/@src')
        image_url = [textify(i) for i in image_url]
        item.set('image_url', image_url)

        shoe_size = []
        nodes = hdoc.select('//div[@class="price detail_custom_text"]//select[@rel="Shoe Size"]//option')
        for node in nodes:
            shoe_size.append(textify(node.select('.')))
        shoe_size = shoe_size[1:]
        if shoe_size:
            item.set('shoe_size', shoe_size)

        color = []
        cnode = hdoc.select('//div[@class="price detail_custom_text"]//select[@rel="Color"]//option')
        for node in cnode:
            color.append(textify(node.select('.')))
        color = color[1:]
        if color:
            item.set('color', color)

        memory = []
        mnode = hdoc.select('//div[@class="price detail_custom_text"]//select[@rel="Memory"]//option')
        for node in mnode:
            memory.append(textify(node.select('.')))
        memory = memory[1:]
        if memory:
            item.set('memory', memory)

        yield item.process()
