from juicer.utils import *
from dateutil import parser
import json

class Hellopeter(JuicerSpider):
    name = 'hellopeter'
    start_urls = ['http://hellopeter.com/worlds-most']

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="lead-bd rest-hght2"]//div/ol//li/a/@href').extract()

        for node in nodes[:2]:
            if 'http' not in node:
                node = 'http://hellopeter.com/' + node
            node = textify(node.strip("since=5")) + 'since=30'
            yield Request(node,self.complaints,response)

    def complaints(self,response):
        hdoc = HTML(response)
        complaint_links = hdoc.select('//td[@class="title"]/div/strong/a/@href').extract()

        for complaint_link in complaint_links[:2]:
            if 'http' not in complaint_link: complaint_link = 'http://hellopeter.com' + complaint_link
            yield Request(complaint_link,self.details,response)

        next_page = textify(hdoc.select('//strong/a[@title="Go to the Next Page"]/@href'))
        if 'http' not in next_page: next_page = 'http://hellopeter.com' + next_page
        yield Request(next_page,self.complaints,response)

    def details(self,response):
        hdoc = HTML(response)
        response.url = 'http://hellopeter.com/telkom/complaints/hosted-pabx-solution-1853469'
        title = textify(hdoc.select('//div[@class="intro spages"]/h1/text()'))
        supplier = textify(hdoc.select('//td[contains(text(),"SUPPLIER")]/following-sibling::td/h2/a/text()'))
        supplier_link = textify(hdoc.select('//td[contains(text(),"SUPPLIER")]/following-sibling::td/h2/a/@href'))
        industry = textify(hdoc.select('//td[contains(text(),"INDUSTRY")]/following-sibling::td//a/text()'))
        industry_link = textify(hdoc.select('//td[contains(text(),"INDUSTRY")]/following-sibling::td//a/@href'))
        branch = textify(hdoc.select('//td[contains(text(),"BRANCH / AREA")]/following-sibling::td/text()')[0])
        country = textify(hdoc.select('//td[contains(text(),"COUNTRY")]/following-sibling::td/text()'))
        date = textify(hdoc.select('//td[contains(text(),"TIME / DATE")]/following-sibling::td/text()')[0])
        person = textify(hdoc.select('//td[contains(text(),"PERSON RESPONSIBLE")]/following-sibling::td/text()'))
        customer = textify(hdoc.select('//td[contains(text(),"CUSTOMER")]/following-sibling::td/text()')[0])
        nature = textify(hdoc.select('//h3[@class="tbl-txt-hd-nb"]/text()'))
        incident = textify(hdoc.select('//td[contains(text(),"INCIDENT")]/following-sibling::td/text()'))
        headline = textify(hdoc.select('//h2[@class="tbl-txt-hd-nb"]/text()'))
        text = textify(hdoc.select('//td[@class="yellow-shade border justify"]/text()'))
        suppliers_responded = textify(hdoc.select('//td[contains(text()," RESPONSE")]/following-sibling::td/strong/a/text()'))
        suppliers_respondedlink = textify(hdoc.select('//td[contains(text()," RESPONSE")]/following-sibling::td/strong/a/@href'))
        responded_date = textify(hdoc.select('//td[contains(text(),"Time and Date")]/following-sibling::td/text()'))
        supplier_response = textify(hdoc.select('//td[@class="supp-resp border"]//text()'))

        comment_link = 'https://www.facebook.com/plugins/comments.php?api_key=&channel_url=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter%2FTlA_zCeMkxl.js%3Fversion%3D41%23cb%3Df365261448%26domain%3Dhellopeter.com%26origin%3Dhttp%253A%252F%252Fhellopeter.com%252Fff765b38%26relation%3Dparent.parent&href=' + response.url + '&locale=en_US&numposts=10&sdk=joey&width=590'
        '''
        print '\n'
        print response.url
        print 'title',xcode(title)
        print 'supplier',{'name':supplier,'link':supplier_link}
        print 'industry',{'name':industry,'link':industry_link}
        print 'location',{'country':country,'branch':branch}
        print 'dt_added',date
        print 'person',person
        print 'customer',customer
        print 'nature',nature
        print 'incident',incident
        print 'headline',headline
        print 'responded_date',responded_date
        print 'text',text
        print 'supplier_responded_details',{'name':suppliers_responded, 'link':suppliers_respondedlink, 'date':responded_date, 'text':supplier_response}
        '''
        if comment_link:
            yield Request(comment_link,self.comments,response)

    def comments(self,response):
        hdoc =HTML(response)
        import pdb;pdb.set_trace()


