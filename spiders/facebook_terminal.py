from juicer.utils import *
import re

class FacebookTerminalSpider(JuicerSpider):
    name = 'facebook_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response)
        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//div[@class="name"]//h2/a/text()')))
        if not title:
            title = xcode(textify(hdoc.select('//h1[@itemprop="name"]//span')))
        item.set('title', title)

        title_sub = xcode(textify(hdoc.select('//span[@class="fbProfileNonIconBylineFragment"]//div[@class="fsm fwn fcg"]')))
        if not title_sub:
            title_sub = xcode(textify(hdoc.select('//span[@class="fsm fwn fcg"]')))
        item.set('title_sub', title_sub)

        about = xcode(textify(hdoc.select('//span[@class="fbLongBlurb"]')))
        if not about:
            about = xcode(textify(hdoc.select('//span[@class="fsm"]')))
        item.set('about', about)

        image_url = textify(hdoc.select('//img[@class="photo img"]/@src'))
        item.set('image_url', image_url)


        feed = textify(hdoc.select('//span[contains(text(), "Sign Up")]//parent::a/@href')).split('_id=')[-1].split('&')[0]
        if not feed:
            feed = textify(hdoc.select('//a[contains(text(), "Log in")]/@href')).split('_id=')[-1].split('&')[0]
        feed_url = 'https://www.facebook.com/feeds/page.php?id=' + feed + '&format=rss20'
        item.set('feed_url', feed_url)

        likes_this = textify(hdoc.select('//div[contains(text(), "like this")]//span/text()')).replace(',', '')
        if likes_this:
            item.set('likes_this', int(likes_this))

        talking_about_this = textify(hdoc.select('//div[contains(text(), "talking about this")]//span/text()')).replace(',', '')
        if talking_about_this:
            item.set('talking_about_this', int(talking_about_this))

        if not likes_this:
            likes_link = textify(hdoc.select('//div[@class="modify"]//a[contains(@href, "/likes")]/@href'))
            yield Request(likes_link, self.parse_likes, response, meta = {'item':item})

        info_url = get_request_url(response) + '/info'
        yield Request(info_url, self.parse_information, response, meta={'item':item})

    def parse_likes(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        nodes = textify(hdoc.select('//span[@class="timelineLikesBigNumber fsm"]'))

        likes_this = nodes.split(' ')[0]
        if likes_this:
            likes_this = likes_this.replace(',', '')
            item.set('likes_this', int(likes_this))

        talking_abouth_this = nodes.split(' ')[-1]
        if talking_abouth_this:
            talking_abouth_this = talking_abouth_this.replace(',', '')
            item.set('talking_abouth_this', int(talking_abouth_this))

        most_popular_age_group = textify(hdoc.select('//div[@class="timelineLikesMetricTitle fsxl"]/text()[contains(., "old")]'))
        item.set('most_popular_age_group', most_popular_age_group)

        most_popular_city = hdoc.select('//span[contains(text(), "Most Popular City")]//parent::li//div/text()')
        most_popular_city = [textify(c) for c in most_popular_city]
        item.set('most_popular_city', most_popular_city)

        most_popular_week = textify(hdoc.select('//span[contains(text(), "Most Popular Week")]//parent::li//div/text()'))
        item.set('most_popular_week', most_popular_week)

        yield item.process()

    def parse_information(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        nodes = hdoc.select('//div[@class="phs"]//table//tr') or hdoc.select('//table[@class="uiInfoTable profileInfoTable"]//tr')
        information = {}
        for node in nodes:
            key = textify(node.select('.//th[@class="label"]'))
            if key:
                value = xcode(textify(node.select('.//td[@class="data"]//text()')))
                information[key] = value
                if 'Likes' in information:
                    information['Likes'] = information['Likes'].split(',').strip()
        item.set('information', information)
        biography = xcode(textify(hdoc.select('//div[@class="mhl"]//div[@class="text_exposed_root"]')))
        if biography:
            item.set('biography', biography)

        yield item.process()
