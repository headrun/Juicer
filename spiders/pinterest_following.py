from juicer.utils import *

class PinterestFollowingSpider(JuicerSpider):
    name = 'pinterest_following'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk_id = get_request_url(response).split('.com/')[-1].split('/')[0]

        followings = []
        following = hdoc.select('//p[@class="PersonIdentity"]//a/@href')
        for flwng in following:
            flwng = textify(flwng)
            flwng = 'http://pinterest.com' + flwng
            get_page('pinterest_terminal', flwng)
            yield Request(flwng, self.parse_followingid, response, meta = {'sk_id':sk_id})

        if '?page=' in  response.url:
            page_number = (response.url).split('?page=')[-1]
            nxt = (response.url).split('?page=')[0]
            nxt2 = nxt + '?page='
            page_number = int(page_number) + 1

        else:
            nxt2 = response.url + '?page='
            page_number = 2

        next_following = nxt2 + '%s' %str(page_number)
        if next_following:
            get_page(self.name, next_following)

    def parse_followingid(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('.com/')[-1].split('/')[0]
        sk_id = response.meta.get('sk_id')
        sk = sk1 + '----' + sk_id
        item.set('sk', sk)

        user_id = sk_id
        item.set('user_id', user_id)

        flwng_id = sk1
        item.set('flwng_id', flwng_id)

        #yield item.process()
