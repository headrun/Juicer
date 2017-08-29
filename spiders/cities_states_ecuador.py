from juicer.utils import *
import MySQLdb

class Wiki_Malay(JuicerSpider):
    name = 'cities_states_ecuador'
    start_urls = ['http://www.travelmath.com/cities-in/Thailand']

    def parse(self, response):
        hdoc = HTML(response)

        cities = hdoc.select('//div[@class="boxmiddle"]//td[@valign="top"]/a')
        print len(cities)
        for i in cities:
            city = textify(i.select('./text()')).split(',')[0].strip()  #for travelmath split(',') is required
            city = city.replace(' ', '+').lower().encode('utf8').decode('ascii','ignore')
            state = ''
            country = 'thailand'

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=TH&loc1=%s&loc2=%s' %(state,city)
            try: print 'location>>', city, state, url
            except: pass

            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
            conn.set_character_set('utf8')
            cursor = conn.cursor()


            query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            values = (str(country),str(state),str(city), str(url))
            cursor.execute(query,values)

            cursor.close()
