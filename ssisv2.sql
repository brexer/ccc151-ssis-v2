CREATE DATABASE IF NOT EXISTS ssisv2;
USE ssisv2;

CREATE TABLE IF NOT EXISTS collegedb (
    college_codedb VARCHAR(10) NOT NULL,
    college_namedb VARCHAR(100) NOT NULL,
    PRIMARY KEY (college_codedb)
);

CREATE TABLE IF NOT EXISTS programdb (
    program_codedb VARCHAR(10) NOT NULL,
    program_namedb VARCHAR(100) NOT NULL,
    college_codedb VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY (program_codedb),
    FOREIGN KEY (college_codedb) REFERENCES collegedb (college_codedb) 
        ON DELETE SET NULL ON UPDATE CASCADE
); 

CREATE TABLE IF NOT EXISTS studentdb (
    student_iddb VARCHAR(20) NOT NULL,
    first_namedb VARCHAR(50) NOT NULL,
    last_namedb VARCHAR(50) NOT NULL,
    genderdb VARCHAR(10) NOT NULL,
    year_leveldb VARCHAR(10) NOT NULL,
    program_codedb VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY (student_iddb),
    FOREIGN KEY (program_codedb) REFERENCES programdb (program_codedb) 
        ON DELETE SET NULL ON UPDATE CASCADE
);