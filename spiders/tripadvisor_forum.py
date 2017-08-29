from juicer.utils import *
from dateutil import parser

class TripAdvisorForum(JuicerSpider):
    name = 'tripadvisor_forum1'
    start_urls = 'https://www.tripadvisor.in/ShowForum-g293860-i511-India.html'

    def parse(self,response):
        hdoc = HTML(response)
        forum_nodes = hdoc.select('//td[contains(@class,"datecol rowentry")]/parent::tr')

        for forum_node in forum_nodes:
            date = textify(forum_node.select('./td[contains(@class,"datecol rowentry")]/a/text()'))
            date_added = get_timestamp(parse_date(xcode(date)) - datetime.timedelta(hours=5,minutes=30))
            if date_added > get_current_timestamp()-86400*30:
                thread_url = textify(forum_node.select('./td[contains(@class,"datecol rowentry")]/a/@href'))
                if 'http' not in thread_url : thread_url = 'https://www.tripadvisor.in' + thread_url
                thread_url = 'https://www.tripadvisor.in/ShowTopic-g293860-i511-k5740951-Train_tickets_online_Solution-India.html'
                yield Request(thread_url,self.parse_details,response,meta={'dont_redirect':True,'handle_httpstatus_list':[302],'url':thread_url})

    def parse_details(self,response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        title = textify(hdoc.select('//span[@class="topTitleText"]/text()'))
        forum_url = hdoc.select('//div[@class="breadcrumbs"]/ul/li[@class="third"]/a/@href').extract()[0]
        if 'http' not in forum_url: forum_url = 'https://www.tripadvisor.in' + forum_url
        forum_title = hdoc.select('//div[@class="breadcrumbs"]/ul/li[@class="third"]/a/text()').extract()[0]
        forum_id = textify(re.findall(r'ShowForum-(\w+-\w+)-', forum_url))
        thread_id = textify(re.findall(r'ShowTopic-(\w+-\w+-\w+)-', response.url))

        nodes = hdoc.select('//div[@class="firstPostBox"] | //div[@onmouseover="mouseEnterPost(this)"]')

        for node in nodes:
            _id=textify(node.select('.//div[contains(@id,"pst_adm")]/@id'))
            dt = textify(node.select('.//div[@class="postDate"]/text()'))
            author_url = textify(node.select('.//div[@class="username"]/a/@href'))
            if author_url and 'http' not in author_url: author_url = 'https://www.tripadvisor.in' + author_url
            author_name = textify(node.select('.//div[@class="username"]/a/span/text()'))
            author_location = textify(node.select('.//div[@class="location"]//text()'))
            author_destexp = textify(node.select('.//div[@class="DE_Info"]//text()'))
            author_levelbadge = textify(node.select('.//div[contains(@class,"levelBadge")]/@class')).split('_')[-1]
            if author_levelbadge: author_levelbadge = int(author_levelbadge)
            author_posts = textify(node.select('.//div[@class="postBadge badge"]/span/text()'))
            author_reviews = textify(node.select('.//div[@class="reviewerBadge badge"]/span[@class="badgeText"]/text()'))
            text = textify(node.select('.//div[@class="postBody"]/p//text()'))
            sk = md5(_id)

            print '\n'
            print 'url',response.url + '#' + _id
            print 'title',xcode(title)
            print 'forum',{'title':xcode(forum_title),'url':forum_url,'id':forum_id}
            print 'thread',{'title':xcode(title),'url':response.url,'id':thread_id}
            print 'author',{'name':xcode(author_name),'url':author_url,'loc':xcode(author_location),'destinatin_expert':xcode(author_destexp),'level':author_levelbadge,'no_ofposts':author_posts,'reviews':author_reviews}
            print 'text',xcode(text)

        nxt_pg = hdoc.select('//div[@class="pgLinks"]/a[@class="paging taLnk"][last()]/@href').extract()
        if nxt_pg:
            nxt_pg = nxt_pg[0]
            yield Request(nxt_pg,self.parse_details,response)

        prev_pg = hdoc.select('//a[@class="guiArw sprite-pagePrev"]/@href').extract()
        if prev_pg:
            prev_pg = prev_pg[0]
            yield Request(prev_pg,self.parse_details,response)
