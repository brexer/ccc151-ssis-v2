CREATE DATABASE IF NOT EXISTS ssisv2;
USE ssisv2;
CREATE TABLE college (
   college_code varchar(10) NOT NULL,
   college_name varchar(100) NOT NULL,
   PRIMARY KEY (college_code)
 )
 
CREATE TABLE program (
   program_code varchar(10) NOT NULL,
   program_name varchar(100) NOT NULL,
   college_code varchar(10) DEFAULT NULL,
   PRIMARY KEY (program_code),
	FOREIGN KEY (college_code) REFERENCES college (college_code) ON DELETE SET NULL ON UPDATE CASCADE
 ) 
 
CREATE TABLE student (
   student_id varchar(20) NOT NULL,
   first_name varchar(50) NOT NULL,
   last_name varchar(50) NOT NULL,
   gender varchar(10) NOT NULL,
   year_level int NOT NULL,
   program_code varchar(10) DEFAULT NULL,
   PRIMARY KEY (student_id),
   FOREIGN KEY (program_code) REFERENCES program (program_code) ON DELETE SET NULL ON UPDATE CASCADE
 )