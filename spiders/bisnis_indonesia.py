from juicer.utils import*
from dateutil import parser

class Bisnis_ID(JuicerSpider):
    name = 'bisnis_indonesia' 
    start_urls = []
    main_link = 'http://www.bisnis.com/loadmore/home?page=%s'
    for page_num in range(1,1000):
        url = main_link%(page_num)
        start_urls.append(url)
    import pdb;pdb.set_trace()
    #start_urls =dd ['http://www.bisnis.com/loadmore/home?page=15&_=1488607948869']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="col-sm-7"]')
        for node in nodes:
            date = textify(node.select('./div[@class="time"]/text()'))
            date = date=date.replace('|','')            
            print date
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                continue
            link = textify(node.select('./h2/a/@href'))
            print link
            yield Request(link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="title"]//text()'))
        text = textify(hdoc.select('//div[@class="col-sm-10"]//p//text()'))
        date = textify(hdoc.select('//div[@class="wrapper-date"]//text()')) 
        author = textify(hdoc.select('//div[@class="author"]/span/text()'))
        import pdb;pdb.set_trace()

        """start_urls = []
            main_link = 'http://www.bisnis.com/loadmore/home?page=%s&_=1488608583%s'
                
                    for page_num in range(10):
                            for id1 in range(215,230):
                                        url = main_link%(page_num,id1)
                                                    print url
                                                                import pdb;pdb.set_trace()
                                                                    """


