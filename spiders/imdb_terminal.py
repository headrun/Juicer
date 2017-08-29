from juicer.utils import *

class ImdbTerminalSpider(JuicerSpider):
    name = 'imdb_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-2]
        item.set('sk', sk)
        item.textify('title', '//h1[@class="header"]')
        item.textify('year', '//h1[@class="header"]//span//a')
        movie_duration = textify(hdoc.select('//div[@class="infobar"]/text()'))
        movie_duration = movie_duration.split('min')[0]
        movie_duration = movie_duration + 'min'
        item.set('movie_duration', movie_duration)
        item.set('movie_release_date', '//div[@class="infobar"]//span[@class="nobr"]//a')
        item.textify('movie_type', '//div[@class="infobar"]//a[contains(@href, "/genre/")]')
        item.textify('movie_rating', '//span[@itemprop="ratingValue"]')
        item.textify('movie_description', '//p[@itemprop="description"]')
        nodelist = hdoc.select('//td[@id="overview-top"]//div[@class="txt-block"]')
        movie_team = {}
        for node in nodelist:
            key = textify(node.select('.//h4[@class="inline"]'))
            value = textify(node.select('.//a'))
            movie_team[key] = value
        item.set('movie_team', movie_team)
        item.textify('movie_image', '//td[@id="img_primary"]//a//img/@src')
        nodes = hdoc.select('//table[@class="cast_list"]//tr[@class]')
        movie_cast = {}
        for node in nodes:
            key = textify(node.select('.//td[@class="name"]'))
            value = textify(node.select('.//td[@class="character"]//div//text()')).strip()
            movie_cast[key] = value
        item.set('movie_cast', movie_cast)
        item.textify('movie_storyline', '//div[@class="article"]//p')
        yield item.process()
