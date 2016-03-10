
# users database table
create table users(
	name char(30) not null,
	username char(30) primary key not null,
	password char(70) not null,
	rollno integer not null,
	address char(30) not null,
	roomno integer not null,
	laundryno integer not null,
	batch char(10) not null,
	branch char(10) not null
);

# rooms database table
create table rooms(
	roomno integer not null,
	name char(30) not null,
	username char(30) not null,
	rollno integer not null,
	branch char(10) not null
);

# admin database table
create table admin(
	name char(30) not null,
	username char(30) primary key not null,
	password char(70) not null
);

