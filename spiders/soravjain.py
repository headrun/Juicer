from juicer.tils import*
from dateutil import parser
import codecs
import csv
import xlwt

class SoravjainBlog(JuicerSpider):
    name = "soravjain_blog"
    start_urls = 'http://www.soravjain.com/indian-social-media-digital-marketing-agencies'
    row_num = 0
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        nodes = hdoc.select('//div[@class="entry-content"]/ol[@style="text-align: justify;"]')
        for node in nodes:
            agency_name = textify(node.select('./li/strong/a/text()')) or textify(node.select('./li/a/strong/text()'))
            agency_link = textify(node.select('./li/strong/a/@href')) or textify(node.select('./li/a/@href'))
            agency_desc = textify(node.select('./li/text()'))
            agency_services = textify(node.select('./following-sibling::p[contains(text(),"Services:")][1]/text()')).replace('Services:','').strip()
            agency_brands = textify(node.select('./following-sibling::p[contains(text(),"Brands:")][1]/text()')).replace('Brands:','').strip()
            agency_location = textify(node.select('./following-sibling::p[contains(text(),"Location:")][1]/text()')).replace('Location:','').strip()
            data_list = "#<>#".join([agency_name,agency_link,agency_desc,agency_loc,agency_clientlist,agency_awards])
            row_num = self.row_num
            self.sheet1.write(row_num, 0, data_list)
            self.row_num= self.row_num+1
            self.book.save("digitalmonster.xls")

'''
            print 'agency_name:',xcode(agency_name)
            print 'agency_link:',xcode(agency_link)
            print 'agency_desc:',xcode(agency_desc)
            print 'agency_services:',xcode(agency_services)
            print 'agency_brands:',xcode(agency_brands)
            print 'agency_location:',xcode(agency_location)'''
