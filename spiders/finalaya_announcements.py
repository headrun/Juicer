from scrapy.http import FormRequest

from juicer.utils import *
class FinalayaAnnouncements(JuicerSpider):
    name= "finalaya_announcements"
    start_urls ="http://www.finalaya.com/"

    def parse(self,response):
        hdoc =HTML(response)
        if self.latest_dt:
            import pdb;pdb.set_trace()
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        check_date = self.latest_dt + datetime.timedelta(hours=8)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt = check_date - oneweek_diff

        url = "http://www.finalaya.com/Companies/Announcements/"
        yield Request(url,self.parse_next,response, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36', 'X-MicrosoftAjax':'Delta=true', 'X-Requested-With':'XMLHttpRequest'}, dont_filter=True, meta={'is_next': True})

    def parse_next(self,response):
        hdoc =HTML(response)
        nodes = hdoc.select('//li[contains(@id, "ctl00_BodyCPH_CorpAnnouncements_rptCorpInfo")]')
        is_next = response.meta.get('is_next', False)

        for node in nodes[:2]:
            post_date = textify(node.select('./h3/span[contains(@id, "Date")]'))
            post_date = parse_date(post_date)
            if post_date >= self.cutoff_dt:
                is_next = True
                url = textify(node.select('./h3/a/@href'))
                yield Request(url, self.parse_page, response)

        if is_next:
            view_state = textify(hdoc.select('//input[@name="__VIEWSTATE"]/@value'))
            curr_page = textify(hdoc.select('//input[@name="ctl00$BodyCPH$CorpAnnouncements$Pagination$HdnPageNo"]/@value'))
            total_pages = textify(hdoc.select('//input[@name="ctl00$BodyCPH$CorpAnnouncements$Pagination$HdnTotalPages"]/@value'))
            hdn_status = textify(hdoc.select('//input[@name="ctl00$BodyCPH$CorpAnnouncements$hdnStatus"]/@value'))
            if not curr_page:
                curr_page = 0
            next_page = int(curr_page) + 1

            post_data = {}
            if not hdn_status or hdn_status=="latest":
                post_data['__EVENTTARGET'] = "ctl00$BodyCPH$CorpAnnouncements$lnkWeek"
            else:
                post_data['__EVENTTARGET'] = "dummy"
            post_data['ctl00$BodyCPH$CorpAnnouncements$hdnStatus'] = hdn_status
            post_data['__VIEWSTATE'] = view_state
            post_data['ctl00$BodyCPH$CorpAnnouncements$Pagination$HdnPageNo'] = str(next_page)
            post_data['ctl00$BodyCPH$CorpAnnouncements$Pagination$HdnTotalPages'] = total_pages

            yield FormRequest(url = response.url, callback = self.parse_next, method = 'POST', formdata = post_data, dont_filter = True)


    def parse_page(self, response):

        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="tabVR1data"]//h2//span[@id="ctl00_BodyCPH_CorpAnnouncements_lblCompany"]//text()'))
        text = textify(hdoc.select('//div[@class="tabVR1data"]//div[@class="ann_content"]//text()'))
        date = textify(hdoc.select('//div[@class="tabVR1data"]//span[@id="ctl00_BodyCPH_CorpAnnouncements_lblAnnDate"]//text()'))
        date = get_timestamp(parse_date(date) + datetime.timedelta(hours=8))
        import pdb;pdb.set_trace()
'''
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', date)
        item.set('url', response.url)
        yield item.process()'''
