from juicer.utils import *
import feedparser

class Indiblogger_rss(JuicerSpider):
    name = 'indiblogger_rss_instance2'

    def start_requests(self):
        requests = []
        urls = file('/home/headrun/indiblogger/indiblogger_data_oct17', 'r').readlines()
        for i in urls[20000:]:
            data = eval(i)
            _url = data['blog']['url']
            try:
                r = Request(_url, self.parse, None, meta = {"data": data})
                requests.extend(r)
            except:
                try:
                    _url = 'http://'+_url
                    r = Request(_url, self.parse, None, meta = {"data": data})
                    requests.extend(r)
                except:pass


        return requests

    def parse(self, response):
        hdoc = HTML(response)

        urls_file = file('/home/headrun/indiblogger/urls_crawled2','ab+')

        try: urls_file.write('%s\n'%(response.url))
        except:
            fired_url = (response.url).encode('utf8').decode('ascii','ignore')
            urls_file.write('%s\n'%(response.url))
            pass
        urls_file.flush()
        urls_file.close()

        urls = hdoc.select_urls("//a/@href", response)
        head_urls = hdoc.select_urls('//link/@href', response)
        urls = urls + head_urls

        for url in urls:
            rss_url = url.lower()
            if 'rss' in rss_url or 'feeds' in rss_url or 'feed' in rss_url or 'xml' in rss_url or 'rdf' in rss_url or 'atom' in rss_url:

                try:
                    _entries = feedparser.parse(rss_url)
                    if len(_entries['entries']) > 1:
                        if '/feeds/posts/default?alt=rss' in rss_url:
                            rss_url = rss_url.replace('?alt=rss','').strip()

                        out_file = file('/home/headrun/indiblogger/indiblogger_final_data_oct17_instance2.csv', 'ab+')
                        data = response.meta['data']
                        try:
                            title = data['blog']['title']
                            out_file.write('%s\t' %(title))
                        except:out_file.write('\t')
                        try:
                            rank = data['blog']['num']['rank']
                            out_file.write('%d\t' %(rank))
                        except:out_file.write('\t')
                        try:
                            author = data['author']['name']
                            out_file.write('%s\t' %(author))
                        except:out_file.write('\t')
                        try:
                            auth_location = data['author']['location']
                            out_file.write('%s\t' %(auth_location))
                        except:out_file.write('\t')
                        out_file.write('%s\t' %(rss_url))
                        try:
                            tags = data['tags']
                            for i in tags:
                                out_file.write('%s\t' %(i))
                        except:
                            pass
                        out_file.write('\n')
                        out_file.close()

                except Exception as e:
                    print e
                    pass


