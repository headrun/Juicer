from juicer.utils import *

class Indiblogger_in(JuicerSpider):
    name = "indiblogger"
    start_urls = "http://www.indiblogger.in/tagsearch.php?tag=fashion"

    def parse(self, response):
        hdoc = HTML(response)
        url = response.url
        blog_title = textify(hdoc.select('//div[@id="maincontent"]/h1/text()')).encode('UTF-8')
        nextpage_url = ""
        tag = []
        rows = hdoc.select('//ul/li[@class="listing"]')
        for row in rows:
            item = Item(response)
            _url = {}
            nextpage_url = hdoc.select('//div[@class="pagerbarT"]/a/@href')

            author_name = textify(row.select('./a[contains(@title,"IndiBlogger profile")]\
                                              //text()')).encode('UTF-8')
            author_location = textify(row.select('./a[contains(@title, "Blogs in")]\
                                                 //text()')).encode('UTF-8')
            a_url = textify(row.select('./a[contains(@title,"IndiBlogger profile")]/@href'))
            author_url = urlparse.urljoin(response.url, a_url)
            author_id = "".join(re.findall(r'/blogger/(\d+)/', author_url))

            tag = row.select('./div[@class="tags"]/a')
            tags = [xcode(textify(i).replace("&amp;","")) for i in tag]
            tags = [j.strip() for j in tags if j]

            rank = textify(row.select('./div[contains(@class,"rank rounded")]//text()'))
            if rank:
                rank = int(rank)
            blog_url = textify(row.select('./h4/a/@href'))
            blog_subtitle = textify(row.select('./h4/a/text()')).encode('UTF-8')

            item.set('author.name', xcode(author_name.decode('ascii', 'ignore'))) if author_name else ""
            item.set('author.location', xcode(author_location.decode('ascii', 'ignore'))) if author_location else""
            item.set('author.url', xcode(author_url)) if author_url else ""
            item.set('author.id', xcode(author_id))
            item.set('tags', tags) if tags else ""
            item.set('author.num.rank', xcode(rank)) if rank else ""
            item.set('title', xcode(blog_title.decode('ascii','ignore').replace("&amp;", "&")))
            item.set('url', xcode(url))
            item.set('blog.url', xcode(blog_url))
            item.set('blog.title', xcode(blog_subtitle.decode('ascii','ignore').replace("&amp;", "&")))
            item.set('rss_urls',[])
            #ob = pprint.PrettyPrinter(indent=2)
            #ob.pprint(item.data)
            my_file = file("/home/headrun/niranjan/indiblogger_text","ab+")
            _url[blog_url] = item.data
            my_file.write("%s\n" % _url)
            my_file.close()
        if nextpage_url:
            yield Request(nextpage_url, self.parse, response)
