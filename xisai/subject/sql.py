insert_s_paper_sql = "insert into s_paper(p_type,p_title,p_report_url,p_do_url) value (%s, %s, %s, %s);"
insert_s_subject_sql = "insert into s_subject(paper_id,sub_no,sub_title) value (%s, %s, %s)"
insert_s_pic_sql = "insert into s_pic(pic_url) value (%s)"
insert_s_sub_pic_sql = "insert into s_sub_pic(sub_id,pic_id) value (%s, %s)"
