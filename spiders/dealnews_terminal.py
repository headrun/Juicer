from juicer.utils import *

class DealnewsTerminalSpider(JuicerSpider):
    name = 'dealnews_terminal'


    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1].split('.')[0]
        item.set('sk', sk)
        overview = textify(hdoc.select('//a[@class="featured-headline"]/text()')).split('\n\n\n')
        item.set('overview', overview)
        image_url = textify(hdoc.select('//a[@target="_blank"]//img/@src')).split('\n\n\n')[0]
        item.set('image', image_url)
        price = textify(hdoc.select('//div[@class="price"]/text()')).split('$')[-1]
        if '$' in price:
            item.set('price', price)
        elif 'off' in price:
            discount = price.split('%')[0].split(' ')[-1]
            item.set('discount', int(discount))
        else:
            price = ''
            item.set('price', price)
        hotness = textify(hdoc.select('//ul[@class="stats stats-top"]//li//img/@alt')).split(':')[-1].strip()
        hotness = hotness.split(' ')[0]
        hotness = hotness.split('/')[0]
        if hotness:
            item.set('hotness', int(hotness))
        posted_on = textify(hdoc.select('//ul[@class="stats stats-top"]//li//time'))
        item.set('posted_on', posted_on)
        discription = textify(hdoc.select('//div[@class="artbody"]//text()'))
        item.set('discription', discription)
        brand = textify(hdoc.select('//ul[@class="stats"]//li[contains(text(), "Brand")]')).split(':')[-1]
        item.set('brand', brand)
        model_number = textify(hdoc.select('//ul[@class="stats"]//li[contains(text(), "Model Number")]')).split(':')[-1]
        item.set('model_number', model_number)
        yield item.process()
