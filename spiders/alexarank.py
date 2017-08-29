from juicer.utils import *

class AlexaRank(JuicerSpider):
    name = 'alexarank'
    start_urls = ['http://www.alexa.com/']

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        f = open('my_forums_filter','r')
        lines = f.readlines()
        for row in lines:
            row = 'http://www.alexa.com/siteinfo/http://' + row
            yield Request(row,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        global_rank = textify(hdoc.select('//span[@data-cat="globalRank"]//strong[@class="metrics-data align-vmiddle"]/text()'))
        rank = textify(hdoc.select('//span[@class="countryRank"]//strong[@class="metrics-data align-vmiddle"]/text()'))
        output_file = 'my_forum_final_alexarank'
        out_file = file(output_file,'ab+')
        out_file.write('%s\t%s\t%s\n'%(response.url,global_rank,rank))
        out_file.close()
