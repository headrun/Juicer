from juicer.utils import *
from lxml import etree

class Temp(JuicerSpider):
    name = "mtime_test"
    start_urls = ['http://movie.mtime.com/99960/posters_and_images/']

    def parse(self, response):

        print "response>>>", response.url
        #data = ''.join(re.findall(r'var imageList = (.*\{"specialimages":\[\]\}\])</script><script type="text/javascript">', response.body.replace('\n', '').replace('\r',''))).strip()
        #data = ''.join(re.findall(r'var imageList = (.*)^</script><script type="text/javascript">', response.body.replace('\n', '').replace('\r',''))).strip()

        #out = file("/home/headrun/venu/mtime_data_final.json", 'w')

        #out.write("%s" %(data))

        #out.close()


