from juicer.utils import *

class Indi_Tags(JuicerSpider):
    name = 'indi_tags'
    start_urls = ['http://www.indiblogger.in/tagsearch.php?tag=cricket']


    def parse(self, response):
        hdoc = HTML(response)

        nextpage_url = ""
        tag = []
        rows = hdoc.select('//ul/li[@class="listing"]')
        for row in rows:
            tag = row.select('./div[@class="tags"]/a')
            tags = [xcode(textify(i).replace("&amp;","")) for i in tag]
            tags = [j.strip() for j in tags if j]
            for tg in tags:
                out_file = file('/home/headrun/venu/indi_tags_cricket','ab+')
                out_file.write('%s\n'%(tg))
                out_file.close()

        nextpage_url = hdoc.select('//div[@class="pagerbarT"]/a/@href')

        if nextpage_url:
            yield Request(nextpage_url, self.parse, response)

