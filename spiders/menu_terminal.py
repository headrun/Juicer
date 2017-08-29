from juicer.utils import *

class MenuTerminalSpider(JuicerSpider):
    name = 'menu_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk) 
        got_page(self.name, response)
        title = textify(hdoc.select('//h2[@class="fn org"]'))
        item.set('title',title)
        category = textify(hdoc.select('//li[@class="cuisine category"]')).split(', ')
        item.set('category',category)
        street_address = textify(hdoc.select('//span[@class="addr street-address"]'))
        restaurant_city = textify(hdoc.select('//span[@class="locality"]'))
        restaurant_state = textify(hdoc.select('//span[@class="region hide-microformat"]'))
        zip_code = textify(hdoc.select('//span[@class="postal-code"]'))
        item.set('street_address',street_address)
        item.set('city',restaurant_city)
        item.set('state',restaurant_state)
        item.set('zip_code', zip_code)
        phone = textify(hdoc.select('//div[@class="phone"]//ul//li')).split(':')[-1]
        item.set('phone_number',phone)
        food_rating = textify(hdoc.select('//th[@class="food-rating"]//span'))
        if food_rating:
            item.set('food_rating', float(food_rating))
        value_rating = textify(hdoc.select('//th[@class="value-rating"]//span'))
        if value_rating:
            item.set('value_rating',float(value_rating))
        service_rating = textify(hdoc.select('//th[@class="service-rating"]//span'))
        if service_rating:
            item.set('service_rating', float(service_rating))
        atmosphere_rating = textify(hdoc.select('//th[@class="atmosphere-rating"]//span'))
        if atmosphere_rating:
                   item.set('atmosphere_rating', float(atmosphere_rating))

        information = {}
        information['more_num']= textify(hdoc.select('//dd[@class="value"]'))
        information['website'] = textify(hdoc.select('//dd//a[@class="note"]//@href'))
        information['notes']= textify(hdoc.select('//dl[@class="notes"]//span')).split(', ')
        hours = textify(hdoc.select('//dl[@class="hours"]//dd//span')).split('m ')
        hours = 'm ,'.join(hours)
        hours = hours.split(' ,')
        information['hours'] = hours
        information['serves']= textify(hdoc.select('//dl[@class="serves"]//dd')).replace('\r\n\t\t\t\t', '').split(',     ')
        information['features']= textify(hdoc.select('//dl[@class="features"]//dd')).replace('\r\n\t\t\t\t', '').split(',     ')
        item.set('information', information)
        yield item.process()


