import xlwt, xlrd, csv
import codecs
from juicer.utils import*
from dateutil import parser

output_file = codecs.open("influencer_sheet","ab+","utf-8") 

class InfluencerIN(JuicerSpider):
    name = 'influencer'
    start_urls = ['http://www.influencer.in/users/list/']


    def parse(self,response):
        hdoc = HTML(response)
        categories = hdoc.select('//ul[@class="nav nav-tabs text-center"]/li/a/@href').extract()
        for category in categories:
            yield Request(category,self.parse_links,response)


    def parse_links(self,response):
        hdoc= HTML(response)
        links = hdoc.select('//div[@class="text-center"]/a[@target="_blank"]/@href').extract()
        for link in links:
            yield Request(link,self.parse_data,response)


    def parse_data(self,response):
        hdoc = HTML(response)
        name = textify(hdoc.select('//h1[@class="font-raleway-semibold "]/text()'))
        industry = textify(hdoc.select('//h1[@class="font-raleway-semibold "]/span/text()').extract())
        blog =textify(hdoc.select('//div[@class="col-md-8 col-sm-8 col-xs-9 nopadding"]/span[@class="f12"]/a/@href'))
        instagram = textify(hdoc.select('//div[@class="col-md-8 col-sm-8 col-xs-7 nopadding"]/span[@class="f12"]/a/@href'))
        twitter = textify(hdoc.select('//div[@class="col-md-8 col-sm-8 col-xs-8 nopadding"]/span[@class="f12"]/a/@href')) 
        writing_to_outputfile = "#<>#".join([name,industry,blog,instagram,twitter])
        output_file.write('%s\n'%writing_to_outputfile)

        '''
        row_count =1
        values = [name,industry,blog,instagram,twitter]
        excel_file_name = 'influencer.xls'
        excel_file = xlwt.Workbook(encoding="utf-8")
        excel_sheet1 = excel_file.add_sheet("sheet1")

        import pdb;pdb.set_trace()
        for col_count,value in enumerate(values):
            excel_sheet1.write(row_count,col_count,value)
            row_count = row_count+1

        #excel_sheet1.write("%s  %s  %s  %s  %s\n")%(name,industry,blog,instagram,twitter)
        excel_file.save(excel_file_name)
        '''
