from juicer.utils import *
import MySQLdb

class Wiki(JuicerSpider):
    name = 'cities_states_indonesia'
    #start_urls = ['http://en.wikipedia.org/wiki/List_of_cities_in_the_Philippines']
    #start_urls = ['http://www.travelmath.com/cities-in/Indonesia']
    start_urls = ['http://www.epictrip.com/Cities-in-Thailand-places-l210.html']

    def parse(self, response):
        hdoc = HTML(response)

        #cities = hdoc.select('//div[@id="mw-content-text"]//tr/td[1]/a')
        #cities = hdoc.select('//div[@class="boxmiddle"]//tr/td/a|//div[@class="fullwidth"]//tr/td/a')
        cities = hdoc.select('//div[@id="epicplaces"]/div/a')
        print len(cities)
        for i in cities:
            city = textify(i.select('./text()'))  #for travelmath split(',') is required
            city = city.replace(' ', '+').lower()
            state = ''
            country = 'thailand'

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=TH&loc1=%s&loc2=%s' %(state,city)
            print 'location>>', city, state, url
            try:
                conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
                conn.set_character_set('utf8')
                cursor = conn.cursor()


                query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(country),str(state),str(city), str(url))
                cursor.execute(query,values)

                cursor.close()
            except: pass
