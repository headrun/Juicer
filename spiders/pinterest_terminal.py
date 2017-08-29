from juicer.utils import *

class PinterestTerminalSpider(JuicerSpider):
    name = 'pinterest_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('.com/')[-1].split('/')[0]
        item.set('sk', sk)

        item.textify('title', '//div[@class="content"]//h1')
        followers = textify(hdoc.select('//a[contains(@href, "/followers/")]/strong'))
        item.set('followers', int(followers))
        following = textify(hdoc.select('//a[contains(@href, "/following/")]/strong'))
        item.set('following', int(following))
        item.textify('user_description', '//p[@class="colormuted"]')
        item.textify('location', '//li[@id="ProfileLocation"]')
        item.textify('image_url', '//a[@class="ProfileImage"]//img/@src')
        links = {}
        links['facebook'] = textify(hdoc.select('//li//a[@class="icon facebook"]/@href'))
        links['twitter'] = textify(hdoc.select('//li//a[@class="icon website"]/@href'))
        links['website'] = textify(hdoc.select('//li//a[@class="icon twitter"]/@href'))
        feed_url = response.url + 'feed.rss'
        links['feed'] = feed_url
        item.set('links', links)
        boards_count = textify(hdoc.select('//a[contains(text(), "Boards")]/strong'))
        if boards_count:
            item.set('boards_count', int(boards_count))
        likes_count = textify(hdoc.select('//a[contains(text(), "Likes")]/strong'))
        if likes_count:
            item.set('likes', int(likes_count))
        pins_count = textify(hdoc.select('//a[contains(text(), "Pins")]/strong'))
        if pins_count:
            item.set('pins', int(pins_count))

        boards = hdoc.select('//div[@class="pin pinBoard"]//div[@class="board"]//a/@href')
        boards = ['http://pinterest.com' + textify(b) for b in boards]
        item.set('boards', boards)
        for board in boards: get_page('pinterest_board', board)

        following_url = textify(hdoc.select('//a/@href[contains(., "/following/")]'))
        following_url = 'http://pinterest.com' + following_url
        item.set('following_url', following_url)
        get_page('pinterest_following', following_url)

        follower_url = textify(hdoc.select('//a/@href[contains(., "/followers/")]'))
        follower_url = 'http://pinterest.com' + follower_url
        item.set('follower_url', follower_url)
        get_page('pinterest_follower', follower_url)


        yield item.process()
