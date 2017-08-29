from juicer.utils import *
import MySQLdb

class Wiki(JuicerSpider):
    name = 'cities_states_singapore'
    start_urls = ['http://www.fallingrain.com/world/SN/']

    def parse(self, response):
        hdoc = HTML(response)

        rows = hdoc.select_urls(['//body/a/@href'], response)
        for row in rows:
            if not 'index' in row:
                yield Request(row, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)

        cities = hdoc.select('//body/table//tr/td[contains(text(),"city")]/parent::tr/td/a')
        for i in cities:
            city = textify(i.select('./text()'))
            city = city.replace(' ', '+').lower()
            state = ''
            country = 'singapore'

            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
            conn.set_character_set('utf8')
            cursor = conn.cursor()

            url = 'http://www.blogger.com/profile-find.g?t=l&loc0=SG&loc1=%s&loc2=%s' %(state,city)
            print 'location>>', city, state

            query = "insert into states_and_cities(country,state,city,url,created_at,modified_at) values(%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            values = (str(country),str(state),str(city), str(url))
            cursor.execute(query,values)

            cursor.close()
