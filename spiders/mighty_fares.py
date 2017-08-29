from juicer.utils import*
from dateutil import parser
import xlwt

class Mightyfares(JuicerSpider):
    name = 'mighty_fares'
    start_urls = ['http://mightyfares.com/']

    fp = open('fares.txt', 'w')

    def __init__(self, *args, **kwargs):
        super(Mightyfares, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.pop('start_urls', [])]

    def parse(self,response):
        hdoc = HTML(response)
        is_nxt = True
        nodes = hdoc.select('//article[contains(@id, "post-")]')
        for node in nodes:
            date = textify(node.select('.//span[@class="date"]//a/time/@datetime'))
            date = date.replace('+00:00','').replace('T',' ')
            if '2016-10-19' in date:
                continue
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            if date_added < get_current_timestamp()-86400*30:
                is_nxt = False
                continue
            link = textify(node.select('.//h2/a/@href'))
            yield Request(link,self.parse_details,response)
        
        nxt_pg = textify(hdoc.select('//div[@class="pagination"]//li[@class="current"]//following-sibling::li[1]/a/@href'))
        if nxt_pg and is_nxt:
            yield Request(nxt_pg,self.parse,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//h1[@class="entry-title"]/text()'))
        text = textify(hdoc.select('//div[@class="entry-content"]//text()'))
        ext_txt = textify(hdoc.select('//div[@class="entry-content"]/center//text()'))
        jun_txt = textify(hdoc.select('//div[@class="clear"]/following-sibling::div[@class="tags"]//text()'))
        junk_txt = textify(hdoc.select('//div[@id="disqus_thread"]/following-sibling::script/text()'))
        text =  text.replace('Advertisements (adsbygoogle=window.adsbygoogle||[]).push({});','').replace('Previous Next','')
        text =  text.replace(junk_txt,'').replace(ext_txt,'').replace(jun_txt,'').replace('Previous','')
        date = textify(hdoc.select('//span[@class="date"]//a/time/@datetime'))
        date = date.replace('+00:00','').replace('T',' ')
        dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
        author = textify(hdoc.select('//span[@class="author"]/a[@rel="author"]/text()'))
        auth_url = textify(hdoc.select('//span[@class="author"]/a[@rel="author"]/@href'))
        
        values = [xcode(response.url),xcode(title), xcode(text),xcode(date), xcode(dt_added), xcode(author), xcode(auth_url)]
        self.fp.write('%s\n' %values)
        self.fp.flush()

