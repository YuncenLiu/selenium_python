DROP TABLE IF EXISTS s_paper;
CREATE TABLE s_paper
(
    id           INT AUTO_INCREMENT PRIMARY KEY,
    p_type       VARCHAR(100) NOT NULL,
    p_title      VARCHAR(100) NOT NULL,
    p_report_url VARCHAR(200),
    p_do_url     VARCHAR(200)
);
DROP TABLE IF EXISTS s_subject;
CREATE TABLE s_subject
(
    id        INT AUTO_INCREMENT PRIMARY KEY,
    paper_id  INT NOT NULL,
    sub_no    VARCHAR(100),
    sub_title VARCHAR(2000),
    sub_tag   VARCHAR(100),
    sub_info  VARCHAR(100),
    sub_ref   VARCHAR(2000)
);
DROP TABLE IF EXISTS s_pic;
CREATE TABLE s_pic
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    pic_url VARCHAR(500) NOT NULL
);
DROP TABLE IF EXISTS s_sub_pic;
CREATE TABLE s_sub_pic
(
    id     INT AUTO_INCREMENT PRIMARY KEY,
    sub_id INT NOT NULL,
    pic_id INT NOT NULL
);
DROP TABLE IF EXISTS s_sub_ref_pic;
CREATE TABLE s_sub_ref_pic
(
    id     INT AUTO_INCREMENT PRIMARY KEY,
    sub_id INT NOT NULL,
    pic_id INT NOT NULL
);
DROP TABLE IF EXISTS s_choose;
CREATE TABLE s_choose
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    sub_id  INT,
    ch_a    VARCHAR(500) NOT NULL,
    ch_b    VARCHAR(500) NOT NULL,
    ch_c    VARCHAR(500) NOT NULL,
    ch_d    VARCHAR(500) NOT NULL,
    ch_true VARCHAR(10)  NOT NULL,
    ch_my   VARCHAR(10)
);
DROP TABLE IF EXISTS s_sub_ch;
CREATE TABLE s_sub_ch
(
    id     INT AUTO_INCREMENT PRIMARY KEY,
    sub_id INT NOT NULL,
    ch_id  INT NOT NULL
);