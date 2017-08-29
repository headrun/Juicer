from juicer.utils import *
from dateutil import parser

class JbTalks(JuicerSpider):
    handle_httpstatus_list = [500, 502]
    name = "sogou"
    start_urls = ['http://weixin.sogou.com/weixin?query=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%E4%B9%90%E5%9B%AD&type=2',
                  'http://weixin.sogou.com/weixin?type=2&query=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E6%96%AF%E5%B0%BC%E4%B9%90%E5%9B%AD',
                  'http://weixin.sogou.com/weixin?query=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%E4%B9%90%E5%9B%AD&type=2',
                  'http://weixin.sogou.com/weixin?type=2&query=%E4%B8%8A%E6%B5%B7%E5%A4%A7%E6%82%A6%E5%9F%8E',
                  'http://weixin.sogou.com/weixin?type=2&query=%E4%B8%8A%E6%B5%B7K11',
                  'http://weixin.sogou.com/weixin?type=2&query=%E8%A5%BF%E5%8D%95%E5%A4%A7%E6%82%A6%E5%9F%8E',
                  'http://weixin.sogou.com/weixin?type=2&query=%E6%9C%9D%E9%98%B3%E5%A4%A7%E6%82%A6%E5%9F%8E',
                  'http://weixin.sogou.com/weixin?type=2&query=%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
                  'http://weixin.sogou.com/weixin?type=2&query=%E5%87%AF%E5%BE%B7MALL',
                  'http://weixin.sogou.com/weixin?type=2&query=%E5%87%AF%E5%BE%B7%E5%92%8C%E5%B9%B3%E5%B9%BF%E5%9C%BA',
                  'http://weixin.sogou.com/weixin?type=2&query=%E5%87%AF%E5%BE%B7%E5%B9%BF%E5%9C%BA',
                  'http://weixin.sogou.com/weixin?type=2&query=%E5%87%AF%E5%BE%B7%E9%BE%99%E4%B9%8B%E6%A2%A6%E8%99%B9%E5%8F%A3',
                  'http://weixin.sogou.com/weixin?query=%E5%88%80%E5%A1%94%E4%BC%A0%E5%A5%87&type=2']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.cutoff_dt = None

    def parse(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        if response.status != 200:
            yield Request(response.url, self.parse, response, dont_filter=True)

        urls = hdoc.select('//div[@class="results"]//h4//a/@href')
        for url in urls:
            yield Request(url, self.parse_details, response)

        next_url = hdoc.select('//div[@id="pagebar_container"]//a[@id="sogou_next"]/@href')
        if next_url:
            yield Request(next_url, self.parse, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        if response.status != 200:
            yield Request(response.url, self.parse_details, response, dont_filter=True)

        title = textify(hdoc.select("//h2[@class='rich_media_title']/text()"))
        text = textify(hdoc.select("//div[@class='rich_media_content']//p//text()"))
        dt_added = textify(hdoc.select('//div[@class="rich_media_meta_list"]//em[@id="post-date"]/text()'))
        author = textify(hdoc.select('//div[@class="rich_media_meta_list"]//a[@id="post-user"]/text()'))

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        import pdb;pdb.set_trace()

        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])

        #yield item.process()
