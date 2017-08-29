from juicer.utils import *

class PlurkFansSpider(JuicerSpider):
    name = 'plurk_fans'

    def parse(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)
        got_page(self.name, response)

        user_id = get_request_url(response).split('id=')[-1]

        fans = []
        nodes = hdoc.select('//ul[@class="random_users"]//li//img//parent::a/@href')
        for node in nodes:
            fans_url = textify(node)
            get_page('plurk_terminal', fans_url)
            yield Request(node, self.parse_fan, response, meta = {'user_id':user_id})

        next_url = textify(hdoc.select('//div[@id="controller"]//a[contains(text(), "Next page")]/@href'))
        next_url = 'http://www.plurk.com' + next_url
        if next_url:
            get_page(self.name, next_url)

    def parse_fan(self, response):
        hdoc = HTML(response)
        item = Item(response, HTML)

        sk1 = get_request_url(response).split('/')[-1]
        user_id = response.meta.get('user_id')
        item.set('user_id', user_id)

        sk = sk1 + '---' + user_id
        item.set('sk', sk)

        fan_id = sk1
        item.set('fan_id', fan_id)

        #yield item.process()
