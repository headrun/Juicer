from juicer.utils import *

class BlogCatalogTerminalSpider(JuicerSpider):
    name = 'blogcatalog_terminal_old'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)
        item.textify('title', '//div[@class="container_gray rounded_4 margin_right_20 margin_bottom_20"]//h2')
        item.textify('location', '//div[@class="user_data"]//text()')
        recent_visitors_links = hdoc.select('//ul[@class="friends"]//li//a/@href')
        recent_visitors_links = ['http://www.blogcatalog.com' + textify(r) for r in recent_visitors_links]
        item.set('recent_visitors_links', recent_visitors_links)

        blog_details = []
        nodelist = hdoc.select('//div[@class="blog"]')
        for node in nodelist:
            details = {}
            details['blog_title'] = textify(node.select('.//h3'))
            details['blog_url'] = textify(node.select('.//p//a'))
            details['blog_description'] = textify(node.select('.//p[@class="meta"]'))
            blog_details.append(details)
        item.set('blog_details', blog_details)

        recent_visitor = hdoc.select('//ul[@class="friends"]//li//a/p')
        recent_visitor = [textify(r) for r in recent_visitor]
        visit_day = hdoc.select('//ul[@class="friends"]//li//a/@title')
        visit_day = [str(parse_date(textify(v))) for v in visit_day]
        visitors = dict(zip(recent_visitor, visit_day))
        item.set('visitors', visitors)

        today = textify(hdoc.select('//ul[@class="stats"]//li')).split('Today:')[-1].split('Last')[0]
        today = today.strip()
        if today:
            item.set('today_visitors', int(today))
        last_7_days = textify(hdoc.select('//ul[@class="stats"]//li')).split('7 Days:')[-1].split('Last')[0]
        last_7_days = last_7_days.strip()
        if last_7_days:
            item.set('last_7_days_visitors', int(last_7_days))
        last_30_days = textify(hdoc.select('//ul[@class="stats"]//li')).split('30 Days:')[-1]
        last_30_days = last_30_days.strip()
        if last_30_days:
            item.set('last_30_days_visitors', int(last_30_days))

        button_title = hdoc.select('//div[@id="buttons"]//a//div[@class="button_title"]')
        button_title = [textify(t) for t in button_title]
        button_count = hdoc.select('//div[@id="buttons"]//a//div[@class="button_count"]')
        button_count = [int(textify(c)) for c in button_count]
        user_stats = dict(zip(button_title, button_count))
        item.set('user_stats', user_stats)

        friends_url = response.url + '/friends/'
        yield Request(friends_url, self.parse_friends, response, meta = {'item':item, '_friends':[] })

        followers_url = response.url + '/followers/'
        yield Request(followers_url, self.parse_followers, response, meta = {'item':item, '_followers':[] })

    def parse_friends(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        _friends = response.meta.get('_friends')
        friends = hdoc.select('//div[@class="page_column_568"]//ul[@class="friends"]//li//a/@href')
        for frnd in friends:
            frnd = textify(frnd)
            frnd = 'http://www.blogcatalog.com' + frnd
            get_page(self.name, frnd)
            _friends.append(frnd)

        next_frnd = textify(hdoc.select('//a[contains(text(), "NEXT")]/@href'))
        if next_frnd:
            yield Request(next_frnd, self.parse_friends, response, meta = {'item':item, '_friends':_friends })
        else:
            item.set('friends', _friends)

        yield item.process()

    def parse_followers(self, response):
        hdoc = HTML(response)
        item = response.meta.get('item')
        _followers = response.meta.get('_followers')
        followers = hdoc.select('//div[@class="page_column_568"]//ul[@class="friends"]//li//a/@href')
        for fllwr in followers:
            fllwr = textify(fllwr)
            fllwr = 'http://www.blogcatalog.com' + fllwr
            get_page(self.name, fllwr)
            _followers.append(fllwr)

        next_fllwr = textify(hdoc.select('//a[contains(text(), "NEXT")]/@href'))
        if next_fllwr:
            yield Request(next_fllwr, self.parse_followers, response, meta = {'item':item, '_followers':_followers })
        else:
            item.set('followers', _followers)

        yield item.process()
