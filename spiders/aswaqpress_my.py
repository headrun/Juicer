from juicer.utils import *
from dateutil import parser

class Aswaqpress(JuicerSpider):
    name = 'aswaqpress_my'
    start_urls = ['http://www.aswaqpress.com/articles/category/14','http://www.aswaqpress.com/articles/category/17','http://www.aswaqpress.com/articles/category/24']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//a[@class="artIconDiv "]/@href').extract()
        for link in links:
            if 'http' not in link:link = 'http://www.aswaqpress.com' + link
            yield Request(link,self.details,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="pageDiv"]//div[@class="pageHeader"]/text()')).strip(u'\u0622\u062e\u0631 \u0627\u0644\u0645\u0642\u0627\u0644\u0627\u062a')
        author = textify(hdoc.select('//div[@class="pageDiv"]//a[@class="authorIcon"]/text()'))
        date = textify(hdoc.select('//a[@class="dateIcon"]/text()'))
        dt_added = get_timestamp(parse_date(date,dayfirst=True) - datetime.timedelta(hours=8))
        text = textify(hdoc.select('//div[@class="pageBody"]//p[contains(@style,"text-align")]//text()')) or textify(hdoc.select('//div[@class="pageBody"]//p[@dir="RTL"]//text()')) or textify(hdoc.select('//div[@class="pageBody"]/h1[@dir="RTL"]//text()')) or textify(hdoc.select('//div[@class="pageBody"]/div[@class="articleInfoDiv"]/following-sibling::p//text()'))

        if dt_added < get_current_timestamp()-86400*30:
        '''
            item = Item(response)
            item.set('url',response.url)
            item.set('title',xcode(title))
            item.set('author',{'name':xcode(author)})
            item.set(('date',xcode(dt_added)))
            item.set('text',xcode(text))
            '''
