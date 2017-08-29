from juicer.utils import*
from dateutil import parser
import ast

class Nikkei(JuicerSpider):
    name = 'nikkei'
    start_urls =['http://www.nikkei.com/news/category/']

    def parse(self,response):
        hdoc = HTML(response)
        links = hdoc.select(`//div[@class="cmn-top_news cmn-clearfix cmn-middle_mark"]/h4/a/@href'))
        for link in links:
            import pdb;pdb.set_trace()
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTMl(response)
        title = textify(hdoc.select('//div[@class="cmn-section cmn-indent "]/h1[@itemprop="name"]/span/text()'))
        text = textify(hdoc.select('//div[@class="cmn-section cmn-indent "]/div[@itemprop="articleBody"]/p/text()'))
        date = textify(hdoc.select('//div[@class="cmn-section cmn-indent "]/dl[@class="cmn-article_status cmn-clearfix"]/dd[@class="cmnc-publish"]/text()'))
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))


    print '/n'
    print response.url
    print 'title', xcode(title)
    print 'text', xcode(text)
    print 'dt_added', xcode(dt_added)


