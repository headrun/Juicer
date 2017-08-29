from juicer.utils import *
import pymongo

client = pymongo.Connection("46.4.102.177", 27017)

db = client.blogger

class Blogger_Authors_Usa(JuicerSpider):
    handle_httpstatus_list = [302, 400, 401, 403, 404,
                            408, 500, 501, 502, 503, 504,
                            505, 506, 507, 508, 509, 510
                        ]

    name = 'blogger_authors_usa'
    allowed_domains = ['www.blogger.com']

    def parse(self, response):

        country = (response.meta['data']).strip()
        got_page(self.name, url=response.url.replace('https','http'), data=repr(response.meta['data']))

        if response.status != 200:
            get_page("blogger_authors_uncrawled", response.url, data=country)

            #raise CloseSpider('%s status code' %(response.status))

            return

        hdoc = HTML(response)

        name = textify(hdoc.select('//h1'))

        user_blogs = hdoc.select_urls(['//div[@class="contents-after-sidebar"]/ul\
                    /li[@class="sidebar-item"]/span[@dir="ltr"]/a/@href'], response)
        blogs_follow = hdoc.select_urls(['//div[@class="contents-after-sidebar"]/\
                    ul/li[@class="sidebar-item"]/a/@href'], response)

        attributes = {}
        for tr in hdoc.select("//div[@class='contents-after-sidebar']//tr"):
            key = textify(tr.select(".//th"))
            value = textify(tr.select(".//td"))
            attributes[make_var(key)] = value.strip()

        sk = response.url.split('/')[-1]

        doc = {'sk' : sk}
        doc['updated'] = get_current_timestamp()
        doc['added'] = get_current_timestamp()
        doc['xtags'] = country+'_country_manual'

        doc['is_added'] = 0 if user_blogs else 1

        data = {'name' : name}
        data['url'] = xcode(response.url)
        data['user_blogs'] = user_blogs
        data['followed_blogs'] = blogs_follow
        data['attributes'] = attributes

        doc['data'] = data
        if sk:
            db.blogger_authors.update({'sk':sk}, doc, upsert=True)

