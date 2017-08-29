from juicer.utils import *

class WretchTerminalSpider(JuicerSpider):
    name = 'wretch_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        user_details = {}
        nodelist = hdoc.select('//div[@id="container"]//td[@id="sidetitle_img"]//ancestor::table//tr')
        for node in nodelist:
            key = xcode(textify(node.select('.//td[@class="sidetitle"][@align="right"]')))
            if key:
                value = xcode(textify(node.select('.//td[@class="side"]')))
                user_details[key] = value
        item.set('user_details', user_details)

        today_visitors = textify(hdoc.select('//td[@id="counter"]//font/text()[contains(., "Today")]')).split(': ')[-1]
        if today_visitors:
            item.set('today_visitors', int(today_visitors))

        total_visitors = textify(hdoc.select('//td[@id="counter"]//font/text()[contains(., "Total")]')).split(': ')[-1]
        if total_visitors:
            item.set('total_visitors', int(total_visitors))

        title = xcode(textify(hdoc.select('//font[@class="small-c"]/text()[contains(., "[")]'))).split('[ ')[-1]
        title = title.replace("'s", "")
        item.set('title', title)

        blog_url = textify(hdoc.select('//a[@id="linkBlog"]/@href'))
        blog_url = 'http://www.wretch.cc' + blog_url
        item.set('blog_url', blog_url)
        get_page('wretch_blog', blog_url)

        friend_url = textify(hdoc.select('//a[@id="linkFriend"]/@href'))
        friend_url = 'http://www.wretch.cc' + friend_url
        item.set('friend_url', friend_url)
        get_page('wretch_friend', friend_url)

        yield item.process()
