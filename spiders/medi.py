from juicer.utils import *

class MediGaurd(JuicerSpider):
    name = "medi"
    start_urls = ['https://www.mediguard.org/']#medication','https://www.mediguard.org/conditions']
    handle_httpstatus_list = [403]

    def parse(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        nodes = hdoc.select('//a[@class="drug_link"]')
        if not nodes: nodes = hdoc.select('//div[@id="conditions_menu"]//a')
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            '__unam':'ec43de5-14ede55a917-647adec8-111',
            #'session_id':'4cc54b775dbc50a0bc3aa8108857aa71',
            #'__utmt_UA-1133947-3':'1','__utmt_UA-7954366-7':'1',
            #'__utma':'180214968.1164997711.1438247940.1440419108.1440477050.7',
            #'__utmb':'180214968.2.10.1440477050','__utmc':'180214968',
            #'__utmz':'180214968.1438250453.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
            'Host':'www.mediguard.org',
            'Referer':'https://www.mediguard.org/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
        }
        yield Request('https://www.mediguard.org/medication',self.parse,headers=headers,dont_filter=True)
        for node in nodes:
            name = textify(node.select('.//text()'))
            url = textify(node.select('./@href'))
            if 'http:' not in url:
                url = 'https://www.mediguard.org'+xcode(url)
            yield Request(url,self.parse_next,response,meta={'name':name})

    def parse_next(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        try: reviews = textify(hdoc.select('//div[@id="medication-body"]//a[contains(@href,"comments")]/@href')[0])
        except: import pdb;pdb.set_trace()
        if not reviews: reviews = textify(hdoc.select('//div[@id="condition-body"]//a[contains(@href,"comments")]/@href')[0])
        if 'http:' not in reviews: reviews='https://www.mediguard.org'+str(reviews)
        yield Request(reviews,self.parse_reviews,response,meta={'name':response.meta['name']})

    def parse_reviews(self,response):
        hdoc = HTML(response)
        is_next = True
        nodes = hdoc.select('//div[@class="comment_block"]')

        for node in nodes:
            date = textify(node.select('.//span[@class="date"]//text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=-5))
            if dt_added < get_current_timestamp()-86400*90:
                is_next = False
                continue
            text = textify(node.select('.//p//text()'))
            sk = response.url+response.meta['name']+text

            item = Item(response)
            item.set('title',response.meta['name'])
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('url',response.url)
            item.set('sk',md5(sk))
            item.set('xtags',['forums_sourcetype_manual','usa_country_manual'])
            yield item.process()


        next_page = hdoc.select('//div[@class="pagination"]//ul/li/a/@href')
        if next_page and is_next:
            for url in next_page:
                url = 'https://www.mediguard.org'+url
                yield Request(url,self.parse_reviews,response,meta={'name':response.meta['name']})
