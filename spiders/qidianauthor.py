from juicer.utils import *

class QidianAuthro(JuicerSpider):
    name = "qidianauthor"
    #tart_urls = "http://me.qidian.com/authorIndex.aspx?id=2470130"
   
    def start_requests(self):
        requests = []
        conn = MySQLdb.connect(host='127.0.0.1', user='root', db='qidian', passwd='root')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        sql = "SELECT category, author_id FROM author_urls WHERE author_id = 2473746"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                category = row[0]
                a_id = row[1]

                url = 'http://me.qidian.com/authorIndex.aspx?id=%s' %(a_id)
                upt = "UPDATE author_urls SET is_crawled = 2 WHERE author_id = '%s'" %(a_id)
                cursor.execute(upt)
                r = Request(url, self.parse, None, meta={'_id': a_id, 'category' : category})
                requests.extend(r)
        except:
            pass
        cursor.close()
        return requests

    def parse(self, response):

        hdoc = HTML(response)
        error_message = "".join(textify(hdoc.select('//div[@class="nb-words"]/strong/text()'))).encode('UTF-8')
        if not error_message:
            author_id = "".join(re.findall(r'id=(\d+)',response.url))
            author_name = "".join(textify(hdoc.select('//div[@class="sp-user-info"]//dl[@class="sui-list"]/dt/a/text()'))).encode('UTF-8')
            print "author_name", author_name.strip(), "end>>"
            import pdb; pdb.set_trace()
            avatar_img = "".join(textify(hdoc.select('//div[@class="sp-user-info"]/div[@class="big-photo"]/a/img/@src'))).encode('UTF-8')
            if '.gif' in avatar_img:
                avatar_image = urlparse.urljoin(response.url, avatar_img)
                print avatar_image
            else:
                avatar_image = avatar_img
                print avatar_image
            author_url = response.url

            genders = "<>".join(textify(hdoc.select('//div[@class="sp-user-info"]//dl[@class="sui-list"]//dd[2]/text()')))
            gen = genders.split('<>')
            gender = gen[0].encode('UTF-8')
            print gender
            book_id = ''
            bk = []
            book = hdoc.select('//div[@class="sp-user-info"]//dl[@class="sui-list"]//dd[3]/a[contains(@floatbook,"true")]/@href')
            for i in book:
                bk = bk + [xcode(textify(i))]
                book_id = "".join(re.findall(r'(\d+)', textify(i)))
                print "book_id",book_id
            books = bk

            cncs = "".join(textify(hdoc.select('//div[@class="profile_update"]//li[@id="linkFollowing"]/a/@href')))
            print "cncs>>>", cncs
            fans = "".join(textify(hdoc.select('//div[@class="profile_update"]//li[@id="linkFollower"]/a/@href')))
            print "fans>>", fans
            badges = "".join(textify(hdoc.select('//div[@class="profile_update"]//li[@id="linkAwards"]/a/@href')))
            print "badges>>", badges
            yield Request(cncs,self.parse_concern, response, meta = { 'fans' : fans, 'badges' :badges, 'gender' : gender, 'author_id' : author_id, 
                                                                  'author_name' : author_name, 'avatar_image' : avatar_image, 
                                                                  'author_url' : author_url, 'books' : books, 'book_id' : book_id,
                                                                  'category' : response.meta['category']})
        else:
            print "error message: ",error_message

    def parse_concern(self, response):
        hdoc = HTML(response)

        concern = re.findall(r'(\d+)',textify(hdoc.select('//div[@class="ta-friends"]//h3/text()')))
        conc = []
        for con in concern:
            if con != '00':
                concs = con.encode('UTF-8')
                if concs:
                    conc.append(concs)
        if len(conc) == '2':
            print "conc_list", conc
            concerns = conc[1]
        else:
            concerns = conc[0]
        print "concerns>>",concerns
        fans_url = urlparse.urljoin(response.url, response.meta['fans'])
        yield Request(fans_url, self.parse_fans, response, meta = { 'badges' : response.meta['badges'], 'concern' : concerns, 
                                                                    'fans' : response.meta['fans'], 'gender' : response.meta['gender'], 
                                                                    'author_id' : response.meta['author_id'], 
                                                                    'author_name' : response.meta['author_name'],
                                                                    'avatar_image' : response.meta['avatar_image'], 
                                                                    'author_url' : response.meta['author_url'], 'books' : response.meta['books'],
                                                                    'book_id' : response.meta['book_id'], 'category' : response.meta['category']})

    def parse_fans(self, response):
        hdoc = HTML(response)

        fan = re.findall(r'(\d+)',textify(hdoc.select('//div[@class="ta-friends"]//h3/text()')))
        print "fan_text", fan
        fan_list = []
        for fa in fan:
            if fa != '00':
                fans = fa.encode('UTF-8')
                print "fans>>>", fans
                if fans:
                    fan_list.append(fans)
        print "fans_list", fan
        fans = fan_list[0]
        print  "fans>>", fans
        badges_url = urlparse.urljoin(response.url, response.meta['badges'])
        yield Request(badges_url, self.parse_badges, response, meta = { 'fans' : fans, 'badges' : response.meta['badges'], 
                                                                        'concern' : response.meta['concern'],
                                                                        'gender' : response.meta['gender'],'author_id' : response.meta['author_id'],
                                                                        'author_name' : response.meta['author_name'], 
                                                                        'avatar_image' : response.meta['avatar_image'],
                                                                        'author_url' : response.meta['author_url'], 'books' : response.meta['books'],
                                                                        'book_id' : response.meta['book_id'], 'category' : response.meta['category']}) 

    def parse_badges(self, response):
        hdoc = HTML(response)

        badges = "".join(textify(hdoc.select('//div[@class="about"]//li[1]/i/text()'))).encode('UTF-8')
        print "badges>>", badges
        books =  "<>".join(response.meta['books'])
        created_at = datetime.datetime.now()
        date = str(created_at)
        mod_at = datetime.datetime.now()
        modified_at = str(mod_at)

        value = [response.meta['author_id'],response.meta['author_name'],response.meta['avatar_image'],response.meta['author_url'],
                response.meta['gender'],response.meta['fans'],response.meta['concern'],books,badges,date,modified_at]
        values = "#<><>#".join(value)

        othr_books = ['',response.meta['book_id'],response.meta['author_id'],'juicer_crawler',books,response.meta['author_url'],
                      '','0','1',response.meta['category'],date,modified_at]
        other_books = "#<><>#".join(othr_books)

        out_file = file('/home/headrun/venu/qidian/author','ab+')
        out_file.write('%s\n' %(values))
        out_file.close()

        out_file = file('/home/headrun/venu/qidian/other_books','ab+')
        out_file.write('%s\n' %(other_books))
        out_file.close()

        out_file = file('/home/headrun/venu/qidian/is_crawled','ab+')
        out_file.write('%s\n' %(response.meta['author_id']))
        out_file.close()

        meta = { 'fans' : response.meta['fans'], 'concern' : response.meta['concern'], 'gender' : response.meta['gender'],
                 'author_id' : response.meta['author_id'],
                 'author_name' : response.meta['author_name'], 'avatar_image' : response.meta['avatar_image'], 
                 'author_url' : response.meta['author_url'], 
                 'books' : response.meta['books'], 'book_id' : response.meta['book_id'], 'category' : response.meta['category']}
