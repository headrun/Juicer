from juicer.utils import *
import MySQLdb

class Wiki(JuicerSpider):
    name = 'cities_states_thailand'
    start_urls = ['http://worldpopulationreview.com/countries/thailand-population/major-cities-in-thailand/']

    def parse(self, response):
        hdoc = HTML(response)

        rows = hdoc.select('//table[@class="generic rounded sortable"]//td[@class="right"][1]//text()')

        print len(rows)
        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        #c_query = 'select distinct(city) from states_and_cities where country="india"'
        #cursor.execute(c_query)

        #rows = cursor.fetchall()
        #rows = [row[0] for row in rows if row[0]]

        for row in rows:
            #city = textify(row.select('.//a/text()')).strip()
            #state = textify(row.select('./td[2]/a/text()')).strip()
            city = textify(row)
            city  = city.strip().replace(' ','+').strip().lower()
            state = ''
            country = 'thailand'
            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=TH&loc1=%s&loc2=%s' %(state,city)
            #url = 'http://www.blogger.com/profile-find.g?t=l&loc0=IN&loc1=%s' %(state)

            print 'location>>', city, state, url

            query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            state = ''
            values = (str(country),str(state),str(city), str(url))
            cursor.execute(query,values)

        cursor.close()
