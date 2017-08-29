from juicer.utils import *

class HexunBrowseSpider(JuicerSpider):
    name = 'hexun_browse'
    allowed_domains = ['hexun.com']
    start_urls = 'http://bbs.hexun.com/'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//a[contains(@href, "/board_")]/@href',\
                                            '//div[@class="botmod"]//div[@class="pagenum"]//a[@class="next"]/@href'], response)

        for navigation_url in navigation_urls:
            get_page(self.name, navigation_url)

        nodelist = hdoc.select('//tr[@class="bg"]')
        for hnode in nodelist:
            last_url = textify(hnode.select('.//span//a[@class="gray"][last()]/@href'))
            if last_url:
                replies = textify(hnode.select('.//td//span[@class="f1b6"]/text()'))

                thread_id1 = last_url.split('/post_')[-1].split('_')[0]
                thread_id2 = last_url.split('/post_')[-1].split('_')[1]
                main_thread = last_url.split('.com/')[-1].split('/')[0]

                pg_num = last_url.split('/post_')[-1].split('_')[2]
                pg_num = int(pg_num)
                page_number = pg_num + 1

                for p in range(2, page_number):
                    if (p == pg_num):
                        reply_url1 = "http://bbs.hexun.com/" + main_thread + "/post_" + str(thread_id1) + "_" + str(thread_id2) + "_" + str(p) + "_d.html" + "&amp;replies=" + replies
                    else:
                        reply_url2 = "http://bbs.hexun.com/" + main_thread + "/post_" + str(thread_id1) + "_" + str(thread_id2) + "_" + str(p) + "_d.html"
                        get_page('hexun_terminal', reply_url2)

        terminal_urls = hdoc.select_urls(['//tr[@class="bg"]//a[contains(@href, "/post_")][@class="f234"]/@href'], response)

        for terminal_url in terminal_urls:
            get_page('hexun_terminal', terminal_url)
