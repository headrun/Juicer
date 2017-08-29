from juicer.utils import *
from dateutil import parser

class SogouTerminal(JuicerSpider):
    handle_httpstatus_list = [500, 502]
    name = "sogou_terminal"

    def __init__(self, *args, **kwargs):
         JuicerSpider.__init__(self, *args, **kwargs)

    def parse(self, response):
        hdoc = HTML(response)
        if response.status != 200:
            yield Request(response.url, self.parse_details, response, dont_filter=True)

        try:
            title = textify(hdoc.select("//h2[@class='rich_media_title']/text()")[0])
        except:
            title = ''
        text = textify(hdoc.select("//div[@class='rich_media_content']//p//text()"))
        dt_added = textify(hdoc.select('//div[@class="rich_media_meta_list"]//em[@id="post-date"]/text()'))
        author = textify(hdoc.select('//div[@class="rich_media_meta_list"]//a[@id="post-user"]/text()'))

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))

        got_page(self.name, url=response.request.url)
        #got_page(self.name, url=response.url)
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])

        if title and text:
            yield item.process()
