from scrapy.http import FormRequest

from juicer.utils import *
class Finalaya(JuicerSpider):
    name = "finalaya"
    start_urls = "http://www.finalaya.com/News/Search.aspx"
    def parse(self,response):
        hdoc = HTML(response)
        if self.latest_dt:self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        check_date = self._latest_dt + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_date - oneweek_diff

        nodes = hdoc.select('//li[contains(@style, "float")]')
        is_next = False
        for node in nodes:
            post_date = textify(node.select('.//span[@style]//span'))
            post_date = parse_date(post_date)
            if post_date >= self.cutoff_dt:
                is_next = True
                url = textify(node.select('./a/@href'))
                yield Request(url,self.parse_next,response)

        if is_next:
            from_date = textify(hdoc.select('//input[@name="ctl00$BodyCPH$txtFromDate"]/@value'))
            to_date = textify(hdoc.select('//input[@name="ctl00$BodyCPH$txtToDate"]/@value'))
            view_state = textify(hdoc.select('//input[@name="__VIEWSTATE"]/@value'))
            curr_page = textify(hdoc.select('//input[@name="ctl00$BodyCPH$Pagination$HdnPageNo"]/@value'))
            next_page = int(curr_page) + 1
            total_pages = textify(hdoc.select('//input[@name="ctl00$BodyCPH$Pagination$HdnTotalPages"]/@value'))
            post_data = {}
            post_data['ctl00$BodyCPH$txtFromDate'] = from_date
            post_data['ctl00$BodyCPH$txtToDate'] = to_date
            post_data['__VIEWSTATE'] = view_state
            post_data['ctl00$BodyCPH$Pagination$HdnPageNo'] = str(next_page)
            post_data['ctl00$BodyCPH$Pagination$HdnTotalPages'] = total_pages
            yield FormRequest(url = response.url, callback = self.parse, method = 'POST', formdata = post_data, dont_filter = True)


    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//span[@id="ctl00_BodyCPH_lblFirstHeading"]//text()'))
        text = textify(hdoc.select('//p//span[@id="ctl00_BodyCPH_lblAnnDetail"]//text()'))
        date_info = textify(hdoc.select('//span[@id="ctl00_BodyCPH_lblTime"]//text()'))

        item = Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set("dt_added",date)
        item.set("url", response.url)
        yield item.process()
