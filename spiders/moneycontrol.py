from juicer.utils import *
class MoneyControl(JuicerSpider):
    name = "moneycontrol"
    start_urls = "http://www.moneycontrol.com"
    def parse(self,response):
        hdoc =HTML(response)
        import pdb;pdb.set_trace()
        urls = hdoc.select_urls('//ul[@class="FL"]//li//a[contains(text(),"All")]//@href',response)
        self.next_urls = []
        self.latest_dt = parse_date('2014-10-15')
        check_date = self._latest_dt+datetime.timedelta(hours=0)
        oneweek_diff = datetime.timedelta(days=7)
        self.cutoff_dt=check_date-oneweek_diff
        yield Request(urls,self.parse_links,response)



    def parse_links(self,response):
        hdoc = HTML(response)

        all_links = hdoc.select('//div[@class="PL15 MT15 PR20 PB20"]//ul//li')
        is_next = False
        for link in all_links[:2]:
            post_date_time = xcode(textify(link.select('.//p[@class="date PT3"]//text()'))).split('|')[0]
            post_date=parse_date(post_date_time.replace('.', ':'))
            url = textify(link.select('.//div[@class="colR"]//a//@href'))
            if post_date >= self.latest_dt and url and '/video/' not in url:
                is_next = True
                yield Request(url, self.parse_next,response)

        next_urls = hdoc.select('//div[@class="paging MT20"]/a[contains(@href, "next")]/@href')
        if next_urls and is_next:
            for next_url in next_urls:
                next_url = textify(next_url)
                if next_url not in self.next_urls:
                    self.next_urls.append(next_url)
                    yield Request(next_url,self.parse_links,response)

    def parse_next(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="PL20 PR15 brdr PT15 PB15"]//h1//text()'))
        text = textify(hdoc.select('//div[@class="PL20 PR15 brdr PT15 PB15"]/p[@class="subTitle brdb PT10"]/em/text()'))
        data = textify(hdoc.select('//div[@class="op_gd14 FL"]//text()'))
        comment = textify(hdoc.select('//div[@class="clearfix PT20"]//div[@class="FR"]//a//text()'))
        date_info = textify(hdoc.select('//div[@class="tpIcnDt clearfix"]//div[@class="FL"]//text()'))
        (date,info)=date_info.split("|")
        author = textify(hdoc.select('//div[@class="FL"]/p/a[@class="UC blOnsb12"]//text()'))
        dt_added = get_timestamp(parse_date(date.replace('.', ':')) - datetime.timedelta(hours=5, minutes=30))
        text = text + " " + data
        import pdb;pdb.set_trace()

        print '/n'
        print response.url
        print 'title', xcode(title)
        print 'text' , xcode(text)
        print 'dt_added',  xcode(dt_added)
        print 'author', xcode(author)




        '''item=Item(response)
        item.set('title', title)
        item.set('text', text.strip())
        item.set('dt_added', dt_added)
        item.set('author.name', author)
        item.set('url', response.url)
        yield item.process()'''
