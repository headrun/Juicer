from juicer.utils import *

class BloomBerg(JuicerSpider):
    name = "bloomberg"
    allowed_domains = ["www.bloomberg.com"]
    start_urls = ["http://www.bloomberg.com/"]

    def parse(self, response):
        hdoc = HTML(response)
        if self.latest_dt is None:
            self.latest_dt = self._latest_dt
        category_urls = hdoc.select_urls(['//div[@class="container"]/ul[@class="top_level"]//li//a/@href'], response)
        for category_url in category_urls:
            yield Request(category_url, self.parse_category, response)

    def parse_category(self, response):
        hdoc = HTML(response)
        import pdb;pdb.set_trace()
        terminal_urls = hdoc.select_urls(['//div[@id="primary_content"]//a[contains(@class,"q")]/@href'], response)
        for terminal_url in terminal_urls:
            yield Request(terminal_url, self.parse_terminal, response)

    def parse_terminal(self, response):
        hdoc = HTML(response)
        item = Item(response)

        posted_dt = xcode(textify(hdoc.select('//div[@class="entry_wrap"]//span/@epoch')))
        if posted_dt:
            posted_dt = get_datetime(float(re.findall(r'(\d+)\w\w\w',posted_dt)[0]))
        if posted_dt and posted_dt >= self.latest_dt:
            if self.flag:
                self.update_dt(posted_dt)
            import pdb;pdb.set_trace()
            title = textify(hdoc.select('//h1[contains(@class,"article_title")]//text()')).replace("&amp;","&").encode('UTF-8')
            author = textify(hdoc.select('//div[@class="entry_wrap"]//span[@class="author"]'))
            author = "".join(re.findall(r'By\s(.*)', author))

            text = textify(hdoc.select('//div[@class="entry_content"]/div[@class="article_body"]//p//text()')).replace("\n"," ").encode('UTF-8')

        print '/n'
        print 'title',xcode(title)
        print 'text',xcode(text)
        print 'posted_dt',xcode(posted_dt)
        print 'author',xcode(author)
