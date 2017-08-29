from juicer.utils import *

class IdenticaGroupSpider(JuicerSpider):
    name = 'identica_group'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        group_title = textify(hdoc.select('//p[@class="profile_block_name"]//a'))
        item.set('group_title', group_title)

        group_location = textify(hdoc.select('//p[@class="profile_block_location"]'))
        item.set('group_location', group_location)

        group_description = textify(hdoc.select('//p[@class="profile_block_description"]'))
        item.set('group_description', group_description)

        group_feed_url = textify(hdoc.select('//li//a[contains(text(), "RSS 2.0")]/@href'))
        item.set('group_feed_url', group_feed_url)

        group_image_url = textify(hdoc.select('//img[@class="ur_face"]/@src'))
        item.set('group_image_url', group_image_url)

        group_users = hdoc.select('//span[@class="vcard author"]//a[@class="url"]/@href')
        group_users = [textify(g) for g in group_users]

        for group_user in group_users:
            get_page('identica_terminal', group_user)

        next_group = textify(hdoc.select('//li[@class="nav_next"]//a/@href'))
        if next_group:
            get_page(self.name, next_group)

        admins = hdoc.select('//span[@class="vcard"]//a[@rel="contact member"]/@href')
        admins = [textify(a) for a in admins]

        for admin in admins:
            get_page('identica_terminal', admin)

        group_members = textify(hdoc.select('//h2//a[contains(text(), "Members")]/@href'))
        yield Request(group_members, self.parse_members, response)

        yield item.process()

    def parse_members(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        members = hdoc.select('//img//parent::a[@class="url entry-title"]/@href')
        members = [textify(m) for f in members]

        for member in members:
            get_page('identica_terminal', member)

        next_member = textify(hdoc.select('//li[@class="nav_next"]//a/@href'))
        if next_member:
            get_page(self.name, next_member)
