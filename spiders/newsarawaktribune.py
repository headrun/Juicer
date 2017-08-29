from juicer.utils import *
from dateutil import parser

class NewsArawaktribune(JuicerSpider):
    name = 'newsarawaktribune'
    start_urls = ['http://www.newsarawaktribune.com/prime/','http://www.newsarawaktribune.com/business/','http://www.newsarawaktribune.com/local/','http://www.newsarawaktribune.com/nation/','http://www.newsarawaktribune.com/sports/','http://www.newsarawaktribune.com/world/','http://www.newsarawaktribune.com/tribune2/']

    def parse(self,response):
        hdoc =  HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@id="section-sub-content"]/parent::td[@valign="top"]')
        for node in nodes:
            date = textify(node.select('./div[contains(text(),"Date Posted")]/text()')).split(':')[-1]
            date_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('./div/a[@title]/@href'))
            yield Request(link,self.details,response)

        nxt_pg = textify(hdoc.select('//a[@title="Next page"]/@href'))
        if nxt_pg and is_next:
            nxt_pg = 'http://www.newsarawaktribune.com' + nxt_pg
            yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//p[@class="news-details-title"]/text()'))
        dt = textify(hdoc.select('//div[contains(text(),"Date Posted")]/text()')).split(':')[-1]
        dt_added = get_timestamp(parse_date(dt) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//div[contains(@style,"font-family")]/span//text()'))
        text = textify(hdoc.select('//div[contains(@style,"text-align:justify")]//text()'))

        item = Item(response) 
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        item.set('author',xcode(author))
        item.set('text',xcode(text))
