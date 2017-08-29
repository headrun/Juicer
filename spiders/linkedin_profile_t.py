import MySQLdb
from unicodedata import normalize
from juicer.utils import *
import logging
log = logging.getLogger()

class Linkedin_Profile(JuicerSpider):
    name = 'linkedin_profile_t_old'
    settings.overrides['USER_AGENT_LIST'] = ['Mozilla/5.0 (compatible; Veveobot; +http://corporate.veveo.net/contact/)']
    global modify, varchar, category
    category = ''.join(re.findall(r'_profile_(\w)_old', name))

    def start_requests(self):
        requests = []
        conn = MySQLdb.connect('localhost','root','root','LINKEDIN')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        print "Came here 01"
        sql = "SELECT pub_id, profile_url FROM linkedin_urls WHERE category= '%s' AND is_crawled = 0 limit 50000" %(category)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                _id = row[0]
                url = row[1]
                try:
                    upt = "UPDATE linkedin_urls SET is_crawled = 2 WHERE pub_id = %s" % (_id)
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

        base = hdoc.select('//div[@id="content"]')
        first_name = modify(textify(base.select('.//span[@class="given-name"]//text()')))
        last_name = modify(textify(base.select('.//span[@class="family-name"]//text()')))
        location = modify(textify(base.select('.//div[@class="profile-header"]//\
                                                            span[@class="locality"]//text()')))
        connections = xcode(textify(base.select('.//dd[@class="overview-connections"]//p\
                                                                              /strong/text()')))
        recommendations = xcode(textify(base.select('.//dt[contains(text(),"Recommendations")]\
                                           /following-sibling::dd[1]/p/strong/text()')).strip())
        industry = modify(textify(base.select('.//div[@class="profile-header"]//\
                                                              dd[@class="industry"]//text()')))

        summary = base.select('.//p[@class=" description summary"]/text()')
        summary = [(textify(matter)).replace('-','').replace('* ','.') for matter in summary if matter]
        summary = re.sub(r' +', ' ', '<>'.join([modify(older) for older in summary if older])).strip()

        specialities = base.select('.//div[@id="profile-specialties"]/p[@class="null"]/text()')
        specialities = re.sub(r' +',' ', '<>'.join([modify(textify(i)) for i in specialities if i])).strip()

        current_position, position = [],''
        current_pos = base.select('.//dl[@id="overview"]//ul[@class="current"]//li')
        for cur in current_pos:
            position = ''.join(re.findall(r'(.*) at ', textify(cur.select('.//text()'))))
            if not position:
                position = ''.join(textify(cur.select('.//text()'))).strip()
            if position:
                current_position.append(modify(position.replace('--','')))
        if position == '':
            position = textify(base.select('.//p[@class="headline-title title"]//text()'))
            position = ''.join(re.findall(r'(.*) at ', position))
            if not position:
                position = base.select('.//p[@class="headline-title title"]//text()')
                position = ''.join(textify(position).strip())
            if position:
                current_position.append(modify(position.replace('--','')))
        current_position = re.sub(r' +',' ', '<>'.join(current_position)).strip()


        current_company, company = [], ''
        current_com = base.select('.//dl[@id="overview"]//ul[@class="current"]//li')
        for curr in current_com:
            company = ''.join(textify(cur.select('.//span[@class="org summary"]/text()')))
            if not company:
                company = ''.join(re.findall(r' at (.*)', textify(curr.select('.//text()'))))
            if company:
                current_company.append(modify(company.replace('--','')))
        if company == '':
            company = textify(base.select('.//p[@class="headline-title title"]//text()'))
            company = ''.join(re.findall(r' at (.*)', company))
            if company:
                current_company.append(modify(company.replace('--','')))
        current_company = re.sub(r' +',' ', '<>'.join(current_company)).strip()

        previous_position = base.select('.//dl[@id="overview"]//ul[@class="past"]//li')
        previous_position = [modify(textify(pr_pos.select('.//text()')).strip()) for pr_pos in previous_position if pr_pos]
        previous_position = re.sub(r' +',' ', '<>'.join(previous_position)).strip()

        skills = hdoc.select('//div[@id="profile-skills"]//ol[@class="skills"]//li')
        skills = [modify(textify(skill.select('.//text()'))) for skill in skills if skill]
        skills = re.sub(r' +',' ', '<>'.join(skills)).strip()

        honors_and_awards = base.select('.//dt[contains(text(),"Honors and Awards:")]/following-sibling::dd[1]/p')
        honors_and_awards = [modify(textify(honor.select('.//text()'))) for honor in honors_and_awards if honor]
        if not honors_and_awards:
            honors_and_awards = base.select('.//div[@id="profile-honorsawards"]//div[@class="content"]/ul/li')
            honors_and_awards = [modify(textify(honor.select('./h3/text()'))) for honor in honors_and_awards if honor]
        honors_and_awards = re.sub(r' +',' ', '<>'.join(honors_and_awards)).strip()

        image_url = textify(base.select('.//div[contains(@class,"image")]/img/@src')).strip()
        interests = modify(textify(base.select('.//dd[@id="interests"]/p/text()')))
        if interests:
            interests = [interest.strip() for interest in interests.split(',')]
            interests = re.sub(r' +',' ', '<>'.join(interests)).strip()

        groups = base.select('.//dd[@id="pubgroups"]/ul[@class="groups"]/li')
        groups = [modify(textify(group.select('.//text()'))) for group in groups if group]
        groups = re.sub(r' +', ' ', '<>'.join(groups)).strip()

        p_websites = []
        websites = base.select('.//dd[@class="websites"]//li[@class="website"]/a/@href')
        for website in websites:
            website = 'http://www.linkedin.com' + textify(website)
            p_websites.append(website)
        if not websites: p_websites = ''
        websites = re.sub(r' +',' ', '<>'.join(p_websites)).strip()

        contact_for = base.select('.//div[@class="interested"]/ul/li')
        contact_for = [modify(textify(contact.select('.//text()'))) for contact in contact_for if contact]
        contact_for = re.sub(r' +',' ', '<>'.join(contact_for)).strip()

        education = base.select('.//dl[@id="overview"]//dd[@class="summary-education"]//ul/li')
        education = [modify(textify(edu.select('.//text()'))) for edu in education if edu]
        education = re.sub(r' +',' ', '<>'.join(education)).strip()

        ref_url = (re.sub(r'http://.*?\.linkedin', r'http://www.linkedin', response.url)).strip()
        pub_id = str(response.meta['_id'])

        now = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%d %H:%M:%S")

        values = ['', xcode(pub_id), first_name, last_name, industry, location,
                          current_position, previous_position, current_company,
                         skills, education, summary, specialities, connections,
                         recommendations, honors_and_awards, interests, groups,
                           websites, contact_for, image_url, ref_url, 'juicer_crawler', now, now]

        profile_file = file("/home/headrun/niranjan/%s_profile/%s_profile_details" %(category,category), "ab+")
        profile_file.write('%s\n' % xcode(re.sub(r' +',' ', '#<><>#'.join(values)).strip()))
        profile_file.close()


        u_query = "update puburls set is_crawled=1,modified_at=now() where id=%s"
        u_values = (pub_id)
        update_file = file("/home/headrun/niranjan/%s_profile/%s_update_details" %(category,category), "ab+")
        update_file.write('%s\n%s\n' %(u_query, repr(u_values)))
        update_file.close()


        experience = base.select('.//div[@id="profile-experience"]//div[@class="content vcalendar"]/div/div')
        for ex_node in experience:
            position = ex_node.select('.//div[@class="postitle"]//span[@class="title"]//text()')
            position = modify(textify(position))
            old_company = modify(textify(ex_node.select('.//div[@class="postitle"]//span[@class="org summary"]//text()')))

            old_location = modify(textify(ex_node.select('.//span[@class="location"]/text()')))
            old_summary = ex_node.select('.//p[contains(@class,"description")]/text()')
            old_summary = [(textify(summary)).replace('-','') for summary in old_summary if summary]
            old_summary = re.sub(r' +',' ', '<>'.join([modify(older) for older in old_summary if older])).strip()

            start_date = modify(textify(ex_node.select('.//p[@class="period"]/abbr[@class="dtstart"]/@title')))
            end_date = ''
            date = textify(ex_node.select('.//p[@class="period"]/abbr[@class="dtstamp"]/@title/text()'))
            end_date = end_date if date else modify(textify(ex_node.select('.//p[@class="period"]/abbr[@class="dtend"]/@title')))

            exp_values = ['',pub_id, position, old_company, old_location,
                           start_date, end_date, old_summary, now, now]

            if not exp_values: exp_values = ''
            if exp_values != '':
                exp_file = file("/home/headrun/niranjan/%s_profile/%s_exp_details" %(category,category), "ab+")
                exp_file.write('%s\n' % xcode(re.sub(r' +',' ', '#<><>#'.join(exp_values)).strip()))
                exp_file.close()
        update(response.meta['_id'])


def update(_id):
    upt = "UPDATE linkedin_urls SET is_crawled = 1, modified_at = now() WHERE pub_id = %s"
    upt_value = (_id)
    is_crawled_file = file("/home/headrun/niranjan/%s_profile/%s_is_crawled_details" %(category,category), "ab+")
    is_crawled_file.write('%s\n%s\n' %(upt, repr(upt_value)))
    is_crawled_file.close()


def init_logger():
    log = logging.getLogger('/home/headrun/niranjan/%s_profile/linkedin.log' %(category))
    hdlr = logging.FileHandler('/home/headrun/niranjan/%s_profile/linkedin.log' %(category))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)

    return log

log = init_logger()

def modify(data):
    try:
        data = ''.join([chr(ord(x)) for x in data]).decode('utf8', 'ignore').encode('utf8')
        return varchar(data)
    except ValueError or UnicodeDecodeError or UnicodeEncodeError:
        try:
            return varchar(data.encode('utf8'))
        except  ValueError or UnicodeEncodeError or UnicodeDecodeError:
            try:
                return varchar(data)
            except ValueError or UnicodeEncodeError or UnicodeDecodeError:
                try:
                    return varchar(xcode(data).encode('utf-8','ignore').decode('ascii', 'ignore'))
                except UnicodeDecodeError:
                    data = normalize('NFKD', data.decode('utf-8','ignore')).encode('ascii', 'ignore')
                    return varchar(data)


def varchar(string):
    return re.sub(r' +',' ', string.replace('&amp;','&').replace('&quot;','"').replace('&gt;',
                          '>').replace('&lt;','<').replace(u'\uf0fc\t', '').replace(u'\uf0d8',
                        '').replace(u'\uf0b7','').replace(u"\uf0f3\t",'').replace(u'\uf0d4\t',
              '').replace(u'\u2022','').replace(u'\xbb','').replace('\n','').replace('\t','')).strip()
