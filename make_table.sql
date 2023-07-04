-- Schema  PROJECT
DROP SCHEMA IF EXISTS PROJECT;

-- Schema  PROJECT
CREATE SCHEMA IF NOT EXISTS PROJECT DEFAULT CHARACTER SET utf8 ;
USE PROJECT;

-- Table  PROJECT.STUDENT
DROP TABLE IF EXISTS PROJECT.STUDENT ;

CREATE TABLE IF NOT EXISTS PROJECT.STUDENT (
    studentID INT NOT NULL PRIMARY KEY,
    student_name VARCHAR(45) NOT NULL,
    student_grade FLOAT NOT NULL)
;


-- Table  PROJECT.INSTRUCTOR
DROP TABLE IF EXISTS PROJECT.INSTRUCTOR ;

CREATE TABLE IF NOT EXISTS PROJECT.INSTRUCTOR(
    instructorID INT PRIMARY KEY,
    instructorName VARCHAR(45) NOT NULL,
    deptName VARCHAR(10) NOT NULL)
;

-- Table  PROJECT.COURSE
DROP TABLE IF EXISTS PROJECT.COURSE;

-- foreign key: primary key
-- ref_instructorID: INSTRUCTOR.instructorID
CREATE TABLE IF NOT EXISTS PROJECT.COURSE(
    courseID VARCHAR(10) NOT NULL,
    classID INT NOT NULL, 
	deptName VARCHAR(10) NOT NULL,
    title VARCHAR(45) NOT NULL,
    courseDate VARCHAR(30),
    ref_instructorID INT NOT NULL,
    credit FLOAT NULL,
    CONSTRAINT COURSE PRIMARY KEY (courseID, classID, deptName),
    FOREIGN KEY (ref_instructorID) REFERENCES PROJECT.INSTRUCTOR (instructorID))
;


-- Table  PROJECT.TAKES
DROP TABLE IF EXISTS  PROJECT.TAKES;

-- TAKES 규칙: 동일한 수업 불가, 동일한 시간대 수업 불가

-- foreign key: primary key
-- ref_studentID : STUDENT.studentID
-- ref_courseID, classID, deptName: COURSE.courseID, COURSE.classID, COURSE.deptName
-- ref_instructorID: INSTRUCTOR.instructorID

CREATE TABLE IF NOT EXISTS PROJECT.TAKES(
    num INT AUTO_INCREMENT PRIMARY KEY,
    ref_studentID INT NOT NULL,
    ref_instructorID INT,
    ref_courseID VARCHAR(10) NOT NULL,
    ref_classID INT NOT NULL,
    ref_deptName VARCHAR(10) NOT NULL,
    FOREIGN KEY (ref_studentID) REFERENCES PROJECT.STUDENT (studentID),
    FOREIGN KEY (ref_courseID, ref_classID, ref_deptName) REFERENCES PROJECT.COURSE (courseID, classID, deptName),
    FOREIGN KEY (ref_instructorID) REFERENCES PROJECT.INSTRUCTOR (instructorID))
;
