from juicer.utils import *
from unicodedata import normalize
import  MySQLdb

class Blogger_Urls(JuicerSpider):
    name = 'blogger_urls_bkup'
    #settings.overrides['DEPTH_LIMIT'] = 0

    def start_requests(self):
        requests = []

        '''
        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        query = 'SELECT url,country FROM states_and_cities WHERE is_crawled=0 limit 5'
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            my_list = []
            for result in results:
                url = result[0].strip()
                country= result[1]
                r = Request(url, self.parse, None, meta={'country': country})
                requests.extend(r)
                my_list.append(str(url))

            my_tuple = tuple(my_list)
            query = "UPDATE states_and_cities SET is_crawled = 2 WHERE url in %s"
            values = str((my_tuple))
            cursor.execute(query % values)
        except: print 'came into except Mr.venu'

        cursor.close()
        '''
        url = 'http://www.blogger.com/profile-find.g?t=l&loc0=IN&loc1=Haryana&loc2=Bahadurgarh'
        r = Request(url, self.parse, None, meta={'country': 'india'})
        requests.extend(r)
        return requests


    def parse(self, response):
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
                print 'url which can"t be updated as status 1 is::>>>', response.url

        blogger_urls = hdoc.select_urls(['//h2/a/@href'], response)
        for blogger_url in blogger_urls:
            yield Request(blogger_url, self.parse_author, response,
            meta = {'country' : response.meta['country']})

        next_url = hdoc.select('//a[contains(@href,"profile-find.g")]/@href')
        if next_url:
            yield Request(next_url, self.parse, response,
            meta = {'country' : response.meta['country']})


    def parse_author(self, response):
        hdoc = HTML(response)

        blog_urls = hdoc.select_urls(['//ul/li[@class="sidebar-item"]/span[@dir="ltr"]/a/@href'], response)
        country = response.meta['country']

        attributes = {}
        for tr in hdoc.select("//div[@class='contents-after-sidebar']//tr"):
            key = textify(tr.select(".//th"))
            value = textify(tr.select(".//td"))
            attributes[make_var(key)] = value.strip()

        name = textify(hdoc.select('//h1'))
        profile_views = textify(hdoc.select('//p[contains(text(),"Profila")]//text()'))
        profile_views = ''.join(re.findall(r'\d+', profile_views))
        profile_views = int(profile_views) if profile_views else 0

        blogs_follow = hdoc.select_urls(['//ul/li[@class="sidebar-item"]/a/@href'], response)
        blogs_follow = '#<>#'.join(blogs_follow)

        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='blogger', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        for blog_url in blog_urls:
            if blog_url.endswith('/'):
                url = blog_url + 'feeds/posts/default?alt=rss'
            else:
                url = blog_url+'/feeds/posts/default?alt=rss'

            query = "INSERT into blogger_urls(country,url,author_url,author_name,attributes,blogs_follow,profile_views, created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            values = (modify(country),modify(url),modify(response.url),modify(name),modify(attributes),modify(blogs_follow),int(profile_views))
            cursor.execute(query,values)

        cursor.close()


def modify(data):
    try:
        return str(data)
    except:
        try:
            data = ''.join([chr(ord(x)) for x in data]).decode('utf8', 'ignore').encode('utf8')
            return varchar(data)
        except ValueError or UnicodeDecodeError or UnicodeEncodeError:
            try:
                return varchar(data.encode('utf8'))
            except  ValueError or UnicodeEncodeError or UnicodeDecodeError:
                try:
                    return varchar(data)
                except ValueError or UnicodeEncodeError or UnicodeDecodeError:
                    try:
                        return varchar(xcode(data).encode('utf-8','ignore').decode('ascii', 'ignore'))
                    except UnicodeDecodeError:
                        data = normalize('NFKD', data.decode('utf-8','ignore')).encode('ascii', 'ignore')
                        return varchar(data)


def varchar(string):
    return re.sub(r' +',' ', string.replace('&amp;','&').replace('&quot;','"').replace('&gt;',
                          '>').replace('&lt;','<').replace(u'\uf0fc\t', '').replace(u'\uf0d8',
                        '').replace(u'\uf0b7','').replace(u"\uf0f3\t",'').replace(u'\uf0d4\t',
              '').replace(u'\u2022','').replace(u'\xbb','').replace('\n','').replace('\t','').replace('\u2019','')).strip()
