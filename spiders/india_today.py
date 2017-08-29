from juicer.utils import*
class IndiaToday(JuicerSpider):
    name = "india_today"
    start_urls = ['http://indiatoday.intoday.in/section/114/1/india.html']
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@class="homeleft"]//div[@class="boxcont"]//div[@class="box"]//div[@class="innerbox"]//a//@href')
        for url in urls:
            print url
            yield Request(url,self.parse_details,response)
    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="strwapper"]//div[@class="strleft"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="mediumcontent"]/p/text()'))
        dt_added = textify(hdoc.select('//div[@class="strstrap"]//text()'))
       # author = textify(hdoc,.select(''))
        print "title=======",title
        print "text========",text
        print "date========",dt_added
       # print author

