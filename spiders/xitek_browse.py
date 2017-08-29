from juicer.utils import *

class XitekSpider(JuicerSpider):
    name = 'xitek_browse'
    allowed_domains = ['xitek.com']
    start_urls = 'http://forum.xitek.com/forum.php'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//div[@class="module cl xl xl2"]//ul//li//a[contains(@href, "/forum-")][not(contains(@href, "forumdisplay-fid-"))]/@href',\
                                            '//a[@class="nxt"]/@href'], response)

        for navigation_url in navigation_urls:
            print "navigation_url>>>>>>>>>", navigation_url
            get_page(self.name, navigation_url)

        nodelist = hdoc.select('//tbody[contains(@id, "thread_")]')
        for xnode in nodelist:
            replies = textify(xnode.select('.//td[@class="num1 xi2"]/text()'))
            pg_num = int(replies)/30
            if pg_num > 0:
                page_number1 = pg_num + 1
                page_number = page_number1 + 1
            else:
                page_number1 = 1
                page_number = page_number1 + 1

            thread_id = textify(xnode.select('.//th//a[contains(@href, "forum.xitek.com/thread-")]/@href')).split('/thread-')[1].split('-')[0]

            for p in range(1, page_number):
                if (str(p) == str(page_number1)):
                    reply_url1 = "http://forum.xitek.com/" + "thread-" + str(thread_id) + "-" + str(p) + "-1-1.html" + "&amp;replies=" + replies
                else:
                    reply_url2 = "http://forum.xitek.com/" + "thread-" + str(thread_id) + "-" + str(p) + "-1-1.html"
                    get_page('xitek_terminal', reply_url2)


        terminal_urls = hdoc.select_urls(['//tbody[contains(@id, "thread_")]//th[@class="new"]//a[contains(@href, "/thread-")]/@href'], response)

        for terminal_url in terminal_urls:
            get_page('xitek_terminal', terminal_url)
