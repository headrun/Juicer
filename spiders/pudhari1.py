from juicer.utils import *
from dateutil import parser

class PudhariIn(JuicerSpider):
    name = 'pudhari1'
    start_urls =['http://www.pudhari.news/mumbai.php','http://www.pudhari.news/pune.php','http://www.pudhari.news/kolhapur.php','http://www.pudhari.news/sangli.php','http://www.pudhari.news/solapur.php','http://www.pudhari.news/satara.php','http://www.pudhari.news/ahmadnagar.php','http://www.pudhari.news/jalna.php','http://www.pudhari.news/marathvada.php','http://www.pudhari.news/aurangabad.php','http://www.pudhari.news/vidarbha.php','http://www.pudhari.news/nashik.php','http://www.pudhari.news/goa.php','http://www.pudhari.news/konkan.php','http://www.pudhari.news/belgaon.php','http://www.pudhari.news/national.php','http://www.pudhari.news/international.php','http://www.pudhari.news/sports.php','http://www.pudhari.news/soneri.php','http://www.pudhari.news/sampadakiy.php','http://www.pudhari.news/bahar.php','http://www.pudhari.news/arogya.php','http://www.pudhari.news/kasturi.php','http://www.pudhari.news/ankur.php','http://www.pudhari.news/edudisha.php','http://www.pudhari.news/bhumiputra.php','http://www.pudhari.news/youthworld.php','http://www.pudhari.news/crimediary.php','http://www.pudhari.news/arthabhan.php']

    def parse(self,response):
        hdoc = HTML(response)
        categories =hdoc.select('//div[@class="col-sm-6 col-md-6 col-lg-6 col-xs-6"]/h6/a/@href').extract() or hdoc.select('//h4/a[@target="_blank"]/@href').extract()
        for cat in categories:
            if 'http' not in cat: cat = 'http://www.pudhari.news/' +  cat
            yield Request(cat,self.parse_links,response, dont_filter = True)

    def parse_links(self,response):
        #ref_url = response.request.url
        hdoc = HTML(response)
        title=textify(hdoc.select('//div[@class="col-md-12"]/h3[@style]//text()'))
        dt=textify(hdoc.select('//div[@class="col-md-9"]//text()'))
        date = dt.partition('|')[0]
        date = date.replace('Published On:','')
        if not dt:
            dte = textify(hdoc.select('//div[@class="col-md-8"]/h5/text()'))
            if 'By' in dte:
                date= dte.partition('|')[2]
                date = date.replace('Published Date:','')
        auth = textify(hdoc.select('//div[@class="col-md-8"]/h5/text()'))
        author = auth.partition('|')[0]
        author = author.replace('By','')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
        ext_txt = textify(hdoc.select('//div[@style="margin-left:10px;"]//p//text()'))
        text = textify(hdoc.select('//div[@style="text-align:justify;width:652px;margin-left:-12px"]//p//text()'))
        text = ext_txt + ' ' + text

        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title)
        item.set('text',xcode(text))
        item.set('dt_added',xcode(dt_added))
        item.set('author',{'name':xcode(author)})
        item.set('xtags',['news_sourcetype_manual','india_country_manual'])
        yield  item.process()
