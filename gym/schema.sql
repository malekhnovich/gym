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

Create table Class (classId int NOT NULL, instructorID int NOT NULL, startTime time,duration int, exerciseID int NOT NULL ,  buildingName Varchar(20) NOT NULL,roomID int NOT NULL,FOREIGN KEY(instructorID) REFERENCES Instructor(id), FOREIGN KEY(exerciseID) REFERENCES Exercise(id), FOREIGN KEY(roomID) REFERENCES Room(roomId), FOREIGN KEY(buildingName) REFERENCES Room(buildingName), PRIMARY KEY(classId));


create table Exercise(id int NOT NULL, name varchar(20), description varchar(20), PRIMARY KEY(id));



create table Room(buildingName varchar(20) NOT NULL , roomID int  NOT NULL, capacity int,PRIMARY KEY(buildingName,roomID));

create table Instructor(id int NOT NULL, name varchar(20), PRIMARY KEY(id));

create table FullTimeInstructor(id int NOT NULL, name varchar(20), salary float,PRIMARY KEY(id));

create table ExternalInstructor(id int NOT NULL, name varchar(20), hoursTaught int, hourlywage float, PRIMARY KEY(id));

Create table Enrolled(id int NOT NULL, classId int NOT NULL, FOREIGN KEY(id) REFERENCES Member(MID), FOREIGN KEY(classID) REFERENCES Class(classId));


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

-- select c.buildingName, c.startTime, i.id,i.name from Instructor i
--   join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id;

select count(*) from Enrolled where classId =2;

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

Insert into Class values(1,1,'12:00:00',1,1,'Calhoun Hall',203);
Insert into Class values(2,2,'10:00:00',2,2,'Calhoun Hall',203);
Insert into Class values(3,3,'12:00:00',1,3,'Julio Hall',124);
Insert into Class values(4,4,'10:00:00',1,4,'Calhoun Hall',203);


Insert into Exercise values(1, 'bicep curl', 'hold dumbbell in hand and curl it focusing on the bicep muscle');
Insert into Exercise values(2, 'Dips', 'rise up over the bars and bend elbow until level with bar, focus on triceps');
Insert into Exercise values(3,'chest bench press','hold bar up and lower until bar hits chest and then rise back up');
Insert into Exercise values(4,'shoulder press','sit and lift dumbells above shoulders and back down');


Insert into Room values('Calhoun Hall', 203, 30);
Insert into Room values('Jones Hall', 302, 20);
Insert into Room values('Julio Hall', 124, 54);


Insert into Instructor values(1,'Tom Hall');
Insert into Instructor values(2, 'Jones Jack');
Insert into Instructor values(3,'Cory Smith');


Insert into FullTimeInstructor values(1,'Tom Hall',50000);
Insert into ExternalInstructor values(2,'Jones Jack',30,57);
Insert into ExternalInstructor values(3,'Cory Smith',60,23);


Insert into Enrolled values(1,1);
insert into Enrolled values(1,2);