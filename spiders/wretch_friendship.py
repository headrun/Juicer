from juicer.utils import *

class WretchFriendshipSpider(JuicerSpider):
    name = 'wretch_friendship'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        user_id = get_request_url(response).split('/')[-1].split('&')[0]

        friendships = []
        friendship = hdoc.select('//div[@id="friendListDiv"]//li//a/@href')
        for frndshp in friendship:
            frndshp = textify(frndshp)
            frndshp = frndshp.replace('/friend/', '/user/')
            get_page('wretch_terminal', frndshp)
            yield Request(frndshp, self.parse_friendship, response, meta = {'user_id':user_id})

        next_url = textify(hdoc.select('//div[@id="pagelink_1"]//a[contains(text(), " ")]/@href'))
        if next_url:
            next_url = 'http://www.wretch.cc' + next_url
            get_page(self.name, next_url)

    def parse_friendship(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        user_id = response.meta.get('user_id')
        item.set('user_id', user_id)

        sk = sk1 + '---' + user_id
        item.set('sk', sk) 

        friendship_id = sk1
        item.set('friendship_id', friendship_id)

        yield item.process()
