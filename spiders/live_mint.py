from juicer.utils import *
from dateutil import parser

class LiveMint(JuicerSpider):
    name = "livemint"
    start_urls = ['http://www.livemint.com/Query/lZy3FU0kP9Cso5deYypuDI/people.html?facet=subSection','http://www.livemint.com/Query/ZtZgviOVr74zwZ37eD9uDI/results.html?facet=subSection','http://www.livemint.com/Query/V1eAlpSAzt0kHm6oBnOvDI/management.html?facet=subSection','http://www.livemint.com/Query/lpAyR4Wo8C3SXmJBj8tuyK/views.html?facet=subSection','http://www.livemint.com/Query/PQJwsqCd52iWfHoxGnNtyK/online-views.html?facet=subSection','http://www.livemint.com/Query/JFxEXcnZWEkzPkSUuUFvyK/columns.html?facet=subSection','http://www.livemint.com/Query/X6WVejFv2XR0EuY0gumvyK/quick-edit.html?facet=subSection','http://www.livemint.com/Query/hbgVnrGsAo71tYr1VPHmkJ/retail.html?facet=subSection','http://www.livemint.com/Query/5jCbPmmTjmX6bvfyV5XlkJ/financial-services.html?facet=subSection','http://www.livemint.com/Query/pDgg1HH1sAxJUpRxH65lkJ/manufacturing.html?facet=subSection','http://www.livemint.com/Query/FFQNajxXoQX6ueRs5ySmkJ/telecom.html?facet=subSection','http://www.livemint.com/Query/hHUQJ3ncBXZBGH3eVyKlkJ/energy.html?facet=subSection','http://www.livemint.com/Query/zuBXLOuue12DFytBwNjlkJ/hr.html?facet=subSection','http://www.livemint.com/Query/P8RBwcvO9gvJl6xh6wTNzO/infotech.html?facet=subSection','http://www.livemint.com/Query/59D3aruALU0IX1GgHP8SDL/policy.html?facet=subSection','http://www.livemint.com/Query/vqugGXasOPir7LpvkzGSDL/infrastructure.html?facet=subSection','http://www.livemint.com/Query/Rvw6vyqrwUdCxnxjvPZSDL/education.html?facet=subSection','http://www.livemint.com/Query/N16rSOPRyTXflQSevctRDL/international.html?facet=subSection','http://www.livemint.com/Query/F9iGNRnBLqZVFcxbO5mTDL/reports.html?facet=subSection','http://www.livemint.com/Query/dpEDNI92z2l8tlro1IdRDL/agriculture.html?facet=subSection','http://www.livemint.com/Query/pvQ1Hmhug42t8emPkTpSDL/human-development.html?facet=subSection','http://www.livemint.com/Query/Hi6HaGXvVLB9W4e31GU5eI/marketing.html?facet=subSection','http://www.livemint.com/Query/pfUlkE2sRxFtnTXRpGk5eI/research.html?facet=subSection','http://www.livemint.com/Query/RFNFcuH8h1B84rXLxtB6eI/personal-tech.html?facet=subSection','http://www.livemint.com/Query/VBSz5w6iZO0oHUqPJsy5eI/media.html?facet=subSection','http://www.livemint.com/Query/b2RMQGpR06nCqpbb2D74eI/advertising.html?facet=subSection','http://www.livemint.com/Query/nMTfX0vuAr8nM1VJaPdp3J/lounge.html?facet=subSection','http://www.livemint.com/Query/ZlVE3pSeycLiyquAxEzn3J/business-of-life.html?facet=subSection','http://www.livemint.com/Query/jIarviPpOzeWkT7rrPMp3J/indulge.html?facet=subSection','http://www.livemint.com/Query/pd7xASzoRgQFLZgfCqhPMN/personal-finance.html?facet=subSection','http://www.livemint.com/Query/lLpizY6ixkyoJtHyUHYYbN/markets.html?facet=subSection','http://www.livemint.com/Query/rq3Q26fPwndf5Wqv8TRNtN/did-you-know.html?facet=subSection','http://www.livemint.com/Query/B5rH9IkIyAjA13Jf0DVWTO/mint-50.html?facet=subSection','http://www.livemint.com/Query/ZbYasTkXO3oQ3J1dHVA26H/mint-money-columns.html?facet=subSection']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="text-box"]')
        for node in nodes[:1]:
            date = textify(node.select('./p[@class="date-box"]/text()'))
            date = date.split(',')[-1].split('.')[0].strip()
            date_added = get_timestamp(parse_date(date) -datetime.timedelta(hours=5,minutes=30))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            link = textify(node.select('.//h2/a/@href'))
            if 'http' not in link: link = 'http://www.livemint.com' + link
        #urls = hdoc.select('//div[@class="col_12"]//div[@class="ins_sub_sty"]//h2//a//@href')
            yield Request(link,self.parse_details, response)

        next_pg = textify(hdoc.select('//div[@class="text-right pagination"]/a[@id="nextBelow"]/@href'))   
        if 'http' not in next_pg:next_pg = 'http://www.livemint.com' + next_pg
        yield Request(next_pg,self.parse,response)

    def parse_details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1/text()'))
        sub_title = textify(hdoc.select('//p[@class="intro-box"]/text()'))
        text = textify(hdoc.select('//div[@class="story-content"]/p//text()'))
        text = sub_title + ' ' + text
        #dt_added = textify(hdoc.select('//div[@class="story-meta"]/text()'))
        #dt_added = textify(hdoc.select('//div[@class="sty_posted_txt"]//text()'))
        #date = datetime.datetime.strftime(dt_added,"%b %d %Y %I:%M %p")
        date = textify(hdoc.select('//div[@class="story-meta"]/span[contains(text(), "First")]/../text()'))
        b=''.join(re.findall('.*\,\s.*\s\d+\d\d+\.\s(\d+\s\d+)\s.*\s.*',date))
        c=b.replace(' ', ':')
        date=date.replace(b,c)
        dt_added = get_timestamp(parse_date(date) - datetime.timedelta(hours=5, minutes=30))
        author = hdoc.select('//div[@class="author-box"]//strong/a//text()').extract()[1]
        import pdb;pdb.set_trace()
        '''
        if dt_added:
            (extra_data,dt_added) = dt_added.split('First Published:')
            _dt_added = dt_added.split('.')
            s = _dt_added[-1].strip().split(' ')
            dt_added = '%s %s:%s %s %s' %(_dt_added[0], s[0], s[1], s[2], s[3])
            dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))
        else:
            dt_added = ""

        item = Item(response)
        item.set('title', xcode(title))
        item.set('text', xcode(text))
        item.set('dt_added', dt_added)
        item.set('author.name', xcode(author))
        item.set('url', response.url)
        yield item.process()'''
