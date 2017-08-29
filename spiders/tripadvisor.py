from juicer.utils import *

class TripAdvisor(JuicerSpider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.in']
    start_urls = ['http://www.tripadvisor.in/Hotels-g293860-India-Hotels.html']

    def parse(self, response):
        hdoc = HTML(response)
        self.latest_dt = parse_date('2014-11-06')
        self.latest_dt=parse_date('2014-11-06')   

        if self.latest_dt:self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        urls = hdoc.select_urls(['//div[@class="geo_name"]/a/@href'], response)
        for url in urls:
            print url
            yield Request(url, self.parse, response)
            

        nodes = hdoc.select('//div[@class="maincontent rollup"]//div[@class="geos_grid"]//div[@class="geos_row"]//div[@class="geo_entry"]')
        for node in nodes:
            '''
            _date = textify(node.select(''))
            if _date:
                _date = parse_date(_date, True)
            if not _date:
                continue
            if _date >= self.latest_dt:
                url = textify(node.select('./li[1]//a/@href'))
            '''   
            yield Request(url, self.parse_terminal, response)

        #next_url = textify(hdoc.select('//div[@class="pgLinks"]//\
         #             a[@class="guiArw sprite-pageNext "]/@href'))
        #if next_url:yield Request(next_url, self.parse, response)


    def parse_terminal(self, response):
        hdoc = HTML(response)

        #next_page = ''
        posts = hdoc.select('//div[@id="REVIEWS"]//div[contains(@id,"review_")]')
        for post in posts:
            item = Item(response)
            post_dt = textify(post.select('.//div[@class="rating reviewItemInline"]//span[@class="ratingDate relativeDate"]'))
            post_dt = parse_date(str(re.sub(r'Reviewed', '', post_dt)).strip(), True)
            if not post_dt:
                continue

            if post_dt >= self.latest_dt:
                if self.flag:self.update_dt(post_dt)
                '''
                next_page = textify(hdoc.select('//div[@class="pgLinks"]//a[@class="guiArw sprite-pageNext "]/@href'))
                author_name = textify(post.select('.//div[@class="username mo"]/span/text()'))
                author_url = 'http://www.tripadvisor.in/members/' + author_name.strip().replace(r' ','_')
                '''
                text = post.select('//div[@class="entry"]//p/text()')
                text = textify(text).encode('utf8').decode('ascii','ignore')
                text = text.replace('&gt;','>').replace('&lt;','<').strip()
                print "text==========",text
                title = textify(hdoc.select('//div[@class="quote"]//text()'))
                title = title.encode('utf8').decode('ascii','ignore')
                print "title++++++++++",title
                #title = title.replace('&gt;','>').replace('&lt;','<')
                '''
                post_id = textify(post.select('.//p[contains(@id,"review_")]/@id'))
                url = re.sub(r'#UR.*','',response.url)+'#'+post_id
                sk = ''.join(re.findall(r'\d+', post_id))

                item.set('sk', sk)
                item.set('dt_added', post_dt)
                item.set('title', xcode(title.strip()))
                item.set('author.name', xcode(author_name))
                item.set('author.url', xcode(author_url))
                item.set('text', xcode(text))
                item.set('url', xcode(url))

                #yield item.process()

        if next_page:
            yield Request(next_page, self.parse_terminal, response)
        '''
