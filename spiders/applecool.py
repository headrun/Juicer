import datetime
from juicer.utils import *


class Applecool(JuicerSpider):
    name = "applecool"
    start_urls = ['http://sg.applecool.com/']


    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)

        check_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_time - oneweek_diff

    def parse(self, response):
        hdoc = HTML(response)
        links = hdoc.select_urls(['//a[contains(@href,"category")]/@href'],response)
        for link in links:
            yield Request(link, self.parse_next, response)

    def parse_next(self, response):
        hdoc = HTML(response)
        listings = hdoc.select('//div[@class="cat_list"]/ul/li')

        for listing in listings:
            posted_dt = textify(listing.select(".//span[@class='date fr']//text()[contains(string(),'-')]"))
            posted_dt = re.findall(r'(\d.*)',posted_dt)
            posted_dt = parse_date(posted_dt[0])
            if posted_dt > self.cutoff_dt:
                title = textify(hdoc.select('//title/text()'))
                post_link = textify(listing.select(".//a/@href"))
                yield Request(post_link, self.parse_post, response, meta = {'title': title})

    def parse_post(self, response):
        hdoc = HTML(response)
        item = Item(response)
        num = {}
        title = textify(hdoc.select('//div[@class="art_title clearfix"]/h1'))
        item.set("title",title)

        data = textify(hdoc.select('//p[@class="info"]/text()')).split(" ")
        validity = re.findall(r'(\d+)',data[1])
        num['validity'] = int(validity[0])
        item.set("num", num)
        date = data[0].split('-')
        date = date[2]+"-"+date[1]+"-"+date[0]
        published_dt = parse_date(date)
        item.set( "dt_added",published_dt)

        tags =  hdoc.select('//div[@class="article-tag"]//a')
        tag_list = []
        for tag in tags:
            tg = textify(tag.select(".//text()"))
            tag_list.append(tg)
        item.set("tags", tag_list)

        text = textify(hdoc.select('//div[@class="article_content"]//p'))
        item.set("text",text)
        item.set('url', response.url)
        item.set('category', response.meta['title'])

        yield item.process()
