from juicer.utils import *
from dateutil import parser
from scrapy.http import FormRequest

class CommonFloorPost(JuicerSpider):
    name = 'commonfloor_post'
    start_urls = ['https://www.commonfloor.com/forum']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="topic-discussion blackBottomBorder"]')
        for node in nodes:
            forum_link = textify(node.select('./div[@class="topic-title"]/a/@href').extract())
            date = textify(node.select('./div[@class="topic-started-user-details"]/div/div[@class="topic-start-date floatLeft"]/text()').extract())
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue

            yield Request(forum_link,callback=self.parse_next)


        for i in range(0,100):
            form_data = {'show_more':'1','r':'a','p':str(i)}
            yield FormRequest(response.url,callback=self.parse,formdata=form_data)


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

        print '\n'
        print response.url
        print 'title',xcode(title) + xcode(question)
        print 'text',xcode(question)
        print 'author',{'name':xcode(ques_postedby),'url':ques_postedbyurl,'location':ques_author_location}
        print 'ques_dt_added',ques_dt_added
        print 'category',real_name

        nodes = hdoc.select('//div[contains(@class,"topic-reply-holder topic-reply-holder")]')

        for node in nodes:
            reply_text = textify(node.select('.//div[@class="topic-reply-content"]//text()'))
            author = textify(node.select('.//div[@class="topic-replied-user-name"]/span/a/text()')).strip(',')
            author_url = textify(node.select('.//div[@class="topic-replied-user-name"]/span/a/@href'))
            author_location = textify(node.select('.//div[@class="topic-replied-user-name"]/text()'))
            date = textify(node.select('.//div[@class="topic-replied-date floatLeft"]/text()'))
            date1 = parse_date(date)
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))

           #if date1 >= self.cutoff_dt:

            print '\n'
            print response.url
            print 'title',xcode(title + question)
            print 'text',xcode(reply_text)
            print 'dt_added',xcode(dt_added)
            print 'author',{'name':xcode(author),'url':author_url,'location':author_location}

        threads = hdoc.select('//div[@class="topic-reply-comment-details"]')

        for thread in threads:
            comment_text = textify(thread.select('.//div[@class="reply-comment-content"]//text()'))
            comment_author = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]//a/text()')).strip(',')
            comment_author_url = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]/span/a/@href'))
            comment_author_location = textify(thread.select('.//div[@class="reply-commented-user-name floatLeft"]/text()'))
            comment_date = textify(thread.select('.//div[@class="reply-commented-date floatRight"]/text()'))
            comment_date1 = parse_date(comment_date)
            comment_dt_added = get_timestamp(parse_date(xcode(comment_date)) - datetime.timedelta(hours=5,minutes=30))

            #if comment_date1 >= self.cutoff_dt:
            print '\n'
            print response.url
            print 'title',xcode(title + question)
            print 'comment_dt_added',comment_dt_added
            print 'author',{'name':xcode(comment_author),'url':comment_author_url,'location':comment_author_location}
            print 'text',xcode(comment_text)
