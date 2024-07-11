delete from s_choose where sub_id in (select id from s_subject where paper_id = %s);
delete from s_pic where id in (select pic_id from s_sub_pic  where sub_id  in  (select id from s_subject where paper_id = %s));
delete from s_pic where id in (select pic_id from s_sub_ref_pic  where sub_id  in  (select id from s_subject where paper_id = %s));
delete from s_sub_ch where sub_id in (select id from s_subject where paper_id = %s);
delete from s_sub_pic where sub_id in (select id from s_subject where paper_id = %s);
delete from s_sub_ref_pic where sub_id  in  (select id from s_subject where paper_id = %s);
delete from s_subject where paper_id  = %s;
delete from s_paper where id = %s;




-- 查询报错的 paper 页面
select id from s_paper where p_title in (select distinct paper_title from s_err)



-- 根据 paper Id 删除所有垃圾数据
delete from s_choose where sub_id in (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err)));
delete from s_pic where id in (select pic_id from s_sub_pic  where sub_id  in  (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err))));
delete from s_pic where id in (select pic_id from s_sub_ref_pic  where sub_id  in  (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err))));
delete from s_sub_ch where sub_id in (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err)));
delete from s_sub_pic where sub_id in (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err)));
delete from s_sub_ref_pic where sub_id  in  (select id from s_subject where paper_id in (select id from s_paper where p_title in (select distinct paper_title from s_err)));
delete from s_subject where paper_id  in (select id from s_paper where p_title in (select distinct paper_title from s_err));
delete from s_paper where p_title in (select distinct paper_title from s_err);




-- 排查数据质量情况
select * from s_subject where paper_id not in (select id from s_paper sp);
select * from s_paper where id not in (select paper_id from s_subject );

delete from s_subject where paper_id not in (select id from s_paper sp);
delete from s_paper where id not in (select paper_id from s_subject );