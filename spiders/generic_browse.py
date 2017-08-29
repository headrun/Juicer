import hashlib
import urlparse
from juicer.utils import *

class SpiderLogic:
    def __init__(self, start_url):
        conn = MySQLdb.connect(host=settings['DB_HOST'],
                               db=settings['DB_NAME'],
                               user=settings['DB_USER'],
                               passwd=settings['DB_PASS'])

        cursor = conn.cursor()

        query = 'SELECT terminal_regexes, browse_regexes, is_whitelist, sk_regexes FROM generic_browse WHERE start_url=%s'
        cursor.execute(query, (start_url,))

        records = cursor.fetchall()
        if not records:
            raise Exception('settings not found for start_url=%s' % start_url)

        terminal_regexes, browse_regexes, is_whitelist, sk_regexes = records[0]
        self.terminal_regexes = eval(terminal_regexes)
        self.browse_regexes = eval(browse_regexes) if browse_regexes else ['.*']
        self.is_whitelist = bool(is_whitelist)
        self.sk_regexes = eval(sk_regexes) if sk_regexes else None

    def _matches(self, url, regexes):
        regexes = regexes or []

        for r in regexes:
            if re.findall(r, url):
                return True

        return False

    def is_terminal(self, url):
        return self._matches(url, self.terminal_regexes)

    def can_open(self, url):
        matches = self._matches(url, self.browse_regexes)
        return not matches ^ self.is_whitelist

    def get_sk(self, url):
        if self.sk_regexes:
            for r in self.sk_regexes:
                sk = re.findall(r, url)
                if sk:
                    return sk[0]

        return hashlib.md5(url).hexdigest()

def gen_start_urls(spider):
    LARGE_LIMIT = 1000 * 1000 * 1000
    items = lookup_items('generic_browse',
                         '%s:got_page:False' % spider.start_url,
                         limit=LARGE_LIMIT)
    if not items:
        items = [(None, None, spider.start_url)]
        empty_index('generic_browse', '%s:got_page:True' % spider.start_url)

    for _id, term, data in items:
        yield data

class Spider(JuicerSpider):
    name = 'generic_browse'
    run_type = 'full'

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_url = self.schedule_name.rsplit(':', 1)[0] \
            if self.schedule_name.endswith(':recent') else self.schedule_name

        if self.run_type == 'recent':
            #settings.overrides['DEPTH_LIMIT'] = 2
            self.start_urls = [self.start_url]
        else:
            #settings.overrides['DEPTH_LIMIT'] = 50
            self.start_urls = gen_start_urls(self)

        self.allowed_domains = [urlparse.urlparse(self.start_url)[1]]

        self.logic = SpiderLogic(self.start_url)

    def _handle_persistance(self, response, links):
        item = Item(response, HTML)
        url = get_request_url(response)
        item.set('sk', '%s>%s' % (self.start_url, hashlib.md5(url).hexdigest()))
        item.set('url', url)
        item.set('start_url', self.start_url)
        item.set('got_page', True)
        item.update_mode = 'custom'
        yield item.process()

        for link in links:
            item = Item(response, HTML)
            item.set('sk', '%s>%s' %(self.start_url, hashlib.md5(link).hexdigest()))
            item.set('url', link)
            item.set('start_url', self.start_url)
            item.update_mode = 'custom'
            yield item.process()

    def parse(self, response):
        hdoc = HTML(response)
        links = [urlparse.urljoin(response.url, textify(x)) for x in hdoc.select('//a/@href')]
        links = [x for x in links if self.logic.can_open(x)]
        links = [x.split('#')[0] for x in links]
        yield Request(links, self.parse, response)

        if self.run_type != 'recent':
            for x in self._handle_persistance(response, links):
                yield x

        terminal_links = [x for x in links if self.logic.is_terminal(x)]
        terminal_links = [x.split('#')[0] for x in terminal_links]
        for tlink in terminal_links:
            item = Item(response, HTML)
            item.set('sk', '%s>%s' % (self.start_url, self.logic.get_sk(tlink)))
            item.set('start_url', self.start_url)
            item.set('from_urls', [get_request_url(response)])
            item.set('url', tlink)
            item.spider = 'generic_terminal'
            yield item.process()

    @staticmethod
    def _update_item(new_data, old_data):
        data = {}
        data.update(old_data)
        data.update(new_data)
        return data

    @staticmethod
    def _index_item(item):
        got_page = item.get('got_page', False)
        return [('%s:got_page:%s' % (item['start_url'], got_page), item['url'])]
