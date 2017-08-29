from juicer.utils import *
from dateutil import parser

class OrientalDailyMalaysia(JuicerSpider):
    name = 'orientaldaily_my'
    start_urls = ['http://www.orientaldaily.com.my/nation','http://www.orientaldaily.com.my/business','http://www.orientaldaily.com.my/society','http://www.orientaldaily.com.my/north','http://www.orientaldaily.com.my/central','http://www.orientaldaily.com.my/south','http://www.orientaldaily.com.my/east-malaysia','http://www.orientaldaily.com.my/international','http://www.orientaldaily.com.my/sports','http://www.orientaldaily.com.my/entertainment','http://www.orientaldaily.com.my/diantai','http://www.orientaldaily.com.my/wangshi','http://www.orientaldaily.com.my/maidong','http://www.orientaldaily.com.my/luntan','http://www.orientaldaily.com.my/qunying','http://www.orientaldaily.com.my/longmen','http://www.orientaldaily.com.my/mingjia','http://www.orientaldaily.com.my/wenhui','http://www.orientaldaily.com.my/lunjian','http://www.orientaldaily.com.my/family','http://www.orientaldaily.com.my/health','http://www.orientaldaily.com.my/tech','http://www.orientaldaily.com.my/food','http://www.orientaldaily.com.my/education','http://www.orientaldaily.com.my/luxury','http://www.orientaldaily.com.my/car','http://www.orientaldaily.com.my/funnews']

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.latest_dt = None
        if kwargs.get("LASTRUN"):
            self.latest_dt = get_datetime(float(kwargs.get("LASTRUN")))
        self.cutoff_dt = None
        self.flag = False


    def parse(self,response):
        hdoc = HTML(response)
        is_next = True

        if self.latest_dt is None :
            self.latest_dt = self._latest_dt
            self.flag = True

        if self.cutoff_dt is None:
            check_date = self._latest_dt + datetime.timedelta(hours=8)
            oneweek_diff = datetime.timedelta(days=7)
            self.cutoff_dt = check_date - oneweek_diff

        links = hdoc.select('//div[@class="item news"]')
        for link in links:
            date = '-'.join(re.findall('\d+',textify(link.select('./p[@class="meta quiet small"]/text()'))))
            import pdb;pdb.set_trace()
            date_added = parse_date(xcode(date))
            if date_added < self.cutoff_dt
                is_next = False
                continue
            news_link = textify(link.select('./h4/a/@href'))
            yield Request(news_link,self.details,response)

        nxt_pg = textify(hdoc.select('//a[@class="next"]/@href'))
        if nxt_pg:
            yield Request(nxt_pg,self.parse,response)

    def details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@id="article"]//h1[@class="left"]/text()'))
        text = textify(hdoc.select('//div[@class="columns large-7 medium-6 small-12"]//text()'))
        published = textify(hdoc.select('//div[@id="article"]//div[@class="meta"]/text()'))
        try:dt = '-'.join(re.findall('\d+',published.split('|')[0]))
        except:dt = '-'.join(re.findall('\d+',published))
        dt_added = get_timestamp(parse_date(xcode(dt)) - datetime.timedelta(hours=8))
        if '|' in  published:author = published.split('|')[-1].split(u'\uff1a')[-1]
        else:author = ''
"""
        item = Item(response)
        item.set('url',response.url)
        item.set('title',xcode(title))
        item.set('dt_added',dt_added)
        if author:item.set('author',{'name':xcode(author)})
        item.set('text',xcode(text))
        item.set('xtags', ['malaysia_country_manual', 'news_sourcetype_manual'])
        yield item.process()
        """
