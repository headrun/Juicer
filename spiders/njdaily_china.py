from juicer.utils import *
from dateutil import parser

class Njdaily(JuicerSpider):
    name = 'njdaily_china'
    start_urls = ['http://www.njdaily.cn/nanjing/shehui/','http://www.njdaily.cn/nanjing/szzh/','http://www.njdaily.cn/nanjing/rsrm/','http://www.njdaily.cn/nanjing/ldhd/','http://www.njdaily.cn/nanjing/minsheng/','http://www.njdaily.cn/comment/whkj/','http://www.njdaily.cn/comment/gdyjy/','http://www.njdaily.cn/comment/szcj/','http://www.njdaily.cn/comment/shms/','http://www.njdaily.cn/news/guonei/','http://www.njdaily.cn/life/3csh/','http://www.njdaily.cn/health/js/','http://www.njdaily.cn/health/jkzx/','http://www.njdaily.cn/life/whjs/','http://www.njdaily.cn/edu/lxzx/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//ul[@class="list"]//li//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="content-main"]//h1//text()'))
        text = textify(hdoc.select('//div[@id="articleText"]//p//text()'))
        dt_added = textify(hdoc.select('//span[@class="post-time"]//text()'))
        author = textify(hdoc.select('//div[@class="f-fr"]/span[@class="info-span"]/text()'))
        if author:
            author = textify(hdoc.select('//div[@class="f-fr"]/span[@class="info-span"]/text()')[0])
            author = author.split(u'\uff1a')
            author.pop(0)
            author = ''.join(author)
        else:
            author= textify(hdoc.select('//p[@class="txt-r f-r fs-12 cor-999"]/text()'))
            author = author.split(u'\uff1a')
            author.pop(0)
            author = ''.join(author)
            dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

            item = Item(response)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', dt_added)
            item.set('author.name',xcode( author))
            item.set('url', response.url)
            yield item.process()

