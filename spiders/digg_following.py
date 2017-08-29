from juicer.utils import *

class DiggFollowingSpider(JuicerSpider):
    name = 'digg_following'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk_id = get_request_url(response).split('/')[-2]

        followings = []
        following = hdoc.select('//a[@class="user-item-title"]/@href')
        for flwng in following:
            flwng = textify(flwng)
            flwng = 'http://digg.com' + flwng
            #get_page('digg_terminal', flwng)
            yield Request(flwng, self.parse_followingid, response, meta = {'sk_id':sk_id})

    def parse_followingid(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        sk_id = response.meta.get('sk_id')
        sk = sk1 + '----' + sk_id
        item.set('sk', sk)

        user_id = sk_id
        item.set('user_id', user_id)

        flwng_id = sk1
        item.set('flwng_id', flwng_id)

        yield item.process()
