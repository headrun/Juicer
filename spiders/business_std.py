from juicer.utils import *
from dateutil import parser

class BusinessStd(JuicerSpider):
    name = "business_std"
    start_urls = ['http://www.business-standard.com/technology-news','http://www.business-standard.com/technology-features','http://www.business-standard.com/technology-gadgets-gizmos','http://www.business-standard.com/technology-personal','http://www.business-standard.com/category/politics-news-north-1550102.htm','http://www.business-standard.com/category/politics-news-south-1550103.htm','http://www.business-standard.com/category/politics-news-east-1550104.htm','http://www.business-standard.com/category/politics-news-west-1550105.htm','http://www.business-standard.com/category/politics-news-central-1550106.htm','http://www.business-standard.com/category/politics-news-north-east-1550107.htm','http://www.business-standard.com/pf-news','http://www.business-standard.com/multi-category/358.htm','http://www.business-standard.com/multi-category/359.htm','http://www.business-standard.com/category/pf-features-mfs-1140212.htm','http://www.business-standard.com/multi-category/361.htm','http://www.business-standard.com/multi-category/362.htm','http://www.business-standard.com/multi-category/363.htm','http://www.business-standard.com/category/specials-brand-w-10906.htm','http://www.business-standard.com/category/companies-opinion-10104.htm','http://www.business-standard.com/category/markets-features-10610.htm','http://www.business-standard.com/category/international-news-markets-1160103.htm','http://www.business-standard.com/category/markets-news-1060101.htm','http://www.business-standard.com/category/specials-beducation-10914.htm','http://www.business-standard.com/multi-category/1108.htm','http://www.business-standard.com/category/opinion-chinese-1050601.htm','http://www.business-standard.com/category/opinion-letters-1050501.htm','http://www.business-standard.com/category/specials-pe-vc-10976.htm','http://www.business-standard.com/category/companies-start-ups-10113.htm','http://www.business-standard.com/category/specials-strategist-10903.htm','http://www.business-standard.com/category/specials-digital-c-10907.htm','http://www.business-standard.com/category/opinion-columns-1050201.htm','http://www.business-standard.com/category/specials-aviation-10929.htm','http://www.business-standard.com/category/specials-defence-10974.htm','http://www.business-standard.com/category/specials-weekend-10904.htm','http://www.business-standard.com/category/markets-ipos-news-1061101.htm','http://www.business-standard.com/opinion-editorial','http://www.business-standard.com/opinion-financial-x-ray','http://www.business-standard.com/opinion-lunch']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="section m0p0 bdrBNone article-container"]//h2//a//@href')
        if not urls:
            urls = hdoc.select('//div[@class="section bdrBNone pB0"]//h2//a//@href')
        if not urls:
            urls = hdoc.select('//div[@class="section m0p0 bdrBNone "]//h2//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="topNewsBox bdrBNone mB0"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="colL_MktColumn2"]//text()'))
        dt_added =textify(hdoc.select('//div[@class="byline mT5 mB5"]//div//text()'))
        author = textify(hdoc.select('//div[@class="byline mT5 mB5"]/strong/a/text()'))
        if not author:
            author = textify(hdoc.select('//div[@class="byline mT5 mB5"]/strong/text()'))
            author = author.replace("|","").strip()
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        yield item.process()
