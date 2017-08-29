from juicer.utils import *

class Blogger_Urls(JuicerSpider):
    name = 'blogger_urls_mm'

    '''
    def start_requests(self):
        requests = []

        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        query = 'SELECT url,country FROM states_and_cities WHERE country="hongkong" and is_crawled=0'
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            my_list = []
            for result in results:
                url = result[0].strip()
                country = result[1]
                req_url = url.replace('http','https') if not url.startswith('https') else url
                r = Request(req_url, self.parse, None, meta={'country': country})
                requests.extend(r)
                my_list.append(str(url))

            my_tuple = tuple(my_list)
            query = "UPDATE states_and_cities SET is_crawled = 2 WHERE url in %s"
            values = str((my_tuple))
            cursor.execute(query % values)
        except: print 'came into except Mr.venu'

        cursor.close()

        return requests
    '''

    def parse(self, response):
        #TODO
        got_page(self.name, response, data=response.meta['data'])

        hdoc = HTML(response)

        if not 'start' in response.url:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
            conn.set_character_set('utf8')
            cursor = conn.cursor()
            query = 'UPDATE states_and_cities SET is_crawled=1, modified_at = NOW() WHERE url ="%s"' %(str(response.url))
            try:
                cursor.execute(query)
                cursor.close()
            except:
                cursor.close()
                print 'url which can"t be updated as status 1 is::>>>', response.url
        #TODO
        #country = response.meta['country']
        #country = response.meta['data'].strip()
        country = 'myanmar'
        import pdb;pdb.set_trace()
        blogger_urls = hdoc.select_urls(['//h2/a/@href'], response)
        #TODO
        for blogger_url in blogger_urls:
            get_page('blogger_authors_mm', blogger_url, data=country)

        next_url = hdoc.select('//a[contains(@href,"profile-find.g")]/@href').extract()
        if next_url:
            if len(next_url) > 1:
                get_page(self.name, next_url[1].split('&ct=')[0], data=country)
            else:
                get_page(self.name, next_url[0].split('&ct=')[0], data=country)

