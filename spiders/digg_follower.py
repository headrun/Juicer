from juicer.utils import *

class DiggFollowerSpider(JuicerSpider):
    name = 'digg_follower'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk_id = get_request_url(response).split('/')[-2]

        followers = []
        follower = hdoc.select('//a[@class="user-item-title"]/@href')
        for flwr in follower:
            flwr = textify(flwr)
            flwr = 'http://digg.com' + flwr
            get_page('digg_terminal', flwr)
            yield Request(flwr, self.parse_followerid, response, meta = {'sk_id':sk_id})

    def parse_followerid(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        sk_id = response.meta.get('sk_id')
        sk = sk1 + '----' + sk_id
        item.set('sk', sk)

        user_id = sk_id
        item.set('user_id', user_id)

        flwr_id = sk1
        item.set('flwr_id', flwr_id)

        yield item.process()
