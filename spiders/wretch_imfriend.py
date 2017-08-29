from juicer.utils import *

class WretchImfriendSpider(JuicerSpider):
    name = 'wretch_imfriend'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        user_id = get_request_url(response).split('/')[-1].split('&')[0]

        imfriends = []
        imfriend = hdoc.select('//div[@id="friendListDiv"]//li//a/@href')
        for imfrnd in imfriend:
            imfrnd = textify(imfrnd)
            imfrnd = imfrnd.replace('/friend/', '/user/')
            get_page('wretch_terminal', imfrnd)
            yield Request(imfrnd, self.parse_imfriend, response, meta = {'user_id':user_id})

        next_url = textify(hdoc.select('//div[@id="pagelink_1"]//a[contains(text(), " ")]/@href'))
        if next_url:
            next_url = 'http://www.wretch.cc' + next_url
            get_page(self.name, next_url)

        friendship_url = textify(hdoc.select('//li[@id="current_tag2"]//a/@href'))
        get_page('wretch_friendship', friendship_url)

    def parse_imfriend(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        user_id = response.meta.get('user_id')
        item.set('user_id', user_id)

        sk = sk1 + '---' + user_id
        item.set('sk', sk) 

        imfriend_id = sk1
        item.set('imfriend_id', imfriend_id)

        yield item.process()
