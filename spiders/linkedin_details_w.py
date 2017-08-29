import MySQLdb
from juicer.utils import *
from unicodedata import normalize
import logging
log = logging.getLogger()

class LinkedinDetails(JuicerSpider):
    name = "linkedin_profile_"

    settings.overrides['USER_AGENT_LIST'] = ['Mozilla/5.0 (compatible; Veveobot; +http://corporate.veveo.net/contact/)']
    global modify, varchar, category
    category = ''.join(re.findall(r'_profile_(\w)', name))

    def start_requests(self):
        requests = []
        conn = MySQLdb.connect('localhost','root','root','LINKEDIN')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        print "Came here 01"
        sql = "SELECT pub_id, profile_url FROM linkedin_urls_new WHERE category= '%s' AND is_crawled != 5 " %(category)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            my_list = []
            for row in results:
                _id = row[0]
                my_list.append(str(_id))
                url = row[1]
                r = Request(url, self.parse, None, meta={'_id': _id})
                requests.extend(r)

            my_tuple = tuple(my_list)
            try:
                query = "UPDATE linkedin_urls_new SET is_crawled = 4 WHERE pub_id in %s"
                values = str((my_tuple))
                cursor.execute(query % values)
            except:
                log.info("Unable to update-4 id %s" %_id)

        except:
            log.info("Error: unable to fecth data")

        return requests

    def parse(self, response):
        hdoc = HTML(response)
        base = hdoc.select('//div[@id="content"]')
        now = datetime.datetime.now()

        pub_id = response.meta['_id']
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

        #
        languages = hdoc.select('//div[@id="profile-languages"]/div[@class="content"]/ul[@class="languages competencies"]/li/h3/text()')
        languages = [textify(i).encode('UTF-8') for i in languages]
        languages = '<>'.join(languages)
        tab_languages_nodes = base.select('.//div[@id="profile-languages"]/div[@class="content"]/ul/li')
        if tab_languages_nodes:
            for lan_node in tab_languages_nodes:
                lan_title =  modify(textify(lan_node.select('./h3/text()'))).strip()
                lan_prof = ''
                lan_prof = modify(textify(lan_node.select('./span[@class="proficiency"]/text()'))).strip().replace('(', '').replace(')','')
                lan_title = varchar(lan_title).encode('ascii', 'ignore')
                lan_prof = varchar(lan_prof).encode('ascii', 'ignore')

                values = [str(pub_id),lan_title,lan_prof,str(now), str(now)]
                values = "#<><>#".join([str(k) for k in values])
                out_file = file('/home/headrun/venu/linkedin_details/languages','ab+')
                out_file.write('%s\n' % xcode(re.sub(r' +',' ',values)))
                out_file.flush()
                out_file.close()
 
        tab_compcourses_nodes = base.select('.//div[@id="profile-courses"]/div[@class="content"]/ul/li')
        for cour_node in tab_compcourses_nodes:
            cour_location = modify(textify(cour_node.select('./div[@class="postitle"]/h4/strong/span/text()'))).strip() or \
                                            modify(textify(cour_node.select('./h4/text()'))).strip()

            cour_location = varchar(cour_location).encode('ascii','ignore')
            cour_title = modify(textify(cour_node.select('./div/h3/span[@class="title"]/text()'))).strip() or \
                                modify(textify(cour_node.select('./h3/text()'))).strip()
            cour_title = varchar(cour_title).encode('ascii', 'ignore').encode('ascii', 'ignore')
            cour_competencies = cour_node.select('./ul/li[@class="competency"]/text()')
            cour_competencies = [modify(textify(i).strip()) for i in cour_competencies if i]
            cour_competencies = [varchar(i).strip() for i in cour_competencies if i]
            cour_competencies = '<>'.join(cour_competencies)
            cour_competencies = varchar(cour_competencies).encode('ascii', 'ignore')

            values = [str(pub_id),cour_title,cour_location,cour_competencies,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/compcourses','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_certifications_nodes = base.select('.//div[@id="profile-certifications"]/div[@class="content"]/ul/li')
        for cer_node in tab_certifications_nodes:
            cer_title = modify(textify(cer_node.select('./h3/text()'))).strip()
            cer_title = varchar(cer_title).encode('ascii', 'ignore')
            cer_org = modify(textify(cer_node.select('./ul[@class="specifics"]/li[@class="fn org"]/text()'))).strip()
            cer_org = varchar(cer_org).encode('ascii', 'ignore')
            cer_lic_number = modify(textify(cer_node.select('./ul[@class="specifics"]/li[@class="license-number"]/text()'))).strip().replace('License', '')
            cer_lic_number = varchar(cer_lic_number).encode('ascii','ignore')
            try:
                cer_start_date = modify(textify(cer_node.select('./ul[@class="specifics"]/li/span[@class="dtstart"]/text()'))).strip()
                if cer_start_date:
                    cer_start_date = parse_date(varchar(cer_start_date).encode('ascii', 'ignore'))
                else:
                    cer_start_date = ''
                cer_end_date = modify(textify(cer_node.select('./ul[@class="specifics"]/li/span[@class="dtend"]/text()'))).strip()
                if cer_end_date:
                    cer_end_date = parse_date(varchar(cer_end_date))
                else:
                    cer_end_date = ''
            except:
                cer_start_date = cer_end_date = ''

            values = [str(pub_id),cer_title,cer_org,cer_lic_number,cer_start_date,cer_end_date,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/certifications','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_projects_nodes = base.select('.//div[@id="profile-projects"]/div[@class="content"]/ul/li')
        for pro_node in tab_projects_nodes:
            pro_title = modify(textify(pro_node.select('./h3/cite/text()'))).strip() or modify(textify(pro_node.select('./h3/a/text()'))).strip()
            pro_title = varchar(pro_title).encode('ascii', 'ignore')
            pro_date_info = modify(textify(pro_node.select('./ul[@class="specifics"]/li/text()'))).strip()
            pro_start_date = pro_end_date = ''
            try:
                if pro_date_info:
                    pro_start_date = pro_date_info.split(' to ')[0].strip()
                    pro_end_date = pro_date_info.split(' to ')[-1].strip()
                    if 'Present' in pro_end_date:
                        pro_end_date = ''
                    pro_start_date = parse_date(varchar("01 " + pro_start_date).encode('ascii','ignore'))
                    pro_end_date = parse_date(varchar("01 " + pro_end_date).encode('ascii', 'ignore'))
            except:
                pro_start_date = pro_end_date = ''
            pro_team_member_links = pro_node.select('./div[@class="attribution"]/a/@href')
            pro_team_member_links = [varchar(textify(i)).strip() for i in pro_team_member_links if i]
            members = []
            for mem in pro_team_member_links:
                if 'http://www.linkedin.com' not in mem:
                    mem = 'http://www.linkedin.com%s' % mem
                    members.append(mem)
            pro_summary = textify(pro_node.select('./div/p/text()')).encode('ascii', 'ignore')
            pro_summary = pro_summary

            all_member_links = '<>'.join(members)

            all_team_member_names = pro_node.select('./div[@class="attribution"]//text()')
            for team_mem in all_team_member_names: 
                if ',' in textify(team_mem):
                    more_team = textify(team_mem).split(',')
                    all_team_member_names.extend(more_team)
                    all_team_member_names.remove(team_mem)

            all_team_member_names = [textify(i).replace('Team Members:', '').replace(',','').strip() for i in  all_team_member_names if i]
            all_team_member_names = [modify(varchar(textify(i))) for i in all_team_member_names if i]
            all_team_member_names = '<>'.join(all_team_member_names).encode('ascii', 'ignore')

            values = [str(pub_id),pro_title,pro_start_date,pro_end_date,pro_summary,all_team_member_names,all_member_links,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/projects','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_publications_nodes = base.select('.//div[@id="profile-publications"]/div[@class="content"]/ul/li')
        for pub_node in tab_publications_nodes:
            pub_organization = modify(textify(pub_node.select('./ul[@class="specifics"]/li/text()'))).strip()
            pub_organization = varchar(pub_organization).encode('ascii', 'ignore')
            pub_title = modify(textify(pub_node.select('./h3/cite/text()'))).strip() or modify(textify(pub_node.select('./h3/a/cite/text()'))).strip()
            pub_title = varchar(pub_title).encode('ascii','ignore')
            pub_summary = ''

            pub_authors_links = pub_node.select('./div[@class="attribution"]/a/@href')
            pub_authors_links = [modify(textify(i).strip()) for i in pub_authors_links if i]
            pub_authors_links = [varchar(i).replace(',','').strip() for i in pub_authors_links]
            pub_authors_links = '<>'.join(pub_authors_links)

            pub_author_names = pub_node.select('./div[@class="attribution"]//text()')
            for auth_name in pub_author_names:
                if ','  in textify(auth_name):
                    names = textify(auth_name).split(',')
                    pub_author_names.extend(names)
                    pub_author_names.remove(auth_name)

            pub_author_names = [textify(i).replace('Authors:', '').replace(',', '').strip() for i in pub_author_names if i]
            pub_author_names = [modify(varchar(i).strip()) for i in pub_author_names if i]
            pub_author_names = '<>'.join(pub_author_names).encode('ascii', 'ignore')

            values = [str(pub_id),pub_organization,pub_title,pub_author_names,pub_authors_links,pub_summary,str(now),str(now)]
            values = "#<><>#".join([modify(varchar(str(k))) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/publications','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_honorawards_nodes = base.select('.//div[@id="profile-honorsawards"]/div[@class="content"]/ul/li')
        for hon_node in tab_honorawards_nodes:
            hon_title = modify(textify(hon_node.select('./h3/text()'))).strip()
            hon_title = varchar(hon_title).encode('ascii', 'ignore')
            hon_received_date = modify(textify(hon_node.select('./ul[@class="specifics"]/li/text()'))).strip()
            try:
                hon_received_date = parse_date(varchar(hon_received_date))
            except:
                hon_received_date = ''
            hon_org = modify(textify(hon_node.select('./div[@class="org-position"]/text()'))).strip()
            hon_org = varchar(hon_org).encode('ascii','ignore')
            hon_summary = modify(textify(hon_node.select('./p[@class=" summary"]/text()'))).strip()
            hon_summary = varchar(hon_summary).encode('ascii', 'ignore')

            values = [str(pub_id),hon_title,hon_received_date,hon_org,hon_summary,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/honorawards','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        honors_and_awards = base.select('.//dt[contains(text(),"Honors and Awards:")]/following-sibling::dd[1]/p/text()')
        honors_and_awards = [textify(i).strip() for i in honors_and_awards if textify(i).strip()]
        honors_and_awards = '<>'.join(honors_and_awards)
        honors_and_awards = varchar(honors_and_awards)

        tab_patents_nodes = base.select('.//div[@id="profile-patents"]/div[@class="content"]/ul/li')
        for pat_node in tab_patents_nodes:
            pat_title = modify(textify(pat_node.select('./h3/text()'))).strip() or modify(textify(pat_node.select('./h3/a/text()'))).strip() 
            pat_title = varchar(pat_title).encode('ascii', 'ignore')
            pat_org = modify(textify(pat_node.select('./ul[@class="specifics"]/li[1]//text()'))).strip()
            pat_org = varchar(pat_org).encode('ascii', 'ignore')

            pat_date = modify(textify(pat_node.select('./ul[@class="specifics"]/li[2]//text()'))).strip()
            pat_date_issued = pat_date_filed = ''
            if 'Issued' in pat_date:
                pat_date_issued = parse_date("".join(re.findall(r'Issued (.*)', pat_date)))
            elif 'Filed' in pat_date:
                pat_date_filed = parse_date("".join(re.findall(r'Filed (.*)', pat_date)))
                pat_date_issued = ''
            else:
                pat_date_filed = ''

            final_pat_date = ''

            pat_inventor_links = pat_node.select('./div[@class="attribution"]/a/@href')
            pat_inventor_links = [varchar(textify(i).strip()) for i in pat_inventor_links if i]
            pat_inventor_links = '<>'.join(pat_inventor_links).encode('ascii', 'ignore')

            pat_inventor_names = pat_node.select('./div[@class="attribution"]//text()')
            for inv_name in pat_inventor_names:
                if ','  in textify(inv_name):
                    names = textify(inv_name).split(',')
                    pat_inventor_names.extend(names)
                    pat_inventor_names.remove(inv_name)

            pat_inventor_names = [textify(i).replace('Inventors:', '').replace(',', '').strip() for i in pat_inventor_names if i]
            pat_inventor_names = [varchar(textify(i).strip()) for i in pat_inventor_names if i]
            pat_inventor_names = '<>'.join(pat_inventor_names).encode('ascii', 'ignore')

            values = [str(pub_id),pat_title,pat_org,pat_date_issued,pat_date_filed,pat_inventor_names,pat_inventor_links,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/patents','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_volunteering_nodes = base.select('.//div[@id="profile-volunteering"]/div[@class="content"]\
                                            /ul[@class="volunteering experienced"]/li[@class="experiences"]/ul/li')
        for vol_node in tab_volunteering_nodes:
            vol_org = modify(textify(vol_node.select('./div[@class="postitle"]/h5/strong/span/text()'))).strip()
            vol_org = varchar(vol_org).encode('ascii', 'ignore')
            vol_title = modify(textify(vol_node.select('./div[@class="postitle"]/h4/span[@class="title"]/text()'))).strip()
            vol_title = varchar(vol_title).encode('ascii','ignore')
            vol_categoty = modify(textify(vol_node.select('./ul[@class="specifics"]/li/text()'))).strip()
            vol_categoty = varchar(vol_categoty).encode('ascii','ignore')

            vol_start_date = parse_date(modify(textify(vol_node.select('./div[@class="period"]/abbr[1]/@title'))).strip())

            vol_end_date = parse_date(modify(textify(vol_node.select('./div[@class="period"]/abbr[2]/@title'))).strip())
            vol_date = (modify(textify(vol_node.select('./div[@class="period"]//text()'))).strip())
            if 'present' in vol_date:
                vol_end_date = ''
            vol_summary = modify(textify(vol_node.select('./div[@class="summary"]/p[@class=" description"]/text()'))).strip()
            vol_summary = varchar(vol_summary).encode('ascii','ignore')

            values = [str(pub_id),vol_org,vol_title,vol_categoty,vol_start_date,vol_end_date,vol_summary,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/volunteering','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_organizations_nodes = base.select('.//div[@id="profile-organizations"]/div[@class="content"]/ul/li')
        for org_node in tab_organizations_nodes:
            org_organization = modify(textify(org_node.select('./h3/text()'))).strip()
            org_organization = varchar(org_organization)
            org_designation = modify(textify(org_node.select('./div[@class="org-position"]/text()'))).strip()
            org_designation = varchar(org_designation)
            org_date_info = textify(org_node.select('./ul[@class="specifics"]/li//text()')).strip()
            org_start_date = org_end_date = ''
            try:
                if org_date_info:
                    org_start_date = org_date_info.split('to')[0].strip()
                    org_start_date = parse_date(modify("01 " + org_start_date))
                    org_end_date = org_date_info.split('to')[-1].strip()
                    if 'Present' in org_end_date:
                        org_end_date = ''
                    else:
                        org_end_date = parse_date(org_end_date)
            except:
                org_start_date = org_end_date = ''

            org_summary = ''

            values = [str(pub_id),org_organization,org_designation,str(org_start_date),str(org_end_date),org_summary,str(now),str(now)]
            values = "#<><>#".join(values)
            out_file = file('/home/headrun/venu/linkedin_details/organizations','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_testscores_nodes = base.select('.//div[@id="profile-testscores"]/div[@class="content"]/ul/li')
        for sco_node in tab_testscores_nodes:
            sco_title = modify(textify(sco_node.select('./h3/text()'))).strip() 
            sco_title = varchar(sco_title)
            sco_date = modify(textify(sco_node.select('./ul[@class="specifics"]/li[1]/text()'))).strip() 
            sco_date = parse_date(varchar("01 " + sco_date))
            sco_score = modify(textify(sco_node.select('./ul[@class="specifics"]/li[2]/text()'))).replace('Score:','').strip()
            sco_score = varchar(sco_score)
            sco_percent = modify(textify(sco_node.select('./div/p[@class=" description"]'))).strip() 
            final_percent = ''
            if sco_percent:
                sco_percent = re.findall('\d+', sco_percent)
                if sco_percent: final_percent = sco_percent[0]

            values = [str(pub_id),sco_title,sco_date,sco_score,final_percent,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/testscores','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()

        tab_education_nodes = base.select('.//div[@id="profile-education"]/div[@class="content vcalendar"]/div/div')
        for ed_node in tab_education_nodes:
            ed_organization = modify(textify(ed_node.select('./h3/text()'))).strip()
            ed_organization = varchar(ed_organization).encode('ascii', 'ignore')
            ed_courses = ed_node.select('.//h4/span')
            ed_course = ''
            for ed_cour in ed_courses:
                txt =  modify(textify(ed_cour.select('./text()'))).strip()
                more_txt = txt + ', '
                ed_course = ed_course + more_txt
            if ed_course.endswith(', '):
                ed_course = (ed_course[:-2]).encode('ascii', 'ignore')
            ed_start_date = "".join(re.findall(r'(\d+-\d+-\d+)',textify(ed_node.select('./p[@class="period"]/abbr[@class="dtstart"]/@title')))).strip()
            if ed_start_date:
                ed_start_date = parse_date(ed_start_date)
            ed_end_date = "".join(re.findall(r'(\d+-\d+-\d+)',textify(ed_node.select('./p[@class="period"]/abbr[@class="dtend"]/@title')))).strip()
            if ed_end_date:
                ed_end_date = parse_date(ed_end_date)
            ed_summary = modify(textify(ed_node.select('./p[contains(@class, "desc details-education")]//text()'))).strip()
            ed_summary = varchar(ed_summary).encode('ascii', 'ignore')

            values = [str(pub_id),ed_organization,ed_course,str(ed_start_date),str(ed_end_date),ed_summary,str(now),str(now)]
            values = "#<><>#".join([str(k) for k in values])
            out_file = file('/home/headrun/venu/linkedin_details/education','ab+')
            out_file.write('%s\n' %(values))
            out_file.flush()
            out_file.close()
        update(pub_id)

def update(_id):
    upt = "UPDATE linkedin_urls_new SET is_crawled = 5, modified_at = NOW() WHERE pub_id = %s"
    upt_value = (_id)
    is_crawled_file = file("/home/headrun/venu/%s_is_crawled_details" %(category), "ab+")
    is_crawled_file.write('%s\n%s\n' %(upt, repr(upt_value)))
    is_crawled_file.close()

def init_logger():
    log = logging.getLogger('/home/headrun/venu/linkedin_details/linkedin.log')
    hdlr = logging.FileHandler('/home/headrun/venu/linkedin_details/linkedin.log')
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
              '').replace(u'\u2022','').replace(u'\xbb','').replace('\n','').replace('\t','').replace('\u2019','')).strip()


