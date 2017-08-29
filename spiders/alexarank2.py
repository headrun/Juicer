from juicer.utils import *

class AlexaRank(JuicerSpider):
    name = 'alexarank2'
    start_urls = ['http://www.alexa.com/']

    def parse(self,response):
        hdoc = HTML(response)
        f = open('th_alexalinks1','r')
        lines = f.readlines()
        for row in lines:
           yield Request(row,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        global_rank = textify(hdoc.select('//span[@data-cat="globalRank"]//strong[@class="metrics-data align-vmiddle"]/text()'))
        rank = textify(hdoc.select('//span[@class="countryRank"]//strong[@class="metrics-data align-vmiddle"]/text()'))
        output_file = 'th_final_alexarank1'
        out_file = file(output_file,'ab+')
        out_file.write('%s\t%s\t%s\n'%(response.url,global_rank,rank))
        out_file.close()
