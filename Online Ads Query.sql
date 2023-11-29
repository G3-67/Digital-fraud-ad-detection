create database OnlineAds

create table Register(Regid int primary Key auto_increment not null, rname varchar(50), gender varchar(50),contact varchar(50),email varchar(50),Address varchar(250), city varchar(50),role varchar(50),uname varchar(50),password varchar(50))

create table postads(postid int primary Key auto_increment not null, ownername varchar(50), contact varchar(50), vname varchar(50), vtype varchar(50), vnumber varchar(50), vmodelno varchar(50), vmodelname varchar(50), postalcode varchar(50), address varchar(250), noofowner varchar(50)  , description varchar(250), price varchar(50), video varchar(250))

create table Vehicledetails(ownername varchar(50), vnumber varchar(50), vname varchar(50),  vmodelno varchar(50),vmodelname varchar(50), pincode varchar(50))

create table feedback(cdate varchar(50),clientname varchar(50),prodname varchar(50),prodtype varchar(50), feedback varchar(50), description varchar(250))

insert into Vehicledetails values('Siva','TN1234','Honda','10','Asta','123456')

create table prebook(ownername varchar(50),vnumber varchar(50),vname varchar(50),username varchar(50),contact varchar(50),email varchar(50))