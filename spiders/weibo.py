from juicer.utils import *
import lxml.html

class Weibo(JuicerSpider):
    name = 'weibo'
    start_urls = ['http://huati.weibo.com/']

    def parse(self, response):
        hdoc = HTML(response)

        urls = hdoc.select('//div[@class="topic_navlist_update"]/ul/li/a/@action-data')
        for url in urls[:1]:
            url = 'http://huati.weibo.com/aj_topiclist/big?' + textify(url)
            yield Request(url, self.parse_forum, response, headers={"X-Requested-With":"XMLHttpRequest"})

    def parse_forum(self, response):
        hdoc = json.loads(response.body)
        hdoc = hdoc['data']['html']
        hdoc = lxml.html.fromstring(hdoc)

        titles = hdoc.xpath('//li[@action-type="show-topic"]//div[@class="hd"]/a/@title')
        for title in titles[:1]:
            title = textify(title)
            url = 'http://huati.weibo.com/aj_topic/list?_pv=1&keyword=%s&match_area=0&ori=1&hasv=0&atten=0&mining=0&istag=2&is_olympic=0&topicName=%s&_t=0' % (title, title)
            yield Request(url, self.parse_post, response, headers={"X-Requested-With":"XMLHttpRequest"}, meta = {"title": title})

    def parse_post(self, response):
        hdoc = json.loads(response.body)
        hdoc = hdoc['data']['html']
        hdoc = lxml.html.fromstring(hdoc)

