from juicer.utils import *

class Socialbakers(JuicerSpider):
    name = 'socialbakers_bkup'

    def start_requests(self):
        req = []

        """
        countries = [
            'india', 'singapore', 'indonesia', 'malaysia',
            'philippines', 'china', 'vietnam', 'thailand'
        ]"""

        category_urls = ['http://www.socialbakers.com/facebook-pages/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/brands/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/media/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/entertainment/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/sports/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/society/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/community/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/celebrities/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/place/country/%s/',
                        'http://www.socialbakers.com/facebook-pages/politics/country/%s/',
                    ]

        for category_url in category_urls:
            country = 'india'
            con_url = category_url %(country)
            category = category_url.split('/')[-4]
            r = Request(con_url, self.parse, None, meta = {'country' : country, 'category' : category})
            req.extend(r)

        return req

    def parse(self, response):
        hdoc = HTML(response)

        category = response.meta['category']
        country = response.meta['country']

        data = {"country" : country, "category" : country}
        print response.url, country
        get_page("socialbakers_terminal", response.url, data=data)

        next_page = textify(hdoc.select('//li[@class="next"]/a/@href'))
        if next_page:
            next_page = 'http://www.socialbakers.com' + next_page
            for i in range(1000):
                next_url = response.url + "page-%s/" %(i)
                get_page("socialbakers_terminal", next_url, data=data)



