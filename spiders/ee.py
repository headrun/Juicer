from juicer.utils import*
from dateutil import parser

class EenaduNews(JuicerSpider):
    name = "eenadu_news"
    start_urls = ['http://www.eenadu.net/andhra-pradesh-news.aspx','http://www.eenadu.net/telangana-news.aspx','http://www.eenadu.net/national-international/national-international-news.aspx','http://www.eenadu.net/crime-news/crime-news.aspx','http://www.eenadu.net/sports/sports.aspx','http://www.eenadu.net/movies/latest-movie-news.aspx','http://www.eenadu.net/sports/sports.aspx']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//li[contains(@class,"two-col-left-by-two")]//p/a[contains(@href, "=break")]/@href').extract()
        times = hdoc.select('//li[contains(@class,"two-col-left-by-two")]//p/span/text()').extract()
        for url,time in zip(nodes,times):
            if 'http' not in url:
                url = 'http://www.eenadu.net/' + url
            time = time.strip('[').strip(']').strip()
            date_added = get_timestamp(parse_date(xcode(time)) - datetime.timedelta(hours=5,minutes=30))
            yield Request(url, self.parse_details, response,meta={'date_added':date_added})

        nodes = hdoc.select('//li[contains(@class,"two-col-left-by-two")]//figcaption//a[contains(@href, "=break")]/@href').extract()
        times = hdoc.select('//li[contains(@class,"two-col-left-by-two")]//figcaption//span/span/text()').extract()
        for url,time in zip(nodes,times): 
            if 'http' not in url:
                url = 'http://www.eenadu.net/' + url
            time = time.strip('[').strip(']').strip()
            date_added = get_timestamp(parse_date(xcode(time)) - datetime.timedelta(hours=5,minutes=30))
            yield Request(url, self.parse_details, response,meta={'date_added':date_added})

    def parse_details(self,response):
        hdoc = HTML(response)
        text = textify(hdoc.select('//span[contains(@id, "PDSAI")]//font[@face="EenaduU"]//font/text()').extract()).strip().encode('utf-8')
        title = textify(hdoc.select('//span[contains(@id, "PDSAI")]//center//font[@face="EenaduU"]//font/text()').extract()).strip().encode('utf-8')
        text = text.replace(title, '').strip()
        date_added = response.meta.get('date_added', '')
        import pdb;pdb.set_trace()
        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text', xcode(text)
        print 'date', xcode(date_added)
