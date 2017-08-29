from juicer.utils import *
import json
from scrapy.http import FormRequest
import datetime

def get_starturls():
    data = urllib.urlopen('http://data.cloudlibs.com/sea/?action=get&key=3DD578J7N13N97RD3COQX37P9E7IWXZFN1YQPE5F&source=baidu_news').read()
    data = json.loads(data)

    url = 'http://www.soubao.net/search/searchList.aspx?keyword=%s&startdate=%s&enddate=%s&timesel=halfyear'
    urls = []

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    last_month = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    for keyword in data['result'][:10]:
        keyword = urllib.quote('"%s"' %keyword.encode('utf8'))
        urls.append(url %(keyword, last_month, now))
    return urls

class Soubao(JuicerSpider):
    name = 'soubao_net'
    start_urls = get_starturls()
    handle_httpstatus_list = [500]

    def parse(self,response):
        hdoc = HTML(response)
        nodes = hdoc.select('//ul[@class="newList"]/li')
        if not nodes:pass

        for node in nodes:
            date = textify(node.select('.//em[@class="postDate"]/span/text()'))
            dt_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=8))
            news_url = textify(node.select('.//h2//a/@href'))
            if not news_url: news_url = textify(node.select('.//input[2]/@value'))
            title = textify(node.select('.//h2//a/text()'))
            news_paper = textify(node.select('.//em[@class="paperName"]/span/text()'))
            text = textify(node.select('.//p//span//text()'))
            print 'url:',news_url
            print 'title:',title
            print 'date:',date
            print 'news_paper:',news_paper
            print 'text:',text

            item = Item(response)
            item.set('title',xcode(title))
            item.set('dt_added',dt_added)
            item.set('text',xcode(text))
            item.set('url',news_url)
            item.set('sk',md5(url))
            item.set('source',xcode(news_paper))
            item.set('xtags',['soubao_sourcetype_manual','news_sourcetype_manual','china_country_manual'])
            #yield item.process()

        search_keyword = response.url.split('keyword=')[-1].split('&')[0]
        next_page = "".join(hdoc.select('//div[@class="paginator"]/span[@class="cpb"]/following-sibling::a[1]/text()').extract())

        li = hdoc.select('//ul[@class="newList"]//h2/input/@value').extract()
        li_1 = []
        for i in range(1,len(li)):
            if i < 9: i = '0'+str(i)
            _id = 'rptRetList$ctl'+str(i)+'$HidKID'
            li_1.append(_id)
            _url = 'rptRetList$ctl'+str(i)+'$HidUrl'
            li_1.append(_url)
        form_dict = dict(zip(li_1,li))
        if next_page:
            form_data = {'HidDTSel':'halfyear','HidGroupType':'PT','HidGroupValue':'','HidTJ':'','__EVENTARGUMENT':next_page,'__EVENTTARGET':'AspNetPager1','__EVENTVALIDATION':'/wEWMALx4LqrBgL9vLWgAQL+lJT0DQLirLWcDAKI++TlCQLeipm1AwLg2ZOZCALChrSLDgLG7+WECAK0zJWCDALG7/m/BwK0zKm9CwLG7437BgK0zL34CgLG78HfAgK0zPHcBgLG79WaAgK0zIWYBgLG7+nVAQK0zJnTBQLG7/2QAQK0zK2OBQLG7/HyBAK0zKHwCALG74WuBAK0zLWrCALd2fXhAgL7yYKzCQLd2YmdAgL7yZbuCALd2Z3YAQL7yaqpCALd2bGTAQL7yb7kBwLd2eX3DAL7yfLIAwLd2fmyDAL7yYaEAwLd2Y3uCwL7yZq/AgLd2aGpCwL7ya76AQLd2ZWLDwL7yaLcBQLd2anGDgL7ybaXBQK4g7vSBgLW88ejDQFzIahsN5ue7iNkSCSor+55wAXw','__VIEWSTATE':'/wEPDwUKLTg3MzI5ODQ4OA9kFgICAQ9kFgQCBw8PFgIeBFRleHQF7wE8c3Bhbj7lhbPplK7lrZfvvJo8ZW0gY2xhc3M9ImtleXdvcmRzIj48L2VtPjwvc3Bhbj7msYnor60gPHNwYW4+5b2T5YmN56ysMS8xMDIz6aG1PC9zcGFuPiA8c3Bhbj7lhbEyMDQ1M+adoeiusOW9lTwvc3Bhbj4gPHNwYW4+5q+P6aG1MjDmnaE8L3NwYW4+IDxzcGFuPuaXpeacn+iMg+WbtO+8mjxlbSBjbGFzcz0iZnJvbSI+MjAxNS0wMi0xNzwvZW0+PGVtIGNsYXNzPSJ0byI+6IezMjAxNS0wOC0xNzwvZW0+PC9zcGFuPmRkAgkPDxYEHgtSZWNvcmRjb3VudALlnwEeEEN1cnJlbnRQYWdlSW5kZXgCAWRkZJDuKd1ItXNnFADJwjfm1SWSm3C9','__VIEWSTATEGENERATOR':'D7D27839','timesel':'on','txtKeyWord':search_keyword,'txtendDate':'2015-08-17','txtstartDate':'2015-02-17'}
            formdata = dict(form_data.items()+form_dict.items())
            yield FormRequest(response.url,self.parse,formdata=formdata)
        else:pass
