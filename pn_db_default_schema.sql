drop table if exists tbl1xx;
drop table if exists tbl2xx;
drop table if exists tbl3xx;
drop table if exists tbl4xx;
drop table if exists tbl5xx;
drop table if exists tbl6xx;
drop table if exists users;

-- *************************
-- *      Table setup      *
-- *       Resistors       *
-- *************************

create table tbl1xx (
  grp integer check( length(grp) = 3) check( grp LIKE "1%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=4) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *      Capacitors       *
-- *************************

create table tbl2xx (
  grp integer check( length(grp) = 3) check( grp LIKE "2%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=5) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *     Passive Parts     *
-- *************************

create table tbl3xx (
  grp integer check( length(grp) = 3) check( grp LIKE "3%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=4) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *     Active Parts      *
-- *************************

create table tbl4xx (
  grp integer check( length(grp) = 3) check( grp LIKE "4%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=4) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *         IC's          *
-- *************************

create table tbl5xx (
  grp integer check( length(grp) = 3) check( grp LIKE "5%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=4) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *       Not above       *
-- *************************

create table tbl6xx (
  grp integer check( length(grp) = 3) check( grp LIKE "6%" ) not null,
  pn integer primary key autoincrement,
  ver integer check(length(ver) <= 2) check(length(ver) > 0) not null default 01,
  value text check( length(value) <=4) check(length(value) > 0) not null,
  param text check( length(param) <=5) check(length(param) > 0) not null,
  desc text check( length(desc) <=10) check(length(desc) > 0) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'no', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *     Table Setup       *
-- *        Users          *
-- *************************

CREATE TABLE users (
    google_id varchar(21) check( length(google_id) = 21) primary key,
    usr_lvl int check( usr_lvl in ( 0, 1, 2 )),
    usr_email varchar(74) check( length(usr_email) <=74),
    sent_auth_req_email varchar(3)
);
-- *************************
-- *       Demo Data       *
-- *       Resistor        *
-- *************************

INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(101,'100','5%','1/16','active','yes','www.google.com');
INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(101,'1M','5%','1/10','active','n/a','www.ddr.com');
INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(102,'10k','2%','1/16','inactive','yes','www.test.com');
INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(110,'100','1%','1/4','deleted','no','asd');
INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(111,'1k','.1%','1/5','active','yes','www.hestore.com');
-- For spam fill
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');
-- INSERT INTO tbl1xx (grp, value, param, desc, status, rohs, datasheet) VALUES
-- (101,'100','5%','1/16','active','yes','www.google.com');

-- *************************
-- *       Demo Data       *
-- *       Capacitor       *
-- *************************

INSERT INTO tbl2xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(201,'100nF','10V','5%','active','yes','www.google.com');
INSERT INTO tbl2xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(202,'10uF','5V','2%','inactive','yes','www.facebook.com');
INSERT INTO tbl2xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(202,'1nF','25V','1%','n/a','no','www.test.com');
INSERT INTO tbl2xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(203,'100nF','50V','10%','deleted','n/a','qwerty');

-- *************************
-- *       Demo Data       *
-- *     Passive Parts     *
-- *************************

INSERT INTO tbl3xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(301,'1k','5%','1/16','active','yes','www.google.com');
INSERT INTO tbl3xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(303,'1k','55%','1/6','inactive','no','n/a');
INSERT INTO tbl3xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(310,'10k','1%','6','n/a','n/a','www.ddr.com');

-- *************************
-- *       Demo Data       *
-- *      Active Parts     *
-- *************************

INSERT INTO tbl4xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(401,'1k','5%','1/16','active','yes','wtest');
INSERT INTO tbl4xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(402,'1k','55%','1/6','inactive','no','asd');
INSERT INTO tbl4xx (grp, value, param, desc, status, rohs, datasheet) VALUES
(403,'10k','1%','1/6','n/a','n/a','www.ddr.com');
