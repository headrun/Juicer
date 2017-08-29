from juicer.utils import *
import MySQLdb

class Wiki_Malay(JuicerSpider):
    name = 'cities_states_malaysia'
    #start_urls = ['http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Malaysia_by_population']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_capitals_in_Malaysia']

    def parse(self, response):
        hdoc = HTML(response)

        cities = hdoc.select('//div[@id="mw-content-text"]//tr/td/a')
        print len(cities)
        for i in cities:
            city = textify(i.select('./text()'))  #for travelmath split(',') is required
            city = city.replace(' ', '+').lower()
            state = ''
            country = 'malaysia'

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=MY&loc1=%s&loc2=%s' %(state,city)
            print 'location>>', city, state, url

            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
            conn.set_character_set('utf8')
            cursor = conn.cursor()


            query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            values = (str(country),str(state),str(city), str(url))
            cursor.execute(query,values)

            cursor.close()
