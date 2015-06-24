drop table if exists sina.feed;
drop table if exists sina.author;
create table sina.author (id BIGINT  AUTO_INCREMENT not null, name varchar(100) not null,url  varchar(500) not null,PRIMARY KEY(id))engine=innodb, charset='utf8';
create INDEX author_id on sina.author(id);
create table sina.feed (id BIGINT AUTO_INCREMENT not null,author_id BIGINT,content varchar(500) not null,replies integer,retweets integer,timestamp TIMESTAMP,PRIMARY KEY (id))engine=innodb, charset='utf8';
create INDEX feed_id on sina.feed(id);