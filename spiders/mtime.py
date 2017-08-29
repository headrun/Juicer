import MySQLdb
from juicer.utils import *
import logging
log = logging.getLogger()

class Mtime(JuicerSpider):
    name = 'mtime'

    def start_requests(self):
        requests = []
        conn = MySQLdb.connect('localhost','root','root','MTIME')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        print "Came here 01"
        sql = "SELECT movie_id, movie_url FROM movie_urls WHERE is_crawled = 2"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                _id = row[0]
                url = row[1]
                try:
                    upt = "UPDATE movie_urls SET is_crawled = 2 WHERE movie_id = %s" % (_id)
                    cursor.execute(upt)
                except:
                    log.info("Unable to update-1 id %s" %_id)
                r = Request(url, self.parse, None, meta={'_id': _id})
                requests.extend(r)

        except:
            log.info("Error: unable to fecth data")


        return requests

    def parse(self, response):
        hdoc = HTML(response)
        crew_list = []

        rank = 0
        movie_id = ''.join(re.findall(r'mtime.com/(\d+)/', response.url))

        actors = hdoc.select('//h3[@id="Actor"]//following-sibling::ul[1]//li')
        for actor in actors:
            rank = rank+1
            crew_info = textify(actor.select('./a[1]/@href'))
            crew_id = ''
            if crew_info:
                crew_id = crew_info.split('/')[-2]
            crew_role = 'actor'
            role_text = textify(actor.select('./em/text()')).replace('.','').strip()
            crew_list.append((movie_id, crew_id, rank, crew_role, role_text))

        directors = hdoc.select('//h3[@id="Director"]//following-sibling::ul[1]//a[1]')
        for direct in directors:
            rank = rank + 1
            dir_info = textify(direct.select('./@href'))
            dir_id, role_text = '',''
            if dir_info:
                dir_id = dir_info.split('/')[-2]
            dir_role = 'director'
            crew_list.append((movie_id, dir_id, rank, dir_role, role_text))

        screen_play_writers = hdoc.select('//h3[@id="Writer"]//following-sibling::ul[1]//a[1]')
        for wri in screen_play_writers:
            rank = rank + 1
            wri_info = textify(wri.select('./@href'))
            wri_id, role_text = '', ''
            if wri_info:
                wri_id = wri_info.split('/')[-2]
            crew_list.append((movie_id, wri_id, rank, 'writer', role_text))

        producers = hdoc.select('//h3[@id="Produced by"]//following-sibling::ul[1]//a[1]')
        for pro in producers:
            rank = rank + 1
            pro_info = textify(pro.select('./@href'))
            pro_id, role_text = '', ''
            if pro_info:
                pro_id = pro_info.split('/')[-2]
            crew_list.append((movie_id, pro_id, rank, 'producer', role_text))

        cinematographers = hdoc.select ('//h3[@id="Cinematography"]//following-sibling::ul[1]//a[1]')
        for cin in cinematographers:
            rank = rank + 1
            cin_info = textify(cin.select('./@href'))
            cin_id, role_text = '',''
            if cin_info:
                cin_id = cin_info.split('/')[-2]
            role_text = textify(cin.select('./em/text()')).replace('.','').strip()
            crew_list.append((movie_id, cin_id, rank, 'cinematographer', role_text))

        assistant_directors = hdoc.select('//h3[@id="Assistant Director"]//following-sibling::ul[1]//a[1]')
        for as_dir in assistant_directors:
            rank = rank + 1
            as_dir_info = textify(as_dir.select('./@href'))
            as_dir_id, role_text = '', ''
            if as_dir_info:
                as_dir_id = as_dir_info.split('/')[-2]
            crew_list.append((movie_id, as_dir_id, rank, 'assistant director', role_text))

        music_directors = hdoc.select('//h3[@id="Original Music"]//following-sibling::ul[1]//a[1]')
        for mus_dir in music_directors:
            rank = rank + 1
            mus_dir_info = textify(mus_dir.select('./@href'))
            mus_dir_id, role_text = '',''
            if mus_dir_info:
                mus_dir_id = mus_dir_info.split('/')[-2]
            crew_list.append((movie_id, mus_dir_id, rank, 'music director', role_text))


        editors = hdoc.select('//h3[@id="Film Editing"]//following-sibling::ul[1]//a[1]')
        for editor in editors:
            rank = rank + 1
            editor_info = textify(editor.select('./@href'))
            editor_id, role_text = '',''
            if editor_info:
                editor_id = editor_info.split('/')[-2]
            crew_list.append((movie_id, editor_id, rank, 'editor', role_text))

        designers = hdoc.select('//h3[@id="Production Designer"]//following-sibling::ul[1]//a[1]')
        for des in designers:
            rank = rank + 1
            des_info = textify(des.select('./@href'))
            des_id, role_text = '',''
            if des_info:
                des_id = des_info.split('/')[-2]
            crew_list.append((movie_id, des_id, rank, 'production designer', role_text))

        art_directors = hdoc.select('//h3[@id="Art Direction by"]//following-sibling::ul[1]//a[1]')
        for art in art_directors:
            rank = rank + 1
            art_info = textify(art.select('./@href'))
            art_id,role_text = '',''
            if art_info:
                art_id = art_info.split('/')[-2]
            crew_list.append((movie_id, art_id, rank, 'art director', role_text))

        ve_supervisors = hdoc.select('//h3[@id="Visual Effects Supervisor"]//following-sibling::ul[1]//a[1]')
        for ve in ve_supervisors:
            rank = rank + 1
            ve_info = textify(ve.select('./@href'))
            ve_id, role_text = '',''
            if ve_info:
                ve_id = ve_info.split('/')[-2]
            crew_list.append((movie_id, ve_id, rank, 'visual effects supervisor', role_text))

        costume_designers = hdoc.select('//h3[@id="Costume Design by"]//following-sibling::ul[1]//a[1]')
        for cos in costume_designers:
            rank = rank + 1
            cos_info = textify(cos.select('./@href'))
            cos_id, role_text = '',''
            if cos_info:
                cos_id = cos_info.split('/')[-2]
            crew_list.append((movie_id, cos_id, rank, 'costume designer', role_text))

        set_decorators = hdoc.select('//h3[@id="Set Decoration by"]//following-sibling::ul[1]//a[1]')
        for set_de in set_decorators:
            rank = rank + 1
            set_info = textify(set_de.select('./@href'))
            set_id, role_text = '',''
            if set_info:
                set_id = set_info.split('/')[-2]
            crew_list.append((movie_id, set_id, rank, 'set decorator', role_text))

        update(movie_id)

        for crew in crew_list:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', db='MTIME', passwd='root')
            conn.set_character_set('utf8')
            upt_cursor = conn.cursor()
            upt_cursor.execute('SET NAMES utf8;')
            upt_cursor.execute('SET CHARACTER SET utf8;')
            upt_cursor.execute('SET character_set_connection=utf8;')
            _id, crew_id1, rank, role, role_text = crew
            query = "insert into crew_urls(movie_id, crew_id, role, rank, role_text, created_at, modified_at) values(%s,%s,%s,%s,%s, now(), now()) on duplicate key update modified_at=now()"
            values = (movie_id.strip(), crew_id1.strip(), role, rank, role_text)
            upt_cursor.execute(query, values)


def update(_id):
    upt = "UPDATE movie_urls SET is_crawled = 3, modified_at = now() WHERE movie_id = %s"
    upt_value = (_id)
    is_crawled_file = file("/home/headrun/venu/crew_is_crawled_details", "ab+")
    is_crawled_file.write('%s\n%s\n' %(upt, repr(upt_value)))
    is_crawled_file.close()

def init_logger():
    log = logging.getLogger('/home/headrun/venu/crew_urls.log')
    hdlr = logging.FileHandler('/home/headrun/venu/crew_urls.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)

    return log

log = init_logger()


