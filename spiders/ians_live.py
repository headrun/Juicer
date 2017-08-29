from juicer.utils import *
from dateutil import parser
import requests
from scrapy.http import FormRequest


class IansLive(JuicerSpider):
    name = "ians_live"
    #start_urls = ['http://ianslive.in/index.php?param=category/NATION/1','http://ianslive.in/index.php?param=category/SPORTS/9','http://ianslive.in/index.php?param=category/INTERNATIONAL/13','http://ianslive.in/index.php?param=category/BUSINESS/5','http://ianslive.in/index.php?param=category/ENTERTAINMENT/15','http://ianslive.in/index.php?param=category/SCIENCE%20and%20TECHNOLOGY/36', 'http://ianslive.in/index.php?param=section/31', 'http://ianslive.in/index.php?param=section/35', 'http://ianslive.in/index.php?param=section/33']
    start_urls = ['http://ianslive.in/index.php?param=category/NATION/1']

    def parse(self, response):
        hdoc = HTML(response)
        nodes = hdoc.select('//div[@class="listholder"]/a/@href').extract()
        for link in nodes:
            if 'http' not in link: link = 'http://ianslive.in/' + link
            #yield Request(link, self.parse_details, response)

        data = ''.join(re.findall('\category(.*)',response.url))
        headers = {
        'Referer' : 'http://www.ianslive.in/index.php?param=category' + data
        }
        import pdb;pdb.set_trace() 
        for i in range(2, 10):
            form_data = {'param' : 'categorypaging' + data + '%s' % i}
            res_url = 'http://ianslive.in/categorypaging2.php'
            yield FormRequest(res_url, callback = self.parse, \
                    formdata = form_data, headers = headers, dont_filter = True)

    def parse_details(self, response):
        hdoc = HTML(response)

        title = textify(hdoc.select('//span[@class="landingheading"]//text()'))
        text = textify(hdoc.select('//div[@class="landingstory"]//p//text()')[:-9] )
        dt_added = textify(hdoc.select('//div[@class="landingstory"]/p/b/text()')[1])
        (extra_data,dt_added) = dt_added.split(':')
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))
        item = Item(response)
        item.set('title', title)
        item.set('text', text)
        item.set('dt_added', dt_added)
        item.set('url', response.url)
        yield item.process()
