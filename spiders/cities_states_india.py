from juicer.utils import *
import MySQLdb

class Wiki(JuicerSpider):
    name = 'cities_states_india'
    start_urls = ['http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_India']

    def parse(self, response):
        hdoc = HTML(response)

        rows = hdoc.select('//table[contains(@class,"wikitable sortable")]//tr\
                //a[contains(@href,"/wiki/")]/ancestor::tr')

        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        c_query = 'select distinct(city) from states_and_cities where country="india"'
        cursor.execute(c_query)

        rows = cursor.fetchall()
        rows = [row[0] for row in rows if row[0]]

        for row in rows:
            city = textify(row.select('./td[1]/a/text()')).strip()

            state = ''
            country = 'india'
            # TODO ###### please check the country code
            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=IN&loc1=%s&loc2=%s' %(state,city)

            query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            state = ''
            values = (str(country),str(state),str(city), str(url))
            cursor.execute(query,values)

        cursor.close()
