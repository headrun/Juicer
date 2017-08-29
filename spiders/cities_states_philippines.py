from juicer.utils import *
import MySQLdb

class PhilippineCountry(JuicerSpider):
    name = 'cities_states_philippines'
    #start_urls = ['http://www.philippinecountry.com/provcitmun.html']
    #start_urls = ["http://en.wikipedia.org/wiki/List_of_cities_and_municipalities_in_the_Philippines"]
    start_urls = ['http://openstreetmap.org.ph/viewall.php']

    def parse(self, response):
        hdoc = HTML(response)

        #cities = hdoc.select('//div[@id="wrapper"]//td//a')
        #cities = hdoc.select('//td/a[contains(@href,"/wiki/")]|//li/a[contains(@href,"/wiki/")]')
        cities = hdoc.select('//li/a/h3')
        print len(cities)
        #cities = [1]
        for i in cities:
            city = textify(i.select('./text()'))  #for travelmath split(',') is required
            city = city.replace(' ', '+').lower()
            state = ''
            country = 'philippines'

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=PH&loc1=%s&loc2=%s' %(state,city)
            #url = 'http://www.blogger.com/profile-find.g?t=l&loc0=PH'
            print 'location>>', city, state, url
            try:
                conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
                conn.set_character_set('utf8')
                cursor = conn.cursor()

                query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(country),str(state),str(city), str(url))
                cursor.execute(query,values)

                cursor.close()
            except:
                print "in try"
                pass
