from juicer.utils import *

class TumblrTerminalSpider(JuicerSpider):
    name = 'tumblr_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response)
        got_page(self.name, response)
        item.set('sk', sk)
        followings = hdoc.select('//center//a/@href')
        fols = []
        for following in followings:
            fol=textify(following)
            if 'tumblr.com' in fol:
                fols.append(fol)
        followings = fols
        for following in followings:
            get_page(self.name, following)
        item.set('followings', followings)
        random = response.url + '/random'
        yield Request(random, self.parse_details, response, meta = {'item':item })

    def parse_details(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        randoms = hdoc.select('//span[@class="action"]//a/@href')
        randos = [textify(random) for random in randoms]
        randoms = randos
        for random in randoms:
            get_page(self.name, random)
        item.set('randoms', randoms)
        ask = response.url.split('/')
        ask[-1] = 'ask'
        ask = '/'.join(ask)
        yield Request(ask, self.parse_data, response, meta = {'item':item })
    def parse_data(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        user_profile = textify(hdoc.select('//div[@id="description"]//div/text()')).strip() or textify(hdoc.select('//div[@class="side"]/text()')) or textify(hdoc.select('//div[@id="sidebar"]//p/text()')) or textify(hdoc.select('//div[@class="sidebardescr"]/text()'))
        item.set('user_profile', user_profile)
        yield item.process()
