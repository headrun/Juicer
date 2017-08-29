from juicer.utils import *

class FengniaoSpider(JuicerSpider):
    name = 'fengniao_browse'
    allowed_domains = ['fengniao.com']
    start_urls = 'http://bbs.fengniao.com/forum/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        top_urls = hdoc.select_urls(['//td[@class="alt1Active"]//a/@href',\
                                     '//td[@class="smallfont"]//a[@class="smallfont"][contains(text(), ">")]/@href'], response)

        for top_url in top_urls:
            get_page(self.name, top_url)

        nodelist = hdoc.select('//table[@id="threadslist"]//tr')
        for knode in nodelist:
            reply_last = textify(knode.select('.//td[@class="alt2"]//a[contains(@href, "_")][last()]/@href'))
            last_page = reply_last.split('_')[-1].split('.html')[0]
            if last_page:
                last_page = int(last_page)
                last_page1 = last_page + 1
                thread_id = reply_last.split('_')[0]
                replies = textify(knode.select('.//td[@class="alt1"][@align="center"][last()]/text()'))

                for p in range(2, last_page1):
                    if (int(p) == int(last_page)):
                        replies_url1 = "http://bbs.fengniao.com/forum/" + str(thread_id) + "_" + str(p) + ".html&amp;replies=" + replies
                        get_page('fengniao_terminal', replies_url1)
                    else:
                        replies_url2 = "http://bbs.fengniao.com/forum/" + str(thread_id) + "_" + str(p) + ".html"
                        get_page('fengniao_terminal', replies_url2)

        terminal_urls = hdoc.select_urls(['//td[@class="alt2"]//div//a[contains(@id, "thread_title_")]/@href'], response)

        for terminal_url in terminal_urls:
            get_page('fengniao_terminal', terminal_url)
