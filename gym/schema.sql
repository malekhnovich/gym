drop table if exists Member ;
drop table if exists Membership;
drop table if exists Benefit ;
drop table if exists MembershipBenefits;
drop table if exists Class ;
drop table if exists Exercise;
drop table if exists Room ;
drop table if exists Instructor;
drop table if exists FullTimeInstructor ;
drop table if exists ExternalInstructor;

create table Member (mID int NOT NULL, name varchar(20), isActive boolean, mbrshipID int, PRIMARY KEY(mID), FOREIGN KEY(mbrshipID) REFERENCES Membership(id));
create table Membership (id int NOT NULL, name varchar(20) ,fee float,PRIMARY KEY(id));
create table MembershipBenefits(mbrshipID int NOT NULL, benefitID int NOT NULL, FOREIGN KEY(mbrshipID) REFERENCES Membership(id), FOREIGN KEY(benefitID) REFERENCES Benefit(id));
create table Benefit (id int NOT NULL, name varchar(20), description varchar(20),PRIMARY KEY(id));
Create table Class (instructorID int NOT NULL, startTime time,duration int,PRIMARY KEY(instructorID));
create table Exercise(id int NOT NULL, name varchar(20), description varchar(20), PRIMARY KEY(id));
create table Room(building varchar(20) NOT NULL , room varchar(20) NOT NULL, capacity int,PRIMARY KEY(building,room));
create table Instructor(id int NOT NULL AUTOINCREMENT, name varchar(20), PRIMARY KEY(id));
create table FullTimeInstructor(id int NOT NULL, name varchar(20), salary float,PRIMARY KEY(id));
create table ExternalInstructor(id int NOT NULL, name varchar(20), hoursTaught int, hourlywage float, PRIMARY KEY(id));


insert into Member values(1, 'steve', "TRUE", 1001);

insert into Member values(2,'pat',"FALSE", 1002);

-- SET SQL_SAFE_UPDATES = 0;
insert into Member values(3,'nicole',"TRUE", 1003);
insert into Member values(4,'john', "TRUE", 1003);
Insert into Member values(5, 'joe', "TRUE",  1004);

insert into Membership values (1001,'Student', 10);
insert into Membership values(1002, 'Senior', 10);
insert into Membership values(1003,'Gold',20);
insert into Membership values(1004,'Platinum',50);



Insert into MembershipBenefits values(1001,2001);
Insert into MembershipBenefits values(1002,2001);
Insert into MembershipBenefits values(1003,2001);
Insert into MembershipBenefits values(1004,2001);
Insert into MembershipBenefits values(1002,2002);
Insert into MembershipBenefits values(1004,2002);
Insert into MembershipBenefits values(1004,2003);

insert into Benefit values (2001,'locker', 'locker room access');
insert into Benefit values (2002,'smoothie', 'smoothie bar access');
insert into Benefit values (2003,'PT','personal trainer');

Insert into Class values(1,'12:00:00',1);
Insert into Class values(2,'10:00:00',2);
Insert into Class values(3,'12:00:00',1);
Insert into Class values(4,'10:00:00',1);


Insert into Exercise values(1, 'bicep curl', 'hold dumbbell in hand and curl it focusing on the bicep muscle');
Insert into Exercise values(2, 'Dips', 'rise up over the bars and bend elbow until level with bar, focus on triceps');
Insert into Exercise values(3,'chest bench press','hold bar up and lower until bar hits chest and then rise back up');


Insert into Room values('Calhoun Hall', '203A', 30);
Insert into Room values('Jones Hall', '113B', 20);
Insert into Room values('Julio Hall', '24C', 54);


Insert into Instructor values(1,'Tom Hall');
Insert into Instructor values(2, 'Jones Jack');
Insert into Instructor values(3,'Cory Smith');


Insert into FullTimeInstructor values(1,'Tom Hall',50000);
Insert into ExternalInstructor values(2,'Jones Jack',30,57);
Insert into ExternalInstructor values(3,'Cory Smith',60,23);

