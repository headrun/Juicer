from juicer.utils import *

class DiggTerminalSpider(JuicerSpider):
    name = 'digg_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        title = textify(hdoc.select('//div[@class="profile-title group"]//h1'))
        item.set('title', title)

        user_id = textify(hdoc.select('//ul[@class="profile-links group"]//li[not(contains(@class, "group"))]'))
        item.set('user_id', user_id)

        links1 = hdoc.select('//ul[@class="profile-links group"]//li//a/@href')
        links1 = [textify(o) for o in links1]

        feed_url = textify(hdoc.select('//li[@id="rss-link"]//a/@href'))
        feed_url = 'http://digg.com' + feed_url
        item.set('feed_url', feed_url)

        user_stats = {}
        key = hdoc.select('//ul[@class="profile-stats group"]//li//a//span') and hdoc.select('//ul[@class="profile-stats group"]//li//span')
        key = [textify(k) for k in key]
        value = hdoc.select('//ul[@class="profile-stats group"]//li//a//strong') and hdoc.select('//ul[@class="profile-stats group"]//li//strong')
        value = [int(textify(v).replace('%', '').replace(',', '')) for v in value]
        user_stats = dict(zip(key, value))
        item.set('user_stats', user_stats)

        about = textify(hdoc.select('//span[@class="profile-bio-text"]'))
        item.set('about', about)

        location = textify(hdoc.select('//span[@class="location"]'))
        item.set('location', location)

        awards = hdoc.select('//span[@class="digger-name"]')
        awards = [textify(p).replace('amp;', '') for p in awards]
        item.set('awards', awards)

        links2 = hdoc.select('//li[@class="group"]//dt//a/@href')
        links2 = [textify(l) for l in links2]

        other_links = links1 + links2
        item.set('other_links', other_links)

        newsroom_urls = hdoc.select('//span[@class="item-user"]//a/@href')
        newsroom_urls = ['http://digg.com' + textify(n) for n in newsroom_urls]
        item.set('newsroom_urls', newsroom_urls)

        for newsroom_url in newsroom_urls:
            yield Request(newsroom_url, self.parse_newsroom, response)

        post_urls = hdoc.select('//li[@class="story-item-comments"]//a/@href')
        post_urls = ['http://digg.com' + textify(c) for c in post_urls]
        item.set('post_urls', post_urls)

        for post_url in post_urls:
            yield Request(post_url, self.parse_post, response)

        posts_details = {}
        post_title = hdoc.select('//h3[@class="story-item-title"]//a[not(contains(@href, "/story/"))]')
        post_title = [xcode(textify(p).replace('.', '')) for p in post_title]
        post_date = hdoc.select('//span[@class="timestamp"]')
        post_date = [parse_date(textify(d).split(' ago')[0].replace('hr', 'hours').replace('min', 'minutes')) for d in post_date]
        posts_details = dict(zip(post_title, post_date))
        item.set('posts_details', posts_details)

        following_url = textify(hdoc.select('//a[@id="filter-following"]/@href'))
        following_url = 'http://digg.com' + following_url
        get_page('digg_following', following_url)

        follower_url = textify(hdoc.select('//a[@id="filter-followers"]/@href'))
        follower_url = 'http://digg.com' + follower_url
        get_page('digg_follower', follower_url)

        yield item.process()

    def parse_newsroom(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        post_links = hdoc.select('//li[@class="story-item-comments"]//a/@href')
        post_links = ['http://digg.com' + textify(l) for l in post_links]

        for post_link in post_links:
            yield Request(post_link, self.parse_post, response)

    def parse_post(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        user_links = hdoc.select('//div[@class="comment-author group"]//p//a[@class="comment-owner-name hcard-trigger"]/@href')
        user_links = ['http://digg.com' + textify(u) for u in user_links]

        for user_link in user_links:
            get_page('digg_terminal', user_link)
