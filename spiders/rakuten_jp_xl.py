from juicer.utils import *
from dateutil import parser
import xlwt

excel_file_name = 'rakuten_jp.xlsx'
header = ['Product Title', 'Review Title', 'Review Details', 'Review URL', 'Review DateTime', 'Reviewd By', 'Review Rating', 'Product URL']

todays_excel_file = xlwt.Workbook(encoding="utf-8")
todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")

for i, row in enumerate(header):
    todays_excel_sheet1.write(0, i, row)

class RakutenJapanReviews(JuicerSpider):
    name = 'rakuten_jp_xls'
    start_urls = ['http://review.rakuten.co.jp/item/1/193677_11346084/1.1/sort6/','http://review.rakuten.co.jp/item/1/193677_11346085/1.1/sort6/']


    def parse(self,response):
        hdoc = HTML(response)
        f = open('rakuten_pg1','r')
        lines = f.readlines()
        for row in lines:
            yield Request(row,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        links = textify(hdoc.select('//table[@class="page_item_reviews"]//td/a[contains(@href,"item")]/@href'))
        if links: links = links + 'sort6/'
        yield Request(links,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)

        try : row_count = response.meta['row_count']
        except: row_count = 1
        product_title = textify(hdoc.select('//h2[@class="revItemTtl fn"]//a/text()'))
        product_link = textify(hdoc.select('//h2[@class="revItemTtl fn"]//a/@href'))
        avg_rating = textify(hdoc.select('//span[@class="revEvaNumber average"]/text()'))
        nodes = hdoc.select('//div[@class="revRvwUserSec hreview"]')
        for node in nodes:
            date = textify(node.select('.//span[@class="revUserEntryDate dtreviewed"]/text()'))
            review_rating = textify(node.select('.//span[@class="revUserRvwerNum value"]/text()'))
            author_name = textify(node.select('.//dt[@class="revUserFaceName"]/span/text()'))or textify(node.select('.//dt[@class="revUserFaceName reviewer"]/a/text()'))
            author_url = textify(node.select('.//dt[@class="revUserFaceName"]/span/@href'))or textify(node.select('.//dt[@class="revUserFaceName reviewer"]/a/@href'))
            text = textify(node.select(' .//dd[@class="revRvwUserEntryCmt description"]//text()'))
            title = textify(node.select('.//dt[@class="revRvwUserEntryTtl summary"]//text()'))
            comment_link = textify(node.select('.//dd[@class="revRvwUserEntryOther"]/a/@href'))
            sk = comment_link

            values = [xcode(product_title), xcode(title), xcode(text), xcode(comment_link), date, xcode(author_name), review_rating, xcode(product_link)]

            for col_count, value in enumerate(values):
                todays_excel_sheet1.write(row_count, col_count, value)
                print value

            row_count = row_count+1
            print row_count
        todays_excel_file.save(excel_file_name)


        nxt_pg = textify(hdoc.select('//div[@class="revPagination"]/a[last()]/@href'))
        yield Request(nxt_pg,self.parse_details,response, meta={'row_count':row_count})
