from juicer.utils import *

class PinterestBoardPinsSpider(JuicerSpider):
    name = 'pinterest_boardpins'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('.com/')[-1].split('/')[1]
        item.set('sk', sk)

        likes_url = hdoc.select('//div[@id="PinLikes"]//a[@class="CommenterImage tipsyHover"]/@href')
        likes_url = ['http://pinterest.com' + textify(l) for l in likes_url]
        item.set('likes_user_url', likes_url)

        repins_url = hdoc.select('//div[@id="PinRepins"]//a[@class="CommenterImage"]/@href')
        repins_url = ['http://pinterest.com' + textify(r) for r in repins_url]
        item.set('repins_user_url', repins_url)

        comment_url = hdoc.select('//div[@class="PinComments"]//a[@class="CommenterName"]/@href')
        comment_url = ['http://pinterest.com' + textify(c) for c in comment_url]
        item.set('comment_user_url', comment_url)

        like = textify(hdoc.select('//div[@id="PinLikes"]//p[@class="PinMoreActivity"]//strong')).split('+')[-1]
        if like:
            like = int(like)
        else:
            like = 0
        likes_count = len(likes_url) + like
        item.set('likes_count', likes_count)

        repin = textify(hdoc.select('//div[@id="PinRepins"]//p[@class="PinMoreActivity"]//strong')).split('+')[-1]
        if repin:
            repin = int(repin)
        else:
            repin = 0
        repins_count = len(repins_url) + repin
        item.set('repins_count', repins_count)

        item.textify('image_url', '//div[@class="ImgLink"]//a//img/@src')

        comment_count = len(comment_url)
        item.set('comment_count', comment_count)

        user_id = textify(hdoc.select('//div[@class="board"]//a/@href')).split('/')[1]
        item.set('user_id', user_id)

        board_id = textify(hdoc.select('//div[@class="board"]//a/@href')).split('/')[-2]
        item.set('board_id', board_id)

        for url in likes_url: get_page('pinterest_terminal', url)

        for url in repins_url: get_page('pinterest_terminal', url)

        for url in comment_url: get_page('pinterest_terminal', url)

        yield item.process()
