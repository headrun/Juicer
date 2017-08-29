from juicer.utils import *
import MySQLdb

class Wiki_Malay(JuicerSpider):
    name = 'cities_states_usa'
    #start_urls = ['http://en.wikipedia.org/wiki/List_of_United_States_cities_by_area']
    #start_urls = ['http://en.wikipedia.org/wiki/Lists_of_populated_places_in_the_United_States']
    #start_urls = ['http://www.usa.gov/Agencies/Local-Government/Cities.shtml']
    start_urls = ['http://www.citytowninfo.com/places']

    def parse(self, response):
        hdoc = HTML(response)

        city_urls = hdoc.select('//div[@class="profile"]//tr/td[1]/a/@href')
        for city_url in city_urls:
            yield Request(city_url, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        cities = hdoc.select('//div[@id="cities_and_towns"]//tr/td/a//text()')
        print len(cities)
        _cities = []
        [_cities.extend(textify(i).split(',')) for i in cities]
        print len(_cities)
        _cities = list(set([city.strip().lower() for city in _cities]))
        print len(_cities)

        for city in _cities:
            city = city.replace(' ', '+').lower()
            state = ''
            country = 'usa'

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=US&loc1=%s&loc2=%s' %(state,city)
            #print 'location>>', city, state, url

            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
            conn.set_character_set('utf8')
            cursor = conn.cursor()

            try:

                query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(country),str(state),str(city), str(url))
                cursor.execute(query,values)

            except: pass
            cursor.close()
