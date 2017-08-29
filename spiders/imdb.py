from juicer.utils import *

class ImdbSpider(JuicerSpider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = 'http://www.imdb.com/genre'

    def parse(self, response):
        hdoc = HTML(response)

        url_pattern = '/search/title?genres=%s&title_type=feature&sort=moviemeter,asc'
        for node in hdoc.select('//a[contains(@href, "/genre/")]/@href'):
            href = textify(node)
            genre = href.split('/')[-1]

            yield Request(url_pattern % genre, self.parse_listing, response)

    def parse_listing(self, response):
        hdoc = HTML(response)
        movie_nodes = hdoc.select('//table[@class="results"]//tr[contains(@class, "detailed")]')
        for movie_node in movie_nodes:

            item = Item(response, HTML)
            item.selector = movie_node

            item.textify('title', './/td[@class="title"]/a/text()')
            item.textify('description','.//span[@class="outline"]/text()')
            people = [textify(person) for person in movie_node.select('.//span[@class="credit"]/a/text()')]
            item.set('people', list(set(people)))
            genres = [textify(genre) for genre in movie_node.select('.//td[@class="title"]/span[@class="genre"]/a/text()')]
            item.set('genres', genres)
            year = textify(movie_node.select('.//td[@class="title"]/span[@class="year_type"]/text()'))[1:-1]
            item.set('year', year)
            item.set('sk', textify(movie_node.select('.//td[@class="title"]/a/@href')).split('/title/')[-1].strip('/'))

            yield item.process()

#        yield Request(hdoc.select('//td[@class="title"]/a[contains(@href, "/title/tt")]/@href'), self.parse_details, response)
        yield Request(hdoc.select('//span[@class="pagination"]/a/@href'), self.parse_listing, response)

    def parse_details(self, response):
        return
        hdoc = HTML(response)

        item = Item(response, HTML)
        item.selector = movie_node

        item.textify('movie_name', '//div[@id="divBreadCrumb"]/span/a[position()>2]/text()', sep=" > ")
        item.textify('name', '//span[contains(@id, "BusinessName")]/text()')
        item.textify('phone', '//span[contains(@id, "PhoneNo")]/text()')
        item.textify('url', '//a[contains(@id, "lnkWebsite")]/@href')
        item.textify('address', '//span[contains(@id, "Address")]/text()')
        item.set('sk', response.url.split('-')[-1].strip('/'))

        yield item.process()
