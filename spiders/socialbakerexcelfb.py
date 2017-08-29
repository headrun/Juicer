from juicer.utils import *
from dateutil import parser
import csv
import xlwt

class SocialbakersFBNEW(JuicerSpider):
    name = 'socialbakers_newfb'
    start_urls = ['https://www.socialbakers.com/statistics/facebook/pages/total/brunei/']
    row_num = 0
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//td[@class="name"]//div[@class="item"]')
        for node in nodes:
            page_id = textify(node.select('./a/@href'))
            pg_id = textify(re.findall('\d+',page_id))
            fb_page = 'https://www.facebook.com/feeds/page.php?id=%s&format=rss20'%pg_id
            row_num = self.row_num
            data = '#<>#'.join([fb_page,pg_id])
            self.sheet1.write(row_num, 0, data)
            self.row_num= self.row_num+1
            self.book.save("fbstats.xls")

        try:
            pg_num = response.meta['pg_num']+1
        except:
            pg_num = 2
        next_page = textify(hdoc.select('//div[@class="more-center-link"]/a[@rel="next"]/@href'))
        if next_page:
            next_page = 'https://www.socialbakers.com/statistics/facebook/pages/total/brunei/page-' + str(pg_num)
            yield Request(next_page, self.parse, response, meta={'pg_num':pg_num})
