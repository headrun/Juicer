from juicer.utils import *
import re
from urlparse import urljoin
from datetime import datetime
class HolidayLettingSpider(JuicerSpider):
    name = 'holidayletting'
    allowed_domains = ['holidaylettings.co.uk']
    start_urls = ['http://www.holidaylettings.co.uk/search.asp?']

    def parse(self, response):
        hdoc = HTML(response)
        yield Request(hdoc.select('//a[@class="dpreg"]/@href'), self.parse_location, response)

    def parse_location(self, response):
        hdoc = HTML(response)
        homes = hdoc.select('//table [@class = "srp3"]')
        for home in homes:
            item = Item(response, HTML)
            meta_desc = textify(home.select('.//p[@class = "descrCellPara"]'))
            item.set('meta_description', meta_desc)
            rental_link = home.select('.//a[@class="srp_property_link"]/@href')
            yield Request(rental_link, self.parse_rental, response, meta={'item':item})
        #yield Request(hdoc.select('//a[@class="srp_property_link"]/@href'), self.parse_rental, response)
        yield Request(hdoc.select('//td[@class="button"]/a[contains(img/@src,"arrow_right.png")]/@href'), self.parse_location, response)

    def parse_rental(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        url = response.url
        sk_val = url.split('/')[-1]
        item.set('sk', sk_val)
        item.textify('description', '//h2[string(.)="Home description"]/following-sibling::p[2]/text()')
        item.textify('title', '//h2[@class = "uh"][@id = "home_header"]/text()')
        g_map = textify(hdoc.select('//span[@id="map_reset"]/a/@onclick'))
        lat_long = re.findall("Map\((.*)\);",g_map)
        lat_long = lat_long[0].split(',')
        lat_long = (lat_long[0].strip(),lat_long[1].strip(),lat_long[2].strip())
        item.set('lat_long', lat_long)

        #accommodation
        accommodation = {}
        #summary1
        key_values = hdoc.select('//table[@id = "summary1"]/tr')
        for key_value in key_values:
            key = textify(key_value.select(".//th"))
            if key == 'Review rating:':
                value = textify(key_value.select('//td/a[@title="Write review"]/@href'))
                accommodation[key] = value
            else:
                value = textify(key_value.select('.//td'))
                accommodation[key] = value

        #summary2
        key_values = hdoc.select('//table[@id = "summary2"]/tr')
        for key_values in key_values:
            key = textify(key_value.select(".//th"))
            value = textify(key_value.select('.//td'))

            accommodation[key] = value
        #end of accomodation
        item.set('accommodations',accommodation)

        #amenities
        amenities = [textify(amm) for amm in hdoc.select('//table[@id ="facilities"]/tr')]
        #end of amenities
        item.set('amenities',amenities)

        #rates
        rates=[]
        rows = hdoc.select('//table[@class ="tariff_table"]/tr[contains(@id, "tariff")]')
        for row in rows:
            values = [textify(val) for val in  row.select("./td")]
            start = datetime.strptime(values[1],'%d %b %y')
            end = datetime.strptime(values[2],'%d %b %y')
            cost = values[3].split()[0]
            cost = "GBP "+cost
            #set value here
            rates.append([start,end,cost])
        item.set('rates',rates)

        nodes = hdoc.select('//table[@id="facilities"]//tr')
        facilities = {}
        for node in nodes:
            fkey = textify(node.select('.//th'))
            fvalue = textify(node.select('.//td'))
            facilities[fkey] = fvalue

        item.set('facilities', facilities)
        #meta={'country':country,'sk_val':sk_val,"description":desc,"rental_name":rental_name,"accomodataion":accomodation,"amenities":amenities,"rates":rates}

        image_page_link = textify(hdoc.select('//div[@class = "button"]/a/@href'))
        image_page_link = urljoin("http://www.holidaylettings.co.uk",image_page_link)
        yield Request(image_page_link, self.parse_images, response, meta={'item':item})


    def parse_images(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        pics = hdoc.select('//a[@class = "photo"]/@href')
        photos = [urljoin("http://www.holidaylettings.co.uk",textify(pic)) for pic in pics]
        item.set('photos',photos)
        yield item.process()
