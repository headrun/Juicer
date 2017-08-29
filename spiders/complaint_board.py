from juicer.utils import *
from dateutil import parser

class  ComplaintBoard(JuicerSpider):
    name = "complaint_board"
    start_urls = ['http://www.complaintboard.com/']

    def parse(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//td[@class="wmm"]/div[@id]')
        for node in nodes[:2]:
            date = textify(node.select('.//td[@class="small"]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=-5))
            url = textify(node.select('.//td[@class="complaint"]/h4/a/@href'))
            if 'http:' not in url:
                url = 'http://www.complaintboard.com'+str(url)
            if dt_added < get_current_timestamp()-86400*7:
                is_next = False
                continue
            yield Request(url,self.parse_details,response)


        next_page = textify(hdoc.select('//div[@class="pagelinks"]/a[contains(text(),"Next")]/@href'))
        if next_page and is_next:
            url = 'http://www.complaintboard.com'+str(next_page)
            yield Request(url,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        is_next = True
        country = textify(hdoc.select('//form[@method="post"]//table/tr[2]//h1/text()'))
        brand = textify(hdoc.select('//form[@method="post"]//table/tr[1]//h1/text()'))
        title = textify(hdoc.select('//form[@method="post"]//h2//text()'))
        nodes = hdoc.select('//form[@method="post"]//div[@id]')
        for node in nodes:
            sub_title = textify(node.select('.//h4//text()'))
            _id = textify(node.select('./@id'))
            text = textify(node.select('.//h4/following-sibling::div//text()'))
            text = sub_title+' '+text
            date = textify(node.select('.//table/tr[1]/td[2]/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=-5))
            if dt_added < get_current_timestamp()-86400*7:
                is_next = False
                continue
            author = textify(node.select('.//table/tr[1]/td/a[not(@rel)]//text()'))
            author_url = textify(node.select('.//table/tr[1]/td/a[not(@rel)]/@href'))
            if author_url:
                author_url = 'http://www.complaintboard.com'+str(author_url)
            if not author:
                author = textify(node.select('.//table/tr[1]/td[1]/text()'))
                author_url = ''
            author = {'name':author,'url':author_url}
            url = response.url+'#'+str(_id)

            country = country.split(',')[0]
            if country.lower() == 'united states':
                country_tag = 'usa_country_manaual'
            else:
                country_tag = country.lower().replace(' ','_')+'_country_manaual'


            '''item = Item(response)
            item.set('title', xcode(title))
            item.set('text', xcode(text))
            item.set('dt_added', dt_added)
            item.set('author',author)
            item.set('url', url)
            item.set('xtags', [country_tag,'forums_sourcetype_manual'])'''
            #yield item.process()


        next_page = textify(hdoc.select('//div[@class="pagelinks"]/a[contains(text(),"Next")]/@href'))
        if next_page and is_next:
            url = 'http://www.complaintboard.com'+str(next_page)
            yield Request(url,self.parse_details,response)
