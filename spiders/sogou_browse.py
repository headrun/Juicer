from juicer.utils import *
from dateutil import parser
import urllib
import simplejson

def get_starturls():
    data = urllib.urlopen('http://data.cloudlibs.com/sea/?action=get&key=3DD578J7N13N97RD3COQX37P9E7IWXZFN1YQPE5F&source=weixin').read()
    data = simplejson.loads(data)

    url = 'http://weixin.sogou.com/weixin?query=%s&type=2'

    urls = []

    for _url in data['result']:
        urls.append(url %urllib.quote(_url.encode('utf8')))
    return urls

class SogouBrowse(JuicerSpider):
    handle_httpstatus_list = [500, 502]
    name = "sogou_browse"
    start_urls = get_starturls()

    def __init__(self, *args, **kwargs):
         JuicerSpider.__init__(self, *args, **kwargs)
         self.cutoff_dt = None

    def parse(self, response):
        hdoc = HTML(response)
        if response.status != 200:
            yield Request(response.url, self.parse, response, dont_filter=True)

        urls = hdoc.select('//div[@class="results"]//h4//a/@href')
        for url in urls:
            #yield Request(url, self.parse_details, response)
            get_page('sogou_terminal', textify(url))

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

        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])

        yield item.process()
