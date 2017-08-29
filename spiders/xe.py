from juicer.utils import *
class Xe(JuicerSpider):     
     name = "xe"
     start_urls = ["http://kienthuc.net.vn/phu-kien-xe/", "http://kienthuc.net.vn/xe/", "http://kienthuc.net.vn/dan-choi-xe/"]
     #start_urls = "http://kienthuc.net.vn/xe/"
     def parse(self,response):
         hdoc = HTML(response)
         urls = hdoc.select_urls('//div[@class="listNsub clearfix"]//section[@class="cat-listnews hzol-clear"]//h4//a/@href',response)
         for each_url in urls:
            yield Request(each_url,self.parse_next,response)
         next_urls = textify(hdoc.select('//div[@class="container"]//div[@class="vov-pager"]//ul[@class="pagination pagination-sm"]//a[@class="next"]/@href'))
         if next_urls:
            yield Request(next_urls,self.parse,response)
     def parse_next(self,response):
         hdoc = HTML(response)
         title = textify(hdoc.select('//section[@class="main-article clearfix"]//h1/text()'))
         if not title:
            title = textify(hdoc.select('//div[@class="article-info"]//h3[@class="title"]'))
         text = textify(hdoc.select('//div[@class="text"]//div[@id="abody"]//div'))
         if not text:
            text = textify(hdoc.select('//div[@class="article-info"]//div[@class="summary"]'))
         info = textify(hdoc.select('//div[@class="meta clearfix"]/time'))
         if not info:
            info = textify(hdoc.select('//div[@class="article-info"]//div[@class="meta"]'))
         tag=textify(hdoc.select('//div[@class="tag"]'))
         tags_list=[]
         (t,n)=tag.split(":")
         tags = n.split(",")

         author=textify(hdoc.select('//div[@class="author"]//span[@class="name"]'))
         if not author:
            author = textify(hdoc.select('//div[@class="article-info"]//div[@class="author"]'))

         date = get_timestamp(parse_date(info[14:31]) - datetime.timedelta(hours=7))

         item = Item(response)
         item.set('title', title)
         item.set('text', text)
         item.set('tags', tags)
         item.set('dt_added', date)
         item.set('url', response.url)
         item.set('author.name', author)

         if date >1396598813:
             yield item.process()
