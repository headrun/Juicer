from juicer.utils import *
from dateutil import parser
import xlwt

excel_file_name = 'amazon_jp.xlsx'
header = ['Product Title', 'Review Title', 'Review Details', 'Review URL', 'Review DateTime', 'Reviewd By', 'Review Rating', 'Product URL']

todays_excel_file = xlwt.Workbook(encoding="utf-8")
todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1")

for i, row in enumerate(header):
    todays_excel_sheet1.write(0, i, row)


class AmazonJapanreviews(JuicerSpider):
    name = 'amazon_jp_xl'
    start_urls = ['http://www.amazon.co.jp/product-reviews/B019RAUO18/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=1']

    def parse(self,response):
        hdoc = HTML(response)
        f = open('amazon_pg1','r')
        lines = f.readlines()
        for row in lines:
            yield Request(row,self.parse_links,response)

    def parse_links(self,response):
        hdoc = HTML(response)
        review_link = textify(hdoc.select('//div[@id="revF"]/div/a/@href'))
        yield Request(review_link,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)

        try:row_count = response.meta['row_count']
        except: row_count = 1

        nodes = hdoc.select('//div[@id="cm_cr-review_list"]/div[@class="a-section review"]')
        product_title = textify(hdoc.select('//div[@class="a-row product-title"]//a/text()'))
        product_link = textify(hdoc.select('//div[@class="a-row product-title"]//a/@href'))
        if 'http' not in product_link: product_link = 'http://www.amazon.co.jp' + product_link

        for node in nodes:
            _id = textify(node.select('.//@id[1]'))
            author = textify(node.select('.//span[contains(@class,"review-byline")]/a/text()')) or textify(node.select('.//span[contains(@class,"review-byline")]/text()'))
            author_link =textify(node.select('.//span[contains(@class,"review-byline")]/a/@href'))
            if 'http' not in author_link:author_link = 'http://www.amazon.co.jp' + author_link
            date = textify(node.select('.//span[contains(@class,"review-date")]'))
            date = '/'.join(re.findall('\d+',date))
            title = textify(node.select('.//a[contains(@class,"review-title")]/text()'))
            title_link = textify(node.select('.//a[contains(@class,"review-title")]/@href'))
            if 'http' not in title_link: title_link = 'http://www.amazon.co.jp' + title_link
            text = textify(node.select('.//span[contains(@class,"review-text")]//text()'))
            rating = textify(node.select('.//i[contains(@class,"review-rating")]/span/text()'))
            if rating: rating = rating.split(u'\u3064\u661f\u306e\u3046\u3061')[-1]
            url = product_link + '#' + _id
            sk = hashlib.md5(xcode(url)).hexdigest()

            values = [xcode(product_title), xcode(title), xcode(text), response.url + '#' + _id, date, xcode(author), rating, xcode(product_link)]
            for col_count, value in enumerate(values):
                print value
                todays_excel_sheet1.write(row_count, col_count, value)

            print row_count
            row_count = row_count+1
        todays_excel_file.save(excel_file_name)

        next_pg = textify(hdoc.select('//li[@class="a-last"]/a/@href'))
        import pdb;pdb.set_trace()
        if next_pg:
           next_pg = 'http://www.amazon.co.jp' +  xcode(next_pg)
           yield Request(next_pg,self.parse_details,response, meta={'row_count':row_count, 'dont_redirect':True,'handle_httpstatus_list':[301]})
