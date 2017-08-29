from juicer.utils import *

class TencentTerminalSpider(JuicerSpider):
    name = 'tencent_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)

        title = xcode(textify(hdoc.select('//span[@class="userName"]')))
        item.set('title', title)

        user_id = xcode(textify(hdoc.select('//h4//span[@class="left"]'))).replace('(@', '').replace(')', '')
        item.set('user_id', user_id)

        posts_count = textify(hdoc.select('//div[@class="userNums"]//a[contains(text(), "Posts")]//strong'))
        if posts_count:
            item.set('posts_count', int(posts_count))

        follower_count = textify(hdoc.select('//div[@class="userNums"]//a//strong[@class="followNum"]'))
        if follower_count:
            item.set('follower_count', int(follower_count))

        following_count = textify(hdoc.select('//div[@class="userNums"]//a[contains(text(), "Following ")]//strong'))
        if following_count:
            item.set('following_count', int(following_count))

        listed_count = textify(hdoc.select('//div[@class="userNums"]//a//strong[@class="listNum"]'))
        if listed_count:
            item.set('listed_count', int(listed_count))

        talk_list = ()
        key = hdoc.select('//ul[@id="talkList"]//li//div[@class="pubInfo"]//a[@class="time"][not(contains(@rel, "1"))]')
        key = [parse_date(textify(k).replace('The', '').replace('the', '').replace('.', '')) for k in key]
        if key:
            value = hdoc.select('//ul[@id="talkList"]//li//div[@class="msgBox"]//div[@class="msgCnt"]')
            value = [textify(v).split(': ')[-1] for v in value]
        talk_list = zip(key, value)
        item.set('talk_list', talk_list)

        verified = xcode(textify(hdoc.select('//div[@class="vDateBox"]')))
        item.set('verified', verified)

        user_information = hdoc.select('//div[@class="RUI"]//li')
        user_information = [xcode(textify(i)).replace(': ', ':') for i in user_information]
        item.set('user_information', user_information)

        image_url = textify(hdoc.select('//li[@class="pic"]//a/img/@src'))
        item.set('image_url', image_url)

        navigation_urls = hdoc.select('//div[@class="pubInfo"]//a[@class="zfNum"]/@href')
        for url in navigation_urls:
            url = textify(url)
            get_page('tencent_browse', url)

        yield item.process()
