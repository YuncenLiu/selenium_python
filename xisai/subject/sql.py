insert_s_paper_sql = "insert into s_paper(p_type,p_title,p_report_url,p_do_url) value (%s, %s, %s, %s);"
insert_s_subject_sql = "insert into s_subject(paper_id,sub_no,sub_title) value (%s, %s, %s);"
insert_s_pic_sql = "insert into s_pic(pic_url) value (%s);"
insert_s_sub_pic_sql = "insert into s_sub_pic(sub_id,pic_id) value (%s, %s);"
insert_s_choose_sql = "insert into s_choose(sub_id,ch_a,ch_b,ch_c,ch_d,ch_true,ch_my) value (%s, %s, %s, %s, %s, %s, %s);"
insert_s_sub_ch_sql = "insert into s_sub_ch(sub_id,ch_id) value (%s, %s);"
insert_s_sub_ref_pic_sql = "insert into s_sub_ref_pic(sub_id,pic_id) value (%s, %s)"
update_s_subject_sql = "update s_subject set sub_tag = %s , sub_info = %s , sub_ref = %s where id = %s"

# 失败插入错误试卷名
insert_s_err_sql = "insert into s_err(paper_title) value(%s)"

select_count_s_paper_sql = "select count(*) as ct from s_paper where p_type = %s and p_title = %s"
select_max_paper_id_sql = "select id from s_paper order by id desc limit 1"
select_max_paper_title_sql = "select p_title from s_paper order by id desc limit 1"



delete_init_choose_sql = "delete from s_choose where sub_id in (select id from s_subject where paper_id = %s)"
delete_init_pic_sql1 = "delete from s_pic where id in (select pic_id from s_sub_pic  where sub_id  in  (select id from s_subject where paper_id = %s));"
delete_init_pic_sql2 = "delete from s_pic where id in (select pic_id from s_sub_ref_pic  where sub_id  in  (select id from s_subject where paper_id = %s));"
delete_init_sub_ch_sql = "delete from s_sub_ch where sub_id in (select id from s_subject where paper_id =%s)"
delete_init_sub_pic_sql = "delete from s_sub_pic where sub_id in (select id from s_subject where paper_id =%s)"
delete_init_sub_ref_pic_sql = "delete from s_sub_ref_pic where sub_id  in  (select id from s_subject where paper_id =%s);"
delete_init_subject_sql = "delete from s_subject where paper_id  = %s;"
delete_init_paper_sql = "delete from s_paper where id = %s;"