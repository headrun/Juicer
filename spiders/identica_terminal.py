from juicer.utils import *

class IdenticaTerminalSpider(JuicerSpider):
    name = 'identica_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        sk = get_request_url(response).split('identi.ca/')[-1]
        item.set('sk', sk)

        title = textify(hdoc.select('//p[@class="profile_block_name"]//a'))
        item.set('title', title)

        location = textify(hdoc.select('//p[@class="profile_block_location"]'))
        item.set('location', location)

        description = textify(hdoc.select('//p[@class="profile_block_description"]'))
        item.set('description', description)

        tags = hdoc.select('//li[@class="hashptag mode-public"]//a')
        tags = [textify(t) for t in tags]
        item.set('tags', tags)

        tags_urls = hdoc.select('//li[@class="hashptag mode-public"]//a/@href')
        tags_urls = [textify(u) for u in tags_urls]
        item.set('tags_urls', tags_urls)

        blog_link = textify(hdoc.select('//a[@class="profile_block_homepage"]/@href'))
        item.set('blog_link', blog_link)

        image_url = textify(hdoc.select('//img[@class="ur_face"]/@src'))
        item.set('image_url', image_url)

        site_notice = hdoc.select('//div[@id="generic_section"]//li//a')
        site_notice = [textify(s) for s in site_notice]
        item.set('site_notice', site_notice)

        following_url = textify(hdoc.select('//a[contains(text(), "Following")]/@href'))
        item.set('following_url', following_url)
        get_page('identica_following', following_url)

        follower_url = textify(hdoc.select('//a[contains(text(), "Followers")]/@href'))
        item.set('follower_url', follower_url)
        get_page('identica_follower', follower_url)

        following_count = textify(hdoc.select('//a[contains(text(), "Following")]//parent::h2')).split(' ')[-1]
        if following_count:
            following_count = int(following_count)
            item.set('following_count', following_count)

        followers_count = textify(hdoc.select('//a[contains(text(), "Followers")]//parent::h2')).split(' ')[-1]
        if followers_count:
            followers_count = int(followers_count)
            item.set('followers_count', followers_count)

        groups_urls = hdoc.select('//ul[@class="entities groups xoxo"]//a[@class="url"]/@href')
        groups_urls = [textify(g) for g in groups_urls]
        item.set('groups_urls', groups_urls)

        for group_url in groups_urls:
            get_page('identica_group', group_url)

        groups_count = textify(hdoc.select('//div[@id="entity_groups"]//h2')).split(' ')[-1]
        if groups_count:
            groups_count = int(groups_count)
            item.set('groups_count', groups_count)

        lists = hdoc.select('//div[@id="entity_lists"]//ul//a')
        lists = [textify(l) for l in lists]
        item.set('lists', lists)
        if lists:
            item.set('lists_count', len(lists))

        lists_urls = hdoc.select('//div[@id="entity_lists"]//ul//a/@href')
        lists_urls = [textify(z) for z in lists_urls]
        item.set('lists_urls', lists_urls)

        #for lists_url in lists_urls:
            #get_page('identica_list', lists_url)

        statistics = {}
        nodelist = hdoc.select('//div[@id="entity_statistics"]//dl')
        for node in nodelist:
            key = textify(node.select('.//dt'))
            value = textify(node.select('.//dd'))
            statistics[key]= value
        statistics['User ID'] = int(statistics['User ID'])
        statistics['Member since'] = parse_date(statistics['Member since'])
        statistics['Notices'] = int(statistics['Notices'])
        statistics['Daily average'] = int(statistics['Daily average'])
        item.set('statistics', statistics)

        feed_url = textify(hdoc.select('//li//a[contains(text(), "RSS 2.0")]/@href'))
        item.set('feed_url', feed_url)

        yield item.process()
