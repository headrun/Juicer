from juicer.utils import*
from dateutil import parser

class CnnPhilippines(JuicerSpider):
    name = 'cnnphilippines'
    start_urls = ['http://cnnphilippines.com' , 'http://cnnphilippines.com/life/']


    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class=" nav navbar-nav custom-navbar"]//li/a/@href').extract()
        for category in categories:
            yield Request(category,self.parse_details,response)


    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        links = hdoc.select('//div[contains(@class, "widget")]//a/@href').extract()
        for link in links:
            if 'videos' in link:
                continue
            yield Request(link,self.parse_finaldata,response)

    def parse_finaldata(self,response):
        hdoc = HTML(response)
#        if response.url == 'http://cnnphilippines.com/news/2016/05/12/leni-robredo-bongbong-marcos-cheating-allegations-election-results-rigging.html':
#        if response.url == 'http://cnnphilippines.com/news/2016/09/14/House-committee-approves-OP-OVP-budget-in-minutes.html':
 #           import pdb;pdb.set_trace()
        title = textify(hdoc.select('//h2[@class="title"]/text()')) or textify(hdoc.select('//div[@class="content-main-title"]/h2/text()'))
        text1 = textify(hdoc.select('//div[contains(@id, "content-body-")]//text()')) or textify(hdoc.select('//div[contains(@id, "content-body-")]/p[not(contains(@href, "http"))]//text()'))
        text2 = hdoc.select('//div[contains(@id, "content-body-")]/p[not(contains(@href, "http"))]//a/text()').extract()
        for text_extra in text2:
            text1 = text1.replace(text_extra,'')
        text = text1
        text = text.replace(u'\u2014\xa0',' ')
        date = textify(hdoc.select('//p[@class="dateString"]/text()').extract()).split('updated')[0]
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author_full = textify(hdoc.select('//div[@class="author-byline"]//text()')) or textify(hdoc.select('//div[@class="cnn-life story-byline"]/p/text()'))
        author = textify(re.findall('\D+,',author_full)) or textify(re.findall('\D+',author_full))
        author = textify(re.split(',',author)).replace('By','').strip()

        date = ','.join((re.split(',',author_full)[2:])) or  textify(hdoc.select('//p[@class="dateString"]/text()')).replace('Updated','').strip()
        author_url = textify(hdoc.select('//div[@class="author-byline"]//a/@href'))
        if not response.meta.get('check', ''):
            yield Request(author_url,self.parse_extraurls,response)
    def parse_extraurls(self,response):
        hdoc = HTML(response)
        is_next = True
        extra_urls = hdoc.select('//div[@class="media-body "]//h4/a/@href')
        for url in extra_urls:
            yield Request(url,self.parse_finaldata,response, meta={'check' : 'check'})

        next_pg = hdoc.select('//ul[@class="pagination"]/li/a/@href').extract()[-1] 
        if 'http' not in next_pg: next_pg = 'http://cnnphilippines.com/tags/author' + next_pg
        no_link = hdoc.select('//ul[@class="pagination"]/li/span[@class="noLink"]/text()').extract()
        if 'http' not in no_link: no_link = 'http://cnnphilippines.com/tags/author' + next_pg
        import pdb;pdb.set_trace()

        if next_pg and is_next:
            if not no_link:
                yield Request(next_pg,self.parse_extraurls,response)



        '''
        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'text', xcode(text)
        print 'dt_added',xcode(dt_added)
        print 'author', xcode(author)
        print 'author_url', xcode(author_url)

'''
