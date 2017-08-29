from juicer.utils import *
import MySQLdb

class Socialbakers(JuicerSpider):
    name = 'socialbakers_terminal'

    def parse(self, response):
        hdoc = HTML(response)

        got_page(self.name, response, data=repr(response.meta['data']))
        import pdb;pdb.set_trace()
        data = (response.meta['data']).strip()
        category = response.meta['category']
        country = response.meta['country']

        print response.url, country

        pages = hdoc.select('//section[@class="content"]//td[@class="rank"]/following-sibling::td[1]/a')
        for page in pages:
            social_bakers_url = textify(page.select('./@href'))
            title = textify(page.select('.//text()')).encode('utf8').decode('ascii','ignore')
            fb_page_id = ''.join(re.findall(r'\d+', social_bakers_url))
            fb_page = 'https://www.facebook.com/%s' %(fb_page_id)
            feed_url = 'https://www.facebook.com/feeds/page.php?id=%s&format=rss20' %(fb_page_id)

            try:
                conn = MySQLdb.connect(host='127.0.0.1', user='root', db='socialbakers', passwd='root')
                cursor = conn.cursor()
                query = "insert into socialbakers_urls(fb_page_id,country,category,page_title,feed_url,social_bakers_url,created_at,modified_at) values(%s,%s,%s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(fb_page_id),str(country),str(category), str(title),str(feed_url),str(social_bakers_url))
                cursor.execute(query,values)
                cursor.close()
            except Exception as e:
                print e.message


