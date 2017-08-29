from juicer.utils import *

class StumbleuponTerminalSpider(JuicerSpider):
    name = 'stumbleupon_terminal'

    #http://www.stumbleupon.com/stumbler/skyblue101
    #@url(["http://www.stumbleupon.com/stumbler/[^/]*$"])
    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        title = textify(hdoc.select('//p[@class="card-name"][@title]'))
        if title:
            item.set('title', title)

        nick_name = textify(hdoc.select('//h1[@class="card-nick"]'))
        item.set('nick_name', nick_name)

        image_url = textify(hdoc.select('//div[@class="card-modal-image"]//img/@src'))
        item.set('image_url', image_url)

        feed_comments = 'http://www.stumbleupon.com/rss/stumbler/' + sk + '/comments'
        item.set('feed_comments', feed_comments)

        feed_likes = 'http://www.stumbleupon.com/rss/stumbler/' + sk + '/likes'
        item.set('feed_likes', feed_likes)

        feed_additions = 'http://www.stumbleupon.com/rss/stumbler/' + sk + '/additions'
        item.set('feed_additions', feed_additions)

        follower_link = get_request_url(response) + '/connections/followers'
        get_page('stumbleupon_follower', follower_link)

        following_link = get_request_url(response) + '/connections/following'
        get_page('stumbleupon_following', following_link)

        interest_link = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[@class="page-interests"]/@href'))
        get_page('stumbleupon_interest', interest_link)

        channel_link = 'http://www.stumbleupon.com' + textify(hdoc.select('//a[@class="page-channels"]/@href'))
        get_page('stumbleupon_channel', channel_link)

        stats = {}
        nodelist = hdoc.select('//ul[@class="nav-side s-nav-side-first"]//li//a')
        for node in nodelist:
            key = textify(node.select('./text()'))
            value = int(textify(node.select('.//span/text()')).replace('(', '').replace(')', '').replace('K', '000').replace(',', ''))
            stats[key] = value
        item.set('stats', stats)

        yield item.process()
