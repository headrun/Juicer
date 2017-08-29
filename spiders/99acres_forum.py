from juicer.utils import *
from dateutil import parser
from scrapy.http import FormRequest

class Acres99Forum(JuicerSpider):
    name = '99acres_forum'
    start_urls = ['http://www.99acres.com/ask']

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

        try:idlist = textify(hdoc.select('//div[contains(@id,"olderPostLink")]/a/@onclick')).split('(')[1].split(',')
        except:import pdb;pdb.set_trace()
        _id = idlist[5:-3]
        _id = ','.join(str(i) for i in _id).strip("'")
        lasttimestamp = idlist[-3].strip("'")
        links = hdoc.select('//div/a[contains(@href,"html")]/@href').extract()

        for link in links:
            yield Request(link,self.parse_next,response)

        headers = {
            'userid':'0',
            'categoryId':'-1',
            'locationId':'-1',
            'locationtype':'city',
            'start':'10',
            'threadIdCsv':_id,
            'lastTimeStamp':lasttimestamp,
            'faq_id_filter':'',
            'pageUrl':'http://www.99acres.com/ask',
            'is_ajax':'1'
            }

        url = 'http://www.99acres.com/ask/getOlderWallData'
        yield FormRequest(url,self.parse,formdata=headers)

    def parse_next(self,response):
        hdoc = HTML(response)
        discussion_title = textify(hdoc.select('//div[@class=" Fnt16 bld float_L"]/text()'))
        discussion_question = textify(hdoc.select('//div[@class="lineSpace_20 ana_blog_detail"]/text()'))
        discussion_quesauthor = textify(hdoc.select('//div[@class="lineSpace_20 ana_blog_detail"]//a/text()'))
        discussion_quesauthor_url = textify(hdoc.select('//div[@class="lineSpace_20 ana_blog_detail"]//a/@href'))
        if 'http' not in discussion_quesauthor_url: discussion_quesauthor_url = 'http://www.99acres.com' + discussion_quesauthor_url
        discussion_quesdate = textify(hdoc.select('//div[@id="questionMainDiv"]//div[contains(text(),"Posted")]/text()')).replace('Posted:','')
        ask_questiontitle = textify(hdoc.select('//div[@id="questionId"]//text()'))
        ask_question = textify(hdoc.select('//div[@id="questionMainDiv"]//div[contains(@class,"fcblk Fnt14")]//text()'))
        ask_quesauthor = textify(hdoc.select('//div[@class="fcdGya mt6"]//a/text()'))
        ask_quesauthorurl = textify(hdoc.select('//div[@class="fcdGya mt6"]/span[@onmouseover]/a/@href'))
        if 'http' not in ask_quesauthorurl: ask_quesauthorurl = 'http://www.99acres.com' + ask_quesauthorurl
        if ask_questiontitle or ask_question:ask_quesdate = textify(hdoc.select('//div[@class="fcdGya mt6"]/text()').extract()[2])
        else: ask_quesdate=''
        date_dict = {'a year ago':'1 years ago','a month ago':'1 months ago','a week ago':'1 week ago','an hour ago':'1 hour ago','Few mins ago':'1 mins ago'}
        for key,value in date_dict.iteritems():
            if key == discussion_quesdate: discussion_quesdate = value
            elif key == ask_quesdate: ask_quesdate = value
        if ask_quesdate != '':
            if 'min' in ask_quesdate: ask_quesdate = ask_quesdate.replace('mins','minutes')
            date_added = parse_date(xcode(ask_quesdate))
            dt_added = get_timestamp(parse_date(xcode(ask_quesdate)) - datetime.timedelta(hours=5,minutes=30))
        elif discussion_quesdate != '':
            if 'min' in discussion_quesdate: discussion_quesdate = discussion_quesdate.replace('mins','minutes')
            date_added = parse_date(xcode(discussion_quesdate))
            dt_added = get_timestamp(parse_date(xcode(discussion_quesdate)) - datetime.timedelta(hours=5,minutes=30))

        if date_added >= self.cutoff_dt:
            if discussion_title or discussion_question:
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(discussion_title + discussion_question))
                item.set('text', xcode(discussion_title + discussion_question))
                item.set('author',{'name':discussion_quesauthor,'url':discussion_quesauthor_url})
                item.set('dt_added',dt_added)
                yield item.process()

            else :
                item = Item(response)
                item.set('url',response.url)
                item.set('title',xcode(ask_questiontitle + ask_question))
                item.set('text', xcode(ask_questiontitle + ask_question))
                item.set('dt_added',dt_added)
                item.set('author',{'name':xcode(ask_quesauthor),'url':ask_quesauthorurl})
                yield item.process()

        nodes = hdoc.select('//div[contains(@id,"MsgContent")]')

        for node in nodes:
            text = textify(node.select('.//span[contains(@id,"msgTxtContent")]//text()')) or textify(node.select('.//div[contains(@id,"msgTxtContent")]//text()'))
            text_id = textify(node.select('.//span[contains(@id,"msgTxtContent")]/@id')) or textify(node.select('.//div[contains(@id,"msgTxtContent")]/@id'))
            date = textify(node.select('.//div[contains(text(),"Posted")]/text()')) or textify(node.select('.//span[@class="fcGya"]/text()')).replace('Posted:','') or textify(node.select('.//div[@class="float_L fcdGya Fnt11"]/text()'))
            author_name = textify(node.select('.//span[@onmouseover]/a/text()'))
            author_url = textify(node.select('.//span[@onmouseover]/a/@href'))
            if 'http' not in author_url: author_url = 'http://www.99acres.com' + author_url
            for key,value in date_dict.iteritems():
                if key == date: date = value
            if 'min' in date: date = date.replace('mins','minutes')
            date_added1 = parse_date(xcode(date))
            dt_added1 = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            sk = response.url + '#' +text_id

            if date_added1 >= self.cutoff_dt and text != '':
                if discussion_title :print 'title',xcode(discussion_title + discussion_question)
                else:print 'title',xcode(ask_questiontitle + ask_question)
                item = Item(response)
                item.set('url',response.url + '#' +text_id)
                if discussion_title :item.set('title', xcode(discussion_title + discussion_question))
                else :item.set('title',xcode(ask_questiontitle + ask_question))
                item.set('text',xcode(text))
                item.set('dt_added1',dt_added1)
                item.set('author',{'name':xcode(author_name),'url':author_url})
                item.set('sk',md5(sk))
