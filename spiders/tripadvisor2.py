from juicer.utils import*
class TripadvisorIndia(JuicerSpider):
    name = "tripadvisorindia"
    start_urls = "http://www.tripadvisor.in/Hotels-g293860-India-Hotels.html"
    def parse(self,response):
        hdoc = HTML(response)
        self.latest_dt=parse_date('2014-11-01')
        if self.latest_dt:self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))
        nodes = hdoc.select('//div[@class="maincontent rollup"]//div[@class="geos_grid"]//div[@class="geos_row"]//div[@class="geo_entry"]')
        for node in nodes:
            url=node.select('.//div[@class="geo_name"]//a//@href')
            print url
            yield Request(url,self.parse_next,response)
    def parse_next(self,response):
        hdoc = HTML(response)
        links = hdoc.select('//div[@id="ACCOM_OVERVIEW"]//div[@class="metaLocationInfo"]//div[@class="quality wrap"]//a//@href')
        for link in links:
            #print link
            yield Request(link,self.parse_terminal,response)
    
    def parse_terminal(self,response):
        hdoc = HTML(response)
        posts = hdoc.select('//div[@id="REVIEWS"]//div[contains(@id,"review_")]//div[@class="wrap"]//div[@class="quote"]')
        for post in posts:
            post_date=textify(post.select('.//div[@class="rating reviewItemInline"]//span[@class="ratingDate relativeDate"]'))
            post_date = parse_date(str(re.sub(r'Reviewed', '', post_date)).strip(), True)
            #if not post_date:
            #    continue
            #urls= post.select('.//div[@class="wrap"]//div[@class="quote"]//a//href')
            #for url in urls:
            if post_date >= self.latest_dt:
                print post_date
                #url= textify(post.select('.//div[@class="wrap"]//div[@class="quote"]//a//href'))
                #for url in urls:
                title = textify(post.select('//div[@class="wrap"]//div[@class="quote"]//text()'))
                title = title.encode('utf8').decode('ascii','ignore')
                print "title====",title
                text = textify(post.select('//div[@class="entry"]//p/text()'))
                text = textify(text).encode('utf8').decode('ascii','ignore')
                print "text=======",text
                print "url===========",response.url
                #post_id = textify('./')
