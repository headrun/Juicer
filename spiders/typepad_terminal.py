from juicer.utils import *

class TypepadTerminalSpider(JuicerSpider):
    name = 'typepad_terminal'

    def parse(self, response):
        hdoc = HTML(response)
        req_url = get_request_url(response)
        item = Item(response, HTML)
        sk = get_request_url(response).split('/')[-1]
        got_page(self.name, response)
        item.textify('user_name', '//div[@class="user-name fn"]')
        item.textify('address_lebel', '//div[@class="user-location adr label"]')
        item.textify('image_url', '//img[@class="photo"]//@src')
        item.textify('user_interest', '//div[@class="user-interests"]/text()')
        data = []
        nodes = hdoc.select('//div[@class="activity-item"]')
        for node in nodes:
            details = {}
            details['comment'] = textify(node.select('.//div[@class="excerpt-text"]'))
            details['comment_date'] = textify(node.select('.//div[@class="excerpt-meta"]/text()[contains(string(), "Commented")]')).replace('Commented', '')
            details['comment_date'] = details['comment_date'].split(' on')[0]
            details['uploaded_image'] = textify(node.select('.//div[@class="group-photo"]//img/@src'))
            details['uploaded_date'] = textify(node.select('.//div[@class="item-title reldate"]')).replace('Posted', '')
            details['uploaded_date'] = details['uploaded_date'].split('at')[0]
            data.append(details)
        item.set('data', data)
        url = hdoc.select('//div[@class="view-all-follower"]//a[contains(text(),"View all ")]/@href')
        yield Request(url, self.parse_first, response, meta={'item':item})

    def parse_first(self, response):
        hdoc = HTML(response)
        req_url = get_request_url(response)
        item = response.meta.get('item')
        following = [url for url in hdoc.select_urls('//div[@class="contact-name"]/a/@href')]
        item.set('following', following)
        for url in following:
            get_page('typepad_terminal', url)
        followers = [url for url in hdoc.select_urls('//div[@class="contact-name"]/a/@href')]
        item.set('followers',  followers)
        for url in  followers:
            get_page('typepad_terminal', url)

        yield item.process()
