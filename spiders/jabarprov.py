from juicer.utils import *
from dateutil import parser

class Jabarprov(JuicerSpider):
    name = 'jabarprov_id'
    start_urls = ['http://jabarprov.go.id/index.php/berita/berita_kategori/0/1', 'http://jabarprov.go.id/index.php/berita/berita_kategori/0/2', 'http://jabarprov.go.id/index.php/berita/berita_kategori/0/3', 'http://jabarprov.go.id/index.php/berita/berita_kategori/0/4']
    months = {'Januari':'January', 'Februari':'February',' Maret':'March', 'April':'April',\
    'Mei':'May', 'Juni':'June', 'Juli':'July', 'Agustus':'August', 'September':'September',\
    'Oktober':'October', 'Nopember':'November', 'Desember':'December'}

    def parse(self, response):
        hdoc = HTML(response)
        is_next = True
        threads = hdoc.select('//div[@class="grve-post-content"]')
        for thread in threads:
            date = textify(thread.select('.//span[@class="grve-post-date"]/text()'))
            for key, value in self.months.iteritems():
                if key in date:
                    date = date.replace(key,value)
            date_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
            if date_added < get_current_timestamp()-86400*30:
                is_next = False
                continue
            newslink = textify(thread.select('.//h3/a/@href'))
            yield Request(newslink, self.details, response)

        nxt_pg = textify(hdoc.select('//li/a[contains(text(),">")]/@href')[0])
        if nxt_pg and is_next:
            yield Request(nxt_pg, self.parse, response)

    def details(self, response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//div[@class="grve-main-content"]//h1/text()'))
        date = textify(hdoc.select('//div[@class="grve-main-content"]//span[@class="grve-post-date"]/text()')).strip(' |')
        dt_added = get_timestamp(parse_date(xcode(date))-datetime.timedelta(hours=9))
        text = textify(hdoc.select('//div[@class="grve-post-content"]/p//text()'))

        item = Item(response)
        item.set('url',response.url)
        item.set('title', xcode(title))
        item.set('dt_added', dt_added)
        item.set('text', xcode(text))
