from juicer.utils import *
from dateutil import parser
class ABPNews(JuicerSpider):
    name = "apb_news"
    start_urls = ['http://www.abplive.in/india/','http://www.abplive.in/World/','http://www.abplive.in/sports/','http://www.abplive.in/lifestyle/','http://www.abplive.in/movies/','http://www.abplive.in/tv/','http://www.abplive.in/business/','http://www.abplive.in/gadget/','http://www.abplive.in/crime/', 'http://www.abplive.in/health/']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="main"]//div[@class="span6 "]//h4[@class="small"]//a//@href')
        import pdb;pdb.set_trace()
        for url in urls:
            yield Request(url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="widget storyContent article"]//h1//text()'))
        text1 = textify(hdoc.select('//div[@class="body "]//p//text()')[0])
        text = textify(hdoc.select('//div[@class="body "]/p/text()'))
        text = text1 + text
        dt_added = textify(hdoc.select('//p[@class="dateline muted"]//text()'))
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()

