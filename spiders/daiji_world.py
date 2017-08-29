from juicer.utils import*
from dateutil import parser

class DaijiWorld(JuicerSpider):
    name = 'daiji_world'
    start_urls = ['http://www.daijiworld.com/news/default.asp?city=topstories&tr=7','http://www.daijiworld.com/news/default.asp?city=health&tr=7','http://www.daijiworld.com/news/default.asp?city=kar&tr=7','http://www.daijiworld.com/news/default.asp?city=me&tr=7','http://www.daijiworld.com/news/default.asp?city=mah&tr=7','http://www.daijiworld.com/news/default.asp?city=sports&tr=7','http://www.daijiworld.com/news/default.asp?city=entertainment&tr=7','http://www.daijiworld.com/news/default.asp?city=others&tr=7','http://www.daijiworld.com/news/default.asp?city=usa&tr=7','http://www.daijiworld.com/news/default.asp?city=goa&tr=7','http://www.daijiworld.com/news/default.asp?city=business&tr=7','http://www.daijiworld.com/news/default.asp?city=editor&tr=7','http://www.daijiworld.com/news/default.asp?city=photoalbum&tr=7']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//b/a/@href')
        for url in urls:
            url = 'http://www.daijiworld.com/%s' %(textify(url))
            yield Request(url,self.parse_next,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//td//h1//text()'))
        text1 = textify(hdoc.select('//p/strong/text()'))
        if text1:
            text1 = textify(hdoc.select('//p/strong/text()')[0])
        text = textify(hdoc.select('//p/text()'))
        if text1:
            text = text1 + text
        dt_added = textify(hdoc.select('//td[@valign="top"]/b/text()'))
        author = hdoc.select('//td[@class="news"]//p/em//strong[contains(text(),":")]//text()')
        if not author:
            author = hdoc.select('//td[@class="news"]//p//em//strong//text()')
        if author:
            author = textify(author[0])
            author = author.replace("Pics:","").strip()
            author = author.replace("Report:","").strip()
            author = author.replace("By","").strip()
            author = author.replace("Pics by","").strip()
        else:
            author = ''
        dt_added = get_timestamp(parse_date(dt_added) - datetime.timedelta(hours=5, minutes=30))

        item =Item(response)
        item.set("title",title)
        item.set("text",text)
        item.set("dt_added",dt_added)
        item.set("author.name",author)
        item.set('url', response.url)
        yield item.process()

