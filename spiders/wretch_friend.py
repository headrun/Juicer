from juicer.utils import *

class WretchFriendSpider(JuicerSpider):
    name = 'wretch_friend'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        user_id = get_request_url(response).split('/')[-1]

        friends = []
        friend = hdoc.select('//div[@id="friendListDiv"]//li//a/@href')
        for frnd in friend:
            frnd = textify(frnd)
            frnd = frnd.replace('/friend/', '/user/')
            get_page('wretch_terminal', frnd)
            yield Request(frnd, self.parse_friend, response, meta = {'user_id':user_id})

        next_url = textify(hdoc.select('//div[@id="pagelink_1"]//a[contains(text(), " ")]/@href'))
        if next_url:
            next_url = 'http://www.wretch.cc' + next_url
            get_page(self.name, next_url)

        imfriend_url = textify(hdoc.select('//li[@id="current_tag1"]//a/@href'))
        get_page('wretch_imfriend', imfriend_url)

    def parse_friend(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        user_id = response.meta.get('user_id')
        item.set('user_id', user_id)

        sk = sk1 + '---' + user_id
        item.set('sk', sk)

        friend_id = sk1
        item.set('friend_id', friend_id)

        yield item.process()
