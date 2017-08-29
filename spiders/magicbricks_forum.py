from juicer.utils import *
from dateutil import parser
from scrapy.http import FormRequest
import urllib2

class MagicbricksForum(JuicerSpider):
    name = 'magicbricks_forum'
    start_urls = ['http://magicbricks.com/forum/city/Greater%20Noida','http://magicbricks.com/forum','http://www.magicbricks.com/forum/city/Gurgaon','http://www.magicbricks.com/forum/city/New%20Delhi','http://www.magicbricks.com/forum/city/Ghaziabad','http://www.magicbricks.com/forum/city/Faridabad','http://www.magicbricks.com/forum/city/Mumbai','http://www.magicbricks.com/forum/city/Pune','http://www.magicbricks.com/forum/city/Bangalore','http://www.magicbricks.com/forum/city/Chennai','http://www.magicbricks.com/forum/city/Agra','http://www.magicbricks.com/forum/city/Jamshedpur','http://www.magicbricks.com/forum/city/Surat','http://www.magicbricks.com/forum/city/Bhubaneswar','http://www.magicbricks.com/forum/city/Lucknow','http://www.magicbricks.com/forum/city/Vadodara','http://www.magicbricks.com/forum/city/Navi%20Mumbai','http://www.magicbricks.com/forum/city/Hyderabad','http://www.magicbricks.com/forum/city/Jaipur','http://www.magicbricks.com/forum/city/Raipur','http://magicbricks.com/forum/city/Bhopal','http://magicbricks.com/forum/city/Kochi','http://magicbricks.com/forum/city/Udaipur','http://magicbricks.com/forum/city/Coimbatore','http://magicbricks.com/forum/city/Thane','http://magicbricks.com/forum/city/Kolkata','http://magicbricks.com/forum/city/Ranchi','http://magicbricks.com/forum/city/Bhiwadi','http://magicbricks.com/forum/city/Kanpur','http://magicbricks.com/forum/city/Trichy','http://magicbricks.com/forum/city/Chandigarh','http://magicbricks.com/forum/city/Mangalore','http://magicbricks.com/forum/city/Ahmedabad','http://magicbricks.com/forum/city/Aurangabad','http://magicbricks.com/forum/city/Jodhpur','http://magicbricks.com/forum/city/Trivandrum','http://magicbricks.com/forum/city/Bokaro%20Steel%20City','http://magicbricks.com/forum/city/Madurai','http://magicbricks.com/forum/city/Vapi','http://magicbricks.com/forum/city/Home%20Insurance','http://magicbricks.com/forum/city/Legal%20and%20Taxation','http://magicbricks.com/forum/city/Investment%20tips','http://magicbricks.com/forum/city/Commercial','http://magicbricks.com/forum/city/Home%20Loan']

    handle_httpstatus_list = [404,302,403]

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False

    def parse(self,response):
        hdoc = HTML(response)
        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=7)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        res = urllib2.urlopen(response.url)
        links = hdoc.select('//div[@id="_recentanswerDiv"]//div[@class="topicComments"]/a/@href').extract() or hdoc.select('//div[@class="topicComments"]/a/@href').extract()
        for link in links[:2]:
            if 'http' not in link : link = 'http://magicbricks.com' + link
            yield Request(link,self.parse_next,response)

        next_page = hdoc.select('//div[@class="viewAllTopicBtn"]/@id').extract()
        url = 'http://magicbricks.com/forum/hottestTopics/list.page'
        if next_page != '':
            try:
                initTrendinglimit = response.meta['initTrendinglimit']
                endTrendingLimit = response.meta['endTrendingLimit']
            except:
                initTrendinglimit = '10'
                endTrendingLimit = '20'
            data = {'viewMoreType':'trending',
                'initTrendinglimit': initTrendinglimit,
                'endTrendingLimit': endTrendingLimit }
            endTrendingLimit = str(int(endTrendingLimit) + 10)
            initTrendinglimit = str(int(initTrendinglimit) + 10)
            yield FormRequest(url,self.parse,formdata=data,meta={'initTrendinglimit':initTrendinglimit,'endTrendingLimit':endTrendingLimit})

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="topicQuestionText"]//text()'))
        _id = textify(hdoc.select('//div[contains(@class,"detailsMainTopicRow")]/@id'))
        author = textify(hdoc.select('//div[contains(@class,"detailsMainTopicRow")]//div[@itemprop="author"]/a//text()'))
        author_url = textify(hdoc.select('//div[contains(@class,"detailsMainTopicRow")]//div[@itemprop="author"]/a/@href'))
        if 'http' not in author_url: author_url = 'http://magicbricks.com' + author_url
        date = textify(hdoc.select('//div[contains(@class,"detailsMainTopicRow")]//span[@itemprop="dateCreated"]/@datetime'))
        date1 = parse_date(xcode(date))
        dt_added = get_timestamp(parse_date(xcode(date),dayfirst=True) - datetime.timedelta(hours=5,minutes=30))
        print 'date',xcode(date)

        if date1 >= self.cutoff_dt:
            print '\n'
            print response.url + '#' + _id
            print 'title',xcode(title)
            print 'author',{'name':xcode(author),'url':xcode(author_url)}
            print 'date',dt_added
            print 'text',xcode(title)

        nodes = hdoc.select('//div[@itemprop="suggestedAnswer"]')

        for node in nodes:
            answer_id = textify(node.select('./parent::div/@id'))
            answerd_author = textify(node.select('.//div[@itemprop="author"]/a//text()'))
            answered_authorurl = textify(node.select('.//div[@itemprop="author"]/a/@href'))
            if 'http' not in answered_authorurl: answered_authorurl = 'http://magicbricks.com' + answered_authorurl
            answered_date = textify(node.select('.//span[@itemprop="dateCreated"]/@datetime'))
            answered_date1 = parse_date(xcode(answered_date))
            dt_added1 = get_timestamp(parse_date(xcode(answered_date),dayfirst=True) - datetime.timedelta(hours=5,minutes=30))
            text = textify(node.select('.//span[@itemprop="text"]//text()'))

            if answered_date1 >= self.cutoff_dt:
                print '\n'
                print response.url + '#' + answer_id
                print 'title',xcode(title)
                print 'date',dt_added1
                print 'author',{'name':answerd_author,'url':answered_authorurl}
                print 'text',xcode(text)

        threads = hdoc.select('//div[@class="pCommentsRow"]')

        for thread in threads:
            comment_id = textify(thread.select('./@id'))
            comment_author = textify(thread.select('.//div[@class="topicDisPersonName"]/a/text()'))
            comment_authorurl = textify(thread.select('.//div[@class="topicDisPersonName"]/a/@href'))
            if 'http' not in comment_authorurl: comment_authorurl = 'http://magicbricks.com' + comment_authorurl
            comment_date = textify(thread.select('.//div[@class="topicDisPersonName"]/span/text()')).strip('Commented on')
            comment_date1 = parse_date(xcode(comment_date))
            dt_added2 = get_timestamp(parse_date(xcode(comment_date),dayfirst=True) - datetime.timedelta(hours=5,minutes=30))
            comment_text = textify(thread.select('.//p[@itemprop="comment"]//text()'))

            if comment_date1 >= self.cutoff_dt:
                print '\n'
                print response.url + '#' + comment_id
                print 'title',xcode(title)
                print 'date',dt_added2
                print 'author',{'name':comment_author,'url':comment_authorurl}
                print 'text',xcode(comment_text)

