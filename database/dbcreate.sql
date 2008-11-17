   --CREATE DATABASE 2009A;
   --GRANT ALL ON 2009A.* TO 'courses'@'localhost';
   --USE 2009A;
CREATE TABLE departments (
  id INT(3) AUTO_INCREMENT PRIMARY KEY,
  abbreviation CHAR(4) NOT NULL
);

CREATE TABLE courses (
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  number INT(3) NOT NULL,
  name VARCHAR(75) NOT NULL,
  description_string VARCHAR(1000),
  FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE profs (
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  display_name VARCHAR(25) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE sections (
  id INT(6) AUTO_INCREMENT PRIMARY KEY,
  course_id INT(5) NOT NULL,
  prof_id INT(5) NOT NULL,
  number INT(3) NOT NULL,
  time_string VARCHAR(100) NOT NULL,
  seats INT(3) NOT NULL,
  seats_filled INT(3) NOT NULL,
  honors INT(1) NOT NULL,
  writing_intensive INT(1) NOT NULL,
  description_string VARCHAR(1023),
  credit INT(1) NOT NULL,
  FOREIGN KEY (course_id) REFERENCES courses (id),
  FOREIGN KEY (prof_id) REFERENCES profs (id)
);
