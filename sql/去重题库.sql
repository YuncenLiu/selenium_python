create table c_subject as select
	id,paper_id,sub_no,sub_title,sub_tag,sub_info,sub_ref
from
	(
	select
		ROW_NUMBER () over(PARTITION by sub_title)r ,
		a.*
	from
		s_subject a) b where r = 1;