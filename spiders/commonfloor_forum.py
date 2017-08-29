from juicer.utils import *
from dateutil import parser

class CommonFloorForum(JuicerSpider):
    name = 'commonfloor_forum'
    start_urls = ['https://www.commonfloor.com/forum?p=9']

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
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=10)
            self.cutoff_dt = check_date - oneweek_diff
        links = hdoc.select('//div[@id="posts_container"]//div[@class="topic-title"]/a/@href').extract()

        for link in links:
            yield Request(link,self.parse_next,response)
        next_page = hdoc.select('//div[@class="show-more-topic-discussions"]/text()').extract()
        if next_page:
            if '/forum?p=' in response.url:
                page_number = int(response.url.split('/forum?p=')[-1]) + 1
                next_page = 'https://www.commonfloor.com/forum?p=' + str(page_number)
            else: next_page = 'https://www.commonfloor.com/forum?p=2'
            yield Request(next_page,self.parse,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="topic"]/h1/text()'))
        question = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]/div[@class="topic-title"]/text()'))
        ques_postedby = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]//div[@class="topic-started-user-name"]/span/a/text()')).strip(',')
        ques_postedbyurl = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]//div[@class="topic-started-user-name"]//a/@href'))
        ques_author_location = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]//div[@class="topic-started-user-name"]/text()'))
        ques_date = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]//div[@class="topic-start-date floatLeft"]/text()'))
        ques_date1 = parse_date(ques_date)
        ques_dt_added = get_timestamp(parse_date(xcode(ques_date)) - datetime.timedelta(hours=5,minutes=30))
        real_name = textify(hdoc.select('//div[@class="topic-question-wrapper blackBottomBorder"]//div[@class="topic-name floatLeft"]/a/text()'))

        if ques_date1 >= self.cutoff_dt:
            print '\n'
            print response.url
            print 'title',xcode(title) + xcode(question)
            print 'text',xcode(question)
            print 'author',{'name':xcode(ques_postedby),'url':ques_postedbyurl,'location':ques_author_location}
            print 'date',ques_date
            print 'category',real_name
        
        nodes = hdoc.select('//div[contains(@class,"topic-reply-holder topic-reply-holder")]')

        for node in nodes:
            reply_text = textify(node.select('.//div[@class="topic-reply-content"]//text()'))
            author = textify(node.select('.//div[@class="topic-replied-user-name"]/span/a/text()')).strip(',')
            author_url = textify(node.select('.//div[@class="topic-replied-user-name"]/span/a/@href'))
            author_location = textify(node.select('.//div[@class="topic-replied-user-name"]/text()'))
            date = textify(node.select('.//div[@class="topic-replied-date floatLeft"]/text()'))
            date1 = parse_date(date)
        #   dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

            if date1 >= self.cutoff_dt:

                print '\n'
                print response.url
                print 'title',xcode(title + question)
                print 'text',xcode(reply_text)
                print 'date',date
                print 'author',{'name':xcode(author),'url':author_url,'location':author_location}
        import pdb;pdb.set_trace()
        threads = hdoc.select('//div[@class="topic-reply-comment-details"]')

        for thread in threads:
            comment_text = textify(thread.select('.//div[@class="reply-comment-content"]//text()'))
            comment_author = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]//a/text()')).strip(',')
            comment_author_url = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]/span/a/@href'))
            comment_author_location = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]/text()'))
            comment_date = textify(thread.select('.//div[@class="reply-commented-date floatRight"]/text()'))
            comment_date1 = parse_date(comment_date)
       #    comment_dt_added = get_timestamp(parse_date(xcode(comment_date)) - datetime.timedelta(hours=5,minutes=30))

            if comment_date1 >= self.cutoff_dt:
                print '\n'
                print response.url
                print 'title',xcode(title + question)
                print 'date',comment_date
                print 'author',{'name':xcode(comment_author),'url':comment_author_url,'location':comment_author_location}
                print 'text',xcode(comment_text)

