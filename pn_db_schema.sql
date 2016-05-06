drop table if exists resistors;
create table resistors (
  pn integer primary key autoincrement,
  value text not null,
  param text not null,
  desc text not null,
  status text not null,
  rohs text not null,
  datasheet text
);
