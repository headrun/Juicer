from juicer.utils import*
from dateutil import parser
import csv
import xlwt


class DigitalmonsterInfo(JuicerSpider):
    name = 'digitalmonster_info'
    start_urls = ['http://digitalmonster.org/top-digital-marketing-companies-in-india#sthash.hZJPlxnD.2RqW5kh3.dpbs']
    row_num = 0
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
 

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="entry themeform"]/ol')
        for node in nodes:
            agency_name = textify(node.select('./li/h4/a/text()'))
            agency_link = textify(node.select('./li/h4/a/@href'))

            agency_clientlist = textify(node.select('./following-sibling::p[2]/strong/../text()')).replace(':','').strip()
            agency_loc = textify(node.select('./following-sibling::p[3]/strong/../text()')).replace(':','').strip() or textify(node.select('./following-sibling::p[4]/strong/../text()')).replace(':','').strip()
            agency_desc = textify(node.select('./following-sibling::p[1]/text()')).replace(':','').strip()
            agency_awards = textify(node.select('./following-sibling::p[3]/a[contains(text(),"Award")]/../text()')).replace(':','').strip()


            data_list = "#<>#".join([agency_name,agency_link,agency_desc,agency_loc,agency_clientlist,agency_awards])
            row_num = self.row_num
            self.sheet1.write(row_num, 0, data_list)
            self.row_num= self.row_num+1
            self.book.save("digitalmonster.xls")

            '''
            print 'agency_name',xcode(agency_name)
            print 'agency_desc',xcode(agency_desc)
            print 'agency_loc',xcode(agency_loc)
            print 'agency_clientlist',xcode(agency_clientlist)
            #print 'agency_awards',xcode(agency_awards)
            '''


