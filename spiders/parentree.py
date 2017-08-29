from juicer.utils import *
from dateutil import parser

class Parentree(JuicerSpider):
    name = "parentree"
    start_urls = ['http://www.parentree.in/India/Bangalore/Schools/62-vidyashilp-academy','http://www.parentree.in/India/Bangalore/Schools/79-greenwood-high','http://www.parentree.in/India/Bangalore/Schools/3115-sarala-birla-academy','http://www.parentree.in/India/Bangalore/Schools/66-st-joseph-boys-high-school','http://www.parentree.in/India/Bangalore/Schools/63-vidya-niketan-school','http://www.parentree.in/India/Bangalore/Schools/65-the-valley-school-kfi','http://www.parentree.in/India/Bangalore/Schools/3471-brigade-school-malleswaram']
    def parse(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1//text()'))
        no_reviews = textify(hdoc.select('//h2[contains(text(),"reviews")]//text()'))
        if no_reviews:
            no_reviews = no_reviews.split(' ')
            no_reviews = no_reviews[0]
            no_reviews = int(no_reviews)
        else:
            no_reviews = 0
        latest_date = '2014-06-01'
        i = 1
        for i in range(no_reviews):
            dt_added = textify(hdoc.select('//time//@datetime')[i])
            if dt_added >=latest_date:

                text = textify(hdoc.select('//div[@class="row-fluid"]//span[@itemprop="reviewBody"]//text()')[i])
                dt_added = textify(hdoc.select('//time//@datetime')[i])
                author = textify(hdoc.select('//span[@itemprop="author"]//text()')[i])
                i = i+1
                print title
                print dt_added
                item = Item(response)
                item.set('title', xcode(title))
                item.set('text', xcode(text))
                item.set('dt_added', dt_added)
                item.set('author.name',xcode(author))
                item.set('url', response.url)
                #yield item.process()

