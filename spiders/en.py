from juicer.utils import *
from dateutil import parser
class ebela_in(JuicerSpider): 
name = 'ebela_in'
 start_urls = 'http://ebela.in/lifestyle'#['http://ebela.in/entertainment/hollywood','http://ebela.in/entertainment/bollywood','http://e    bela.in/entertainment/tollywood','http://ebela.in/lifestyle']  
 def parse(self,response):
   hdoc = HTML(response)
     hdoc = HTML(response)
     links = hdoc.select('//div[@class="black_conetent_text_large"]/a/@href')
     for link in links:
     yield Request(link,self.parse_details,response)
      def parse_details(self,response):
      hdoc = HTML(response)
      title = textify(hdoc.select('//h1[@class="story_topstory_head"]/text()'))
      text = textify(hdoc.select('//div[contains(@class,"story_description")]//text() | //div[@class="story_detail_section"]//text()'))
      date = textify(hdoc.select('//script[@type="application/ld+json"]/text()'))
      date = ast.literal_eval(date)["datePublished"]
       import pdb;pdb.set_trace()
       dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
       print response.url
       print 'title',xcode(title)
       print 'text',xcode(text)
       print 'dt_added',xcode(dt_added)


