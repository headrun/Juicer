from juicer.utils import *

class ErjiSpider(JuicerSpider):
    name = 'erji_browse'
    allowed_domains = ['erji.net']
    start_urls = 'http://www.erji.net/'
    #start_urls = 'http://www.erji.net/thread.php?fid=135search=&page=53'

    def parse(self, response):
        hdoc = HTML(response)
        got_page(self.name, response)

        navigation_urls = hdoc.select_urls(['//tbody[contains(@id, "cate")]//tr//h2//a/@href'], response)

        for navigation_url in navigation_urls:
            get_page(self.name, navigation_url)

        last_page = textify(hdoc.select('//td[@valign="middle"]//div[@class="pages"]//a[last()]/@href'))
        if last_page:
            last = int(last_page.split('page=')[-1]) + 1
            foum_id = last_page.split('fid=')[-1].split('&')[0]

            for page in range(1, last):
                next_page = "http://www.erji.net/thread.php?fid=" + str(foum_id) + "search=&page=" + str(page)
                get_page(self.name, next_page)

        nodelist = hdoc.select('//tr[@class="tr3 t_one"]')
        for enode in nodelist:
            last_link = textify(enode.select('.//td//span//a[last()]/@href'))
            if last_link:
                replies = textify(enode.select('.//td[@class="tal f10 y-style"][1]/text()'))
                last_page = int(last_link.split('&page=')[-1].split('&')[0])
                last_page1 = last_page + 1

                fpage = last_link.split('fpage=')[-1]

                thread_id = last_link.split('tid=')[-1].split('&')[0]

                for p in range(2, last_page1):
                    if (p == last_page):
                        reply_url1 = "http://www.erji.net/read.php?tid=" + str(thread_id) + "&page=" + str(p) + "&fpage=" + str(fpage) + "&amp;replies=" + replies
                    else:
                        reply_url2 = "http://www.erji.net/read.php?tid=" + str(thread_id) + "&page=" + str(p) + "&fpage=" + str(fpage)
                        get_page('erji_terminal', reply_url2)

        terminal_urls = hdoc.select_urls(['//a[contains(@href, "/read.php?")][not(contains(@href, "page"))]/@href'], response)

        for terminal_url in terminal_urls:
            get_page('erji_terminal', terminal_url)
