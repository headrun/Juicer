from juicer.utils import *
import MySQLdb
import requests

class Bseindia(JuicerSpider):
    name = 'bseindia_1'
    start_urls = ['http://www.bseindia.com/corporates/ann.aspx?curpg=1&annflag=1&dt=&dur=D&dtto=&cat=&scrip=&anntype=A']

    def parse(self, response):
        hdoc = HTML(response)

        out_file = file('/home/headrun/venu/bse_india','ab+')
        out_file.write('%s\n' %(time.ctime()))
        out_file.close()
        base = hdoc.select('//span[@id="ctl00_ContentPlaceHolder1_lblann"]/table')
        posts = base.select('./tr/td[@class="TTHeadergrey"]/parent::tr')
        for post in posts:
            title = textify(post.select('./td[@class="TTHeadergrey"][1]//text()'))
            _type = textify(post.select('./td[@class="TTHeadergrey"][2]//text()'))
            pdf_link = textify(post.select('./td[@class="TTHeadergrey"][3]/a/@href'))
            post_dt = textify(post.select('./td[@class="TTHeadergrey"][4]/text()'))
            post_dt = parse_date(post_dt)
            text = textify(post.select('./following-sibling::tr[1]/td[@class="TTRow_leftnotices"]//text()'))
            url = textify(post.select('./following-sibling::tr[2]/td[@class="TTRow_leftnotices"]/a/@href'))
            if url:
                url = urlparse.urljoin(response.url,url)
                data = requests.get(url).text
                try:
                    data = data.split('TTRow_leftnotices')[1]
                    text = ''.join(re.findall(r'colspan =\'3\'>(.*)</td></tr></table></td></tr></table></td>', data))
                except:
                    pass

            a=b=c=d=e=f=''
            if 'open offer' in title.lower() or 'buyback' in title.lower():a=True
            elif 'scheme of arrangement' in title.lower() or 'preferential offer' in title.lower():b=True
            elif 'merger' in title.lower() or 'demerger' in title.lower() or 'restructuring' in title.lower():c=True
            elif 'open offer' in text.lower() or 'buyback' in text.lower():d=True
            elif 'scheme of arrangement' in text.lower() or 'preferential offer' in text.lower():e=True
            elif 'merger' in text.lower() or 'demerger' in text.lower() or 'restructuring' in text.lower():f=True

            #if a or b or c or d or e or f:
            if True:
                doc = {}
                doc['title'] = title
                doc['type']= _type
                if pdf_link: doc['pdf_link'] = pdf_link
                doc['text'] = text
                doc['dt_added'] = post_dt
                title_hash = hashlib.md5(title+text).hexdigest()
                doc['title_hash'] = title_hash
                '''
                db,db_name = get_cursor()
                data = db.find_one('bseindia', "news", spec={'title_hash':title_hash})
                if data['result'] is None:
                    db.update('bseindia', "news", spec={'title_hash': title_hash}, doc=doc, upsert=True)
                '''

                conn = MySQLdb.connect(host='interns.headrun.com', user='headrun', db='stock_info', passwd='headrun')
                conn = MySQLdb.connect(host='localhost', user='root', db='SAP_CACHE', passwd='root')
                cursor = conn.cursor()
                query = "insert into stocks1(title,contents,type,pdf_link,dt_added,created_at,modified_at) values(%s,%s,%s, %s, %s, now(), now()) on duplicate key update modified_at=now()"
                values = (str(title),str(text),str(_type), str(pdf_link),str(post_dt))
                cursor.execute(query,values)
                cursor.close()

