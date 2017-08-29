from juicer.utils import *

class Linkedin(JuicerSpider):
    name = "linkedin_com"
    global get_urls
    global letter

    def __init__(self, *args, **kwargs):
        JuicerSpider.__init__(self, *args, **kwargs)
        self.let = kwargs.get("url")
        if kwargs.get("DIRECTORY"):
            url = "http://www.linkedin.com/directory/people/"+ str(kwargs.get("DIRECTORY")) + ".html"

    def get_urls():
        url = "http://www.linkedin.com/directory/people/" + letter + ".html"
        return url

    start_urls = "http://www.linkedin.com/directory/people/i.html" 


    def parse(self, response):
        hdoc = HTML(response)
        file_name = self.let + "_urls"
        urls_dump = file(file_name, "ab+")

        urls = hdoc.select_urls(['//div[@class="wrapper"]//ul[@class="directory"]//li/a/@href'], response)

        for url in urls :
            if "directory" in url :
                yield Request(url, self.parse, response)
            else :
                try:
                    urls_dump.write("%s\n"%(xcode(url)))
                except Exception:
                    import pdb;pdb.set_trace()
                print url 

