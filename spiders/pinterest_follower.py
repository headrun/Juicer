from juicer.utils import *

class PinterestFollowerSpider(JuicerSpider):
    name = 'pinterest_follower'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk_id = get_request_url(response).split('.com/')[-1].split('/')[0]

        followers = []
        follower = hdoc.select('//p[@class="PersonIdentity"]//a/@href')
        for flwr in follower:
            flwr = textify(flwr)
            flwr = 'http://pinterest.com' + flwr
            get_page('pinterest_terminal', flwr)
            yield Request(flwr, self.parse_followerid, response, meta = {'sk_id':sk_id})

        if '?page=' in  response.url:
            page_number = (response.url).split('?page=')[-1]
            nxt = (response.url).split('?page=')[0]
            nxt2 = nxt + '?page='
            page_number = int(page_number) + 1

        else:
            nxt2 = response.url + '?page='
            page_number = 2

        next_follower = nxt2 + '%s' %str(page_number)
        if next_follower:
            get_page(self.name, next_follower)

    def parse_followerid(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('.com/')[-1].split('/')[0]
        sk_id = response.meta.get('sk_id')
        sk = sk1 + '----' + sk_id
        item.set('sk', sk)

        user_id = sk_id
        item.set('user_id', user_id)

        flwr_id = sk1
        item.set('flwr_id', flwr_id)

        #yield item.process()
