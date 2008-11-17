CREATE TABLE IF NOT EXISTS departments(
  id INT(3) AUTO_INCREMENT PRIMARY KEY,
  dept CHAR(4) NOT NULL
);
TRUNCATE TABLE departments;

CREATE TABLE IF NOT EXISTS courses(
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  number INT(3) NOT NULL,
  description_string VARCHAR(1023),
  FOREIGN KEY (department_id) REFERENCES departments (id)
);
TRUNCATE TABLE courses;

CREATE TABLE IF NOT EXISTS profs(
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  display_name VARCHAR(25) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments (id)
);
TRUNCATE TABLE profs;

CREATE TABLE IF NOT EXISTS sections(
  id INT(6) AUTO_INCREMENT PRIMARY KEY,
  course_id INT(5) NOT NULL,
  prof_id INT(5) NOT NULL,
  number INT(3) NOT NULL,
  TDR0 VARCHAR(50) NOT NULL,
  TDR1 VARCHAR(50),
  TDR2 VARCHAR(50),
  TDR3 VARCHAR(50),
  TDR4 VARCHAR(50),
  seats INT(3) NOT NULL,
  seats_avail INT(3) NOT NULL,
  honors INT(1) NOT NULL,
  writing_intensive INT(1) NOT NULL,
  description_string VARCHAR(1023),
  notes VARCHAR(4095),
  credit INT(1) NOT NULL,
  FOREIGN KEY (course_id) REFERENCES courses (id),
  FOREIGN KEY (prof_id) REFERENCES profs (id)
);
TRUNCATE TABLE sections;
