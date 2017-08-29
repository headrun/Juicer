from juicer.utils import*
from dateutil import parser

class ComplaintsIndia(JuicerSpider):
    name = 'complaints_india'
    start_urls = ['http://www.consumercomplaints.in/']

    
    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//td[@class="complaint"]/h4/a/@href').extract()
        for url in urls:
            if 'http' not in url:
                url = 'http://www.consumercomplaints.in' + url
            yield Request(url,self.parse_details,response)

        next_page = textify(hdoc.select('//div[@class="pagelinks"]//a[contains(text(),"Next")]/@href'))
        if next_page:
            if 'http' not in next_page:
                next_page = 'http://www.consumercomplaints.in' + next_page
            yield Request(next_page,self.parse,response)
        

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td[@class="complaint"]/h1/text()'))
        text = textify(hdoc.select('//td[@class="compl-text"]/div/text()'))
        author = textify(hdoc.select('//table[@typeof="v:Review-aggregate"]//td[@class="small"]/a[contains(@href,"profile")]/text()'))
        author_url = textify(hdoc.select('//table[@typeof="v:Review-aggregate"]//td[@class="small"]/a[last()][contains(@href,"profile")]/@href'))
        if 'http' not in author_url:author_url = 'http://www.consumercomplaints.in' + author_url
        date = textify(hdoc.select('//table[@typeof="v:Review-aggregate"]//td[@class="small"]/text()')).split('on')[-1]

        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'author',xcode(author)
        print 'author_url',xcode(author_url)
        print 'date',xcode(date)
