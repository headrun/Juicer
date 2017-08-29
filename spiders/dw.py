from juicer.utils import*
class dw(JuicerSpider):
    name = "dw"
    start_urls = ['http://www.daijiworld.com/news/news_disp.asp?n_id=276351']
    def parse(self,response):
        hdoc = HTML(response)
        url = 'http://www.daijiworld.com/news/news_disp.asp?n_id=276351'
        print url
        yield Request(url,self.parse_next,response)
    def parse_next(self,response):
        hdoc = HTML(resposne)
        print "info"
        title = textify(hdoc.select('//td//h1//text()'))
        print title
