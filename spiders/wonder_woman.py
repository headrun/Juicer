from juicer.utils import*
from dateutil import parser

class WonderWoman(JuicerSpider):
    name = "wonder_women"
    start_urls = ['http://wonderwoman.intoday.in/category/pregnancy/1/206.html','http://wonderwoman.intoday.in/category/parenting/1/207.html','http://wonderwoman.intoday.in/category/good-health/1/208.html','http://wonderwoman.intoday.in/recipesection/135/1/recipes.html','http://wonderwoman.intoday.in/category/budgeting/1/209.html','http://wonderwoman.intoday.in/category/home-improvement/1/210.html','http://wonderwoman.intoday.in/category/home-improvement/1/210.html','http://wonderwoman.intoday.in/category/stress-&-fitness/1/213.html','http://wonderwoman.intoday.in/category/work-wise/1/214.html','http://wonderwoman.intoday.in/category/beauty/1/215.html','http://wonderwoman.intoday.in/category/celeb-style/1/217.html','http://wonderwoman.intoday.in/category/celeb-style/1/217.html','http://wonderwoman.intoday.in/category/sex-secrets/1/221.html','http://wonderwoman.intoday.in/category/know-your-man/1/222.html','http://wonderwoman.intoday.in/category/love-truths/1/223.html','http://wonderwoman.intoday.in/category/on-your-honeymoon/1/225.html','http://wonderwoman.intoday.in/category/on-your-honeymoon/1/225.html','http://wonderwoman.intoday.in/category/wedding-planner/1/227.html','http://wonderwoman.intoday.in/category/potpourri/1/228.html','http://wonderwoman.intoday.in/category/fashion-police/1/229.html','http://wonderwoman.intoday.in/category/celeb-gossip/1/230.html']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td//div[@class="strlblock"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="strheadline"]//h1//text()'))
        text = textify(hdoc.select('//div[@id="womanstory"]//p//text()'))
        author = textify(hdoc.select('//div[@id="womanstory"]//div[@class="byline"]//text()'))
        if not title:
            title = textify(hdoc.select('//div[@class="strheadline"]/text()'))

        item =Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set("author.name",author)
        item.set('url', response.url)
        yield item.process()
