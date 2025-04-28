CREATE DATABASE IF NOT EXISTS ssisfinal;
USE ssisfinal;

CREATE TABLE colleges (
    code VARCHAR(8) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE programs (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    college_code VARCHAR(8),
    FOREIGN KEY (college_code) REFERENCES colleges(code) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE students (
    id VARCHAR(9) PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    year_level ENUM('First Year', 'Second Year', 'Third Year', 'Fourth Year') NOT NULL,
    program_code VARCHAR(10),
    FOREIGN KEY (program_code) REFERENCES programs(code) ON DELETE SET NULL ON UPDATE CASCADE
);
