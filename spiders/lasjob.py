from juicer.utils import *
from dateutil import parser

class Lasjob(JuicerSpider):
    name = 'lasjob'
    start_urls = ['http://www.simplylawjobs.com/jobs']

    def parse(self,response):
        hdoc = HTML(response)
        job_url = hdoc.select('//div[@class="info_box"]/div[contains(@class, "info")]/a/@href').extract()
        for job in job_url:
            url = urljoin(response.url, job)
            yield Request(url,callback=self.parse_job)

        nxt_pg = textify(hdoc.select('//div[@id="pagination"]//a[contains(.,">>")]/@href'))
        if nxt_pg:
            yield Request(urljoin(response.url,nxt_pg[0]), self.parse)


    def parse_job(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        

