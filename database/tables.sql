
CREATE DATABASE IF NOT EXISTS PaperRecommendation DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use PaperRecommendation; 

-- 论文基本信息表
DROP TABLE IF EXISTS PaperInfo;
CREATE TABLE PaperInfo(
    id INT NOT NULL AUTO_INCREMENT,
    author_id INT NOT NULL,
    source_id INT NOT NULL,
    publication_time DATETIME,
    title VARCHAR(256),
    abstract TEXT,
    keywords VARCHAR(128),
    PRIMARY KEY(id)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 作者信息表
DROP TABLE IF EXISTS AuthorInfo;
CREATE TABLE AuthorInfo(
    id INT NOT NULL AUTO_INCREMENT,
    author_affiliation_id INT,
    name VARCHAR(64),
    PRIMARY KEY(id)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 论文作者关系表
DROP TABLE IF EXISTS PaperAuthorRel;
CREATE TABLE PaperAuthorRel(
    id INT NOT NULL AUTO_INCREMENT,
    author_id INT NOT NULL,
    paper_id INT NOT NULL,
    ord SMALLINT NOT NULL,
    PRIMARY  KEY(ID)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 部门表
DROP TABLE IF EXISTS Affiliation;
CREATE TABLE Affiliation(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128),
    PRIMARY KEY(id)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 论文引用关系表
DROP TABLE IF EXISTS PaperRef;
CREATE TABLE PaperRef(
    id INT NOT NULL AUTO_INCREMENT,
    ref_id INT NOT NULL,
    beref_id INT NOT NULL,
    PRIMARY KEY(id)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 推荐结果模板表
DROP TABLE IF EXISTS RecForUser;
CREATE TABLE RecForUser(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    src_paper_id INT NOT NULL, -- 推荐源paper id
    rec_paper_id INT NOT NULL, -- 推荐paper id
    rec_time DATETIME NOT NULL,
    PRIMARY KEY(id)
)ENGINE=MyISAM  AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 论文来源表
DROP TABLE IF EXISTS Sources;
CREATE TABLE Sources(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256),
    level SMALLINT NOT NULL,
    type INT NOT NULL,
    PRIMARY KEY(id)
);


-- 知识分类表
DROP TABLE IF EXISTS Classfination;
CREATE TABLE Classfination(
    id INT NOT NULL AUTO_INCREMENT,
    keywords VARCHAR(128),
    PRIMARY KEY(id)
);

-- 读者知识分类表
DROP TABLE IF EXISTS ReaderClass;
CREATE TABLE ReaderClass(
    id INT NOT NULL,
    reader_id INT NOT NULL,
    class_id INT NOT NULL,
    PRIMARY KEY(id)
);

