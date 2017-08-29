from juicer.utils import *
from dateutil import parser

class LoveLimes(JuicerSpider):
    name = "love_limes"
    start_urls = ['']

    def parse(self, response):
        hdoc = HTML(response)
        urls = hdoc.select('')
        for url in urls:
            yield Request(url, self.parse_details, response)

    def parse_details(self, response):
        hdoc = HTML(response)

        title = textify(hdoc.select(''))
        text = textify(hdoc.select(''))
        dt_added = textify(hdoc.select(''))
        author = textify(hdoc.select(''))

        #if date format is "05-05-2014" and day is the first then we have to
        #pass dayfirst=True to parse_date function
        # parse_date('05-07-2014') - Wrong
        #datetime.datetime(2014, 5, 7, 0, 0)
        #parse_date('05-07-2014', dayfirst=True) - Correct
        #datetime.datetime(2014, 7, 5, 0, 0)

        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=8))
        print "Title:::::::::::::",title
        print "Text::::::::::::::",text
        print "date::::::::::;;",dt_added
        print "url::::::",resposne.url
        '''
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        item.set('xtags', ['china_country_manual', 'wechat_sourcetype_manual'])

        yield item.process()
        '''
