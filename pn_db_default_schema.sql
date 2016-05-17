drop table if exists resistor;
drop table if exists capacitor;
drop table if exists passive;
drop table if exists active;
drop table if exists ic;
drop table if exists other;

-- *************************
-- *      Table setup      *
-- *       Resistors       *
-- *************************

create table resistor (
  pn integer primary key autoincrement,
  value text check( length(value) <=4) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *      Capacitors       *
-- *************************

create table capacitor (
  pn integer primary key autoincrement,
  value text check( length(value) <=6) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *     Passive Parts     *
-- *************************

create table passive (
  pn integer primary key autoincrement,
  value text check( length(value) <=4) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *     Active Parts      *
-- *************************

create table active (
  pn integer primary key autoincrement,
  value text check( length(value) <=4) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *         IC's          *
-- *************************

create table ic (
  pn integer primary key autoincrement,
  value text check( length(value) <=4) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *      Table setup      *
-- *       Not above       *
-- *************************

create table other (
  pn integer primary key autoincrement,
  value text check( length(value) <=4) not null,
  param text check( length(param) <=5) not null,
  desc text check( length(desc) <=10) default 'n/a',
  status text check( status in ('active','inactive','deleted','n/a')) not null default 'n/a',
  rohs text check(rohs in ('yes', 'YES', 'no', 'NO', 'n/a')) not null default 'n/a',
  datasheet text check( length(datasheet) <=30) default 'n/a'
);

-- *************************
-- *       Demo Data       *
-- *       Resistor        *
-- *************************

INSERT INTO resistor (value, param, desc, status, rohs, datasheet) VALUES ('100','5%','1/16','active','yes','www.google.com');
INSERT INTO resistor (value, param, desc, status, rohs, datasheet) VALUES ('1M','5%','1/10','active','n/a','www.ddr.com');
INSERT INTO resistor (value, param, desc, status, rohs, datasheet) VALUES ('10k','2%','1/16','inactive','yes','www.test.com');
INSERT INTO resistor (value, param, desc, status, rohs, datasheet) VALUES ('100','1%','1/4','deleted','no','asd');
INSERT INTO resistor (value, param, desc, status, rohs, datasheet) VALUES ('1k','.1%','1/5','active','yes','www.hestore.com');

-- *************************
-- *       Demo Data       *
-- *       Capacitor       *
-- *************************

INSERT INTO capacitor (value, param, desc, status, rohs, datasheet) VALUES ('100nF','10V','5%','active','yes','www.google.com');
INSERT INTO capacitor (value, param, desc, status, rohs, datasheet) VALUES ('10uF','5V','2%','inactive','yes','www.facebook.com');
INSERT INTO capacitor (value, param, desc, status, rohs, datasheet) VALUES ('1nF','25V','1%','n/a','no','www.test.com');
INSERT INTO capacitor (value, param, desc, status, rohs, datasheet) VALUES ('100nF','50V','10%','deleted','n/a','qwerty');

-- *************************
-- *       Demo Data       *
-- *     Passive Parts     *
-- *************************

INSERT INTO passive (value, param, desc, status, rohs, datasheet) VALUES ('1k','5%','1/16','active','yes','www.google.com');
INSERT INTO passive (value, param, desc, status, rohs, datasheet) VALUES ('1k','55%','1/6','inactive','no','n/a');
INSERT INTO passive (value, param, desc, status, rohs, datasheet) VALUES ('10k','1%','6','n/a','n/a','www.ddr.com');

-- *************************
-- *       Demo Data       *
-- *      Active Parts     *
-- *************************

INSERT INTO active (value, param, desc, status, rohs, datasheet) VALUES ('1k','5%','1/16','active','yes','wtest');
INSERT INTO active (value, param, desc, status, rohs, datasheet) VALUES ('1k','55%','1/6','inactive','no','asd');
INSERT INTO active (value, param, desc, status, rohs, datasheet) VALUES ('10k','1%','6','n/a','n/a','www.ddr.com');


