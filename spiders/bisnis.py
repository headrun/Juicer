from juicer.utils import *
class Bisnis(JuicerSpider):
    name = "bisnis"
    start_urls = ['http://dapurpacu.com/category/auto-news/auto-show/tokyo-motor-show/', 'http://dapurpacu.com/category/auto-news/gallery/photos/', 'http://dapurpacu.com/category/auto-news/auto-show/bangkok-motor-show/', 'http://dapurpacu.com/category/auto-news/motor/motor-modifikasi/', 'http://dapurpacu.com/category/auto-news/balap/', 'http://dapurpacu.com/category/auto-news/mobil/mobil-modifikasi/', 'http://dapurpacu.com/category/auto-news/wacana/', 'http://dapurpacu.com/category/auto-news/ragam/pernik/', 'http://dapurpacu.com/category/auto-news/ragam/', 'http://dapurpacu.com/category/auto-news/mobil/', 'http://dapurpacu.com/category/auto-news/komunitas-mobil-motor/komunitas-motor/', 'http://dapurpacu.com/category/auto-news/motor/motor-klasik/', 'http://dapurpacu.com/category/auto-news/komunitas-mobil-motor/', 'http://dapurpacu.com/category/auto-news/motor/', 'http://dapurpacu.com/category/auto-news/auto-show/detroit-motor-show/', 'http://dapurpacu.com/category/auto-news/bengkel-mobil-motor/teknologi-bengkel/', 'http://dapurpacu.com/category/auto-news/balap/balap-mobil/', 'http://dapurpacu.com/category/auto-news/bengkel-mobil-motor/komponen/', 'http://dapurpacu.com/category/auto-news/mobil/group-test/', 'http://dapurpacu.com/category/auto-news/balap/balap-motor/', 'http://dapurpacu.com/category/auto-news/auto-news/auto-issue/', 'http://dapurpacu.com/category/auto-news/mobil/mobil-baru/', 'http://dapurpacu.com/category/auto-news/auto-news/auto-business/', 'http://dapurpacu.com/category/auto-news/auto-show/indonesia-motor-show/', 'http://dapurpacu.com/category/auto-news/komunitas-mobil-motor/komunitas-mobil/', 'http://dapurpacu.com/category/auto-news/tips-mobil-motor/', 'http://dapurpacu.com/category/auto-news/bengkel-mobil-motor/pabel-ahli/', 'http://dapurpacu.com/category/auto-news/mobil/mobil-klasik/', 'http://dapurpacu.com/category/auto-news/tips-mobil-motor/tips-motor/', 'http://dapurpacu.com/category/auto-news/auto-show/geneva-motor-show-auto-show/', 'http://dapurpacu.com/category/auto-news/tips-mobil-motor/tips-mobil/', 'http://dapurpacu.com/category/auto-news/gallery/', 'http://dapurpacu.com/category/auto-news/bengkel-mobil-motor/', 'http://dapurpacu.com/category/auto-news/motor/motor-tes/', 'http://dapurpacu.com/category/auto-news/motor/motor-baru-motor/', 'http://dapurpacu.com/category/auto-news/motor/motor-konsep/', 'http://dapurpacu.com/category/auto-news/auto-show/china-motor-show/', 'http://dapurpacu.com/category/auto-news/auto-news/', 'http://dapurpacu.com/category/auto-news/auto-show/', 'http://dapurpacu.com/category/auto-news/mobil/mobil-konsep/', 'http://dapurpacu.com/category/auto-news/ragam/auto-gadget/']
    def parse(self,response):
         hdoc = HTML(response)
         urls = hdoc.select_urls('//div[@class="box-content"]//div[@class="box-content-title"]/a/@href',response)
         for each_url in urls:
            yield Request(each_url,self.parse_next,response)
         next_url=textify(hdoc.select('//div[@class="cat-content"]//div[@class="pagenavi"]//div[@class="wp-pagenavi"]/a[@class="nextpostslink"]/@href'))
         if next_url:
            yield Request(next_url,self.parse,response)
    def parse_next(self,response):
         hdoc = HTML(response)
         title = textify(hdoc.select('//div[@class="single-title"]//h1'))
         text = textify(hdoc.select('//div[@class="content"]/p'))
         info = textify(hdoc.select('//span[@class="author"]'))
         (author,date) = info.split("/")
         tags=textify(hdoc.select('//div[@class="tags"]'))
         (aa,tag) = tags.split(":")
         tag_list = tag.split("#")
         date = get_timestamp(parse_date(date) - datetime.timedelta(hours=7))

         item = Item(response)
         item.set('title', title)
         item.set('text', text)
         item.set('tags', tag_list)
         item.set('author.name', author.strip())
         item.set('dt_added', date)
         item.set('url', response.url)

         if date > 1396598813:
             yield item.process()


