from juicer.utils import *

def _get_urls():

    urls = []
    for i in range(210, 3150, 30):
        _date = datetime.datetime.utcnow().date() - datetime.timedelta(days=i)
        url = "http://botd.wordpress.com" + _date.strftime("/%Y/%m/")
        urls.append(url)

    urls = list(set(urls))
    return urls

class Botd_Browse(JuicerSpider):
    name = "botd_browse"
    start_urls = _get_urls()

    def parse(self, response):
        hdoc = HTML(response)

        blog_urls = []

        try:
            top_blogs_url = textify(hdoc.select('//div[@class="threequarters"]/ul//a[contains(text(), "Top Blogs")]/@href')[0])
            growing_blogs_url = textify(hdoc.select('//div[@class="threequarters"]/ul//a[contains(text(), "Growing Blogs")]/@href')[0])
            top_post_blogs_url = textify(hdoc.select('//div[@class="threequarters"]/ul//a[contains(text(), "Top Posts")]/@href')[0])

            top_blogs = make_blogs(top_blogs_url)
            growing_blogs = make_blogs(growing_blogs_url)
            top_post_blogs = make_blogs(top_post_blogs_url)

            blog_urls = top_blogs + growing_blogs + top_post_blogs

        except Exception as e:
            print e.message

        for blog_url in blog_urls:
            get_page("botd_browse_urls", blog_url)

def make_blogs(url):

    urls = []
    data_set = []

    y, m, d, _id = re.findall(r'\d+', url)
    d, _id = int(d), int(_id)

    for i in range(1, d):
        data_set.append((i, _id - (d-i)))

    for i in range(d, 32):
        data_set.append((i, _id - (d-i)))

    if "top-blogs" in url:
        _type = "top-blogs-"
    elif "growing-blogs" in url:
        _type = "growing-blogs-"
    else: _type = "top-posts-"

    for i in data_set:
        url = "http://botd.wordpress.com/" + y + "/" + m + "/" + str(i[0]) + "/" + _type + str(i[1]) + "/"
        urls.append(url)

    return urls
