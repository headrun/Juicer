from juicer.utils import *

class PlurkTerminalSpider(JuicerSpider):
    name = 'plurk_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        item.set('sk', sk)
        feed_url = response.url + '.xml'
        item.set('feed_url', feed_url)
        title = xcode(textify(hdoc.select('//h1[@id="full_name"]')))
        item.set('title', title)
        item.textify('gender', '//span[@id="m_or_f"]')
        item.textify('location', '//span[@id="location"]')
        item.textify('image_url', '//div[@id="dash-profile"]//img[@id="profile_pic"]/@src')
        user_links = hdoc.select('//p[@id="about_me"]//a/@href')
        user_links = [textify(l) for l in user_links]
        item.set('user_links', user_links)
        follows_count = textify(hdoc.select('//div[@class="show_all_friends"]//a/text()[contains(., "friends")]')).replace('Show all friends (', '')
        follows_count = follows_count.replace(')', '')
        item.set('follows_count', int(follows_count))
        fans_count = textify(hdoc.select('//div[@class="show_all_friends"]//a/text()[contains(., "fans")]')).replace('Show all fans (', '')
        fans_count = fans_count.replace(')', '')
        item.set('fans_count', int(fans_count))
        plurk_information = {}
        nodelist = hdoc.select('//div[@id="dash-stats"]//table//tr')
        for node in nodelist:
            key = textify(node.select('.//th')).replace(':', '')
            if key:
                value = textify(node.select('.//td'))
                plurk_information[key] = value
        plurk_information['Profile views'] = int(plurk_information.get('Profile views'))
        plurk_information['Friends invited'] = int(plurk_information.get('Friends invited') or 0)
        plurk_information['Plurks'] = int(plurk_information.get('Plurks') or 0)
        plurk_information['Plurk responses'] = int(plurk_information.get('Plurk responses') or 0)
        plurk_information['Last login'] = parse_date(plurk_information.get('Last login'))
        plurk_information['Member since'] = parse_date(plurk_information.get('Member since'))
        #print plurk_information
        item.set('plurk_information', plurk_information)
        about_author = xcode(textify(hdoc.select('//p[@id="about_me"]')))
        if about_author:
            item.set('about_author', about_author)

        follows_url = textify(hdoc.select('//div[@class="show_all_friends"]//a/@href[contains(., "/showFriendsBasic?")]'))
        follows_url = 'http://www.plurk.com' + follows_url
        item.set('follows_url', follows_url)
        get_page('plurk_follows', follows_url)

        fans_url = textify(hdoc.select('//div[@class="show_all_friends"]//a/@href[contains(., "/showFansBasic?")]'))
        fans_url = 'http://www.plurk.com' + fans_url
        item.set('fans_url', fans_url)
        get_page('plurk_fans', fans_url)

        yield item.process()
