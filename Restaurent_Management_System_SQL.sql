create database project;
use project;
create table menu_card(item_id int primary key,items varchar(50),category varchar(50),price int);
select * from menu_card;
insert into menu_card values(1,'chicken biryani','non-veg',220);
insert into menu_card values(2,'Mutton biryani','non-veg',340);
insert into menu_card values(3,'paneer biryani','veg',180);
insert into menu_card values(4,'veg biryani','veg',120);
create table orders(order_id int auto_increment primary key ,user_name varchar(50),mobile_no varchar(15),
item_name varchar(100),category varchar(50),quality int,price float,total float,order_date date);
select * from orders;
create table cart(item_id int primary key,name varchar(30),category varchar(50),price int,quantity int);
select * from cart;
alter table cart add mobile_no varchar(15);
alter table orders drop primary key;