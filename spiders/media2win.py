from juicer.utils import *

class Media2win(JuicerSpider):
    name = "media2win"
    url = "http://socialbrands.media2win.com/ajax_response.php?page=%s&search_key=fans&term=&category1=&likes="
    start_urls = [url %(i) for i in range(1,37)]

    def parse(self, response):
        hdoc = HTML(response)

        try:
            nodes = hdoc.select('//td[@valign="top"]//a[@title="Brand History"]')
            out = file("/home/headrun/venu/facebook_pages/media2win_fb_pages", "ab+")
            for node in nodes:
                _id = textify(node.select('./@href'))
                _id = ''.join(re.findall(r'fb_id=(\d+)', _id))
                rss_url = "https://www.facebook.com/feeds/page.php?id=%s&format=rss20" %(_id)
                title = textify(node.select('./parent::div/following-sibling::div[1]/a//text()')).encode('utf8').decode('ascii', 'ignore')

                out.write("%s\t%s\n" %(title, rss_url))

            out.close()
        except Exception as e:
            print e.message
