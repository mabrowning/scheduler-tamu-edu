CREATE TABLE IF NOT EXISTS departments(
  id INT(3) AUTO_INCREMENT PRIMARY KEY,
  dept CHAR(4) NOT NULL
);

CREATE TABLE IF NOT EXISTS allcourses(
  id INT(7) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  number INT(3) NOT NULL,
  description_string VARCHAR(1023),
  FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE IF NOT EXISTS profs(
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  display_name VARCHAR(25) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE IF NOT EXISTS grades(
  id INT(7) AUTO_INCREMENT PRIMARY KEY,
  department_id INT(3) NOT NULL,
  prof_id INT(5) NOT NULL,
  course_id INT(7) NOT NULL,
  section_number INT(3) NOT NULL,
  A INT(3) NOT NULL,
  B INT(3) NOT NULL,
  C INT(3) NOT NULL,
  D INT(3) NOT NULL,
  F INT(3) NOT NULL,
  TOT INT(3) NOT NULL
  FOREIGN KEY (department_id) REFERENCES departments (id)
  FOREIGN KEY (prof_id) REFERENCES profs (id)
  FOREIGN KEY (course_id) REFERENCES allcourses (id)
);

CREATE TABLE IF NOT EXISTS courses(
  id INT(5) AUTO_INCREMENT PRIMARY KEY,
  course_id INT(7) NOT NULL,
  semester CHAR(5) NOT NULL,
  FOREIGN KEY (course_id) REFERENCES allcourses (id)
);

CREATE TABLE IF NOT EXISTS sections(
  id INT(6) AUTO_INCREMENT PRIMARY KEY,
  course_id INT(5) NOT NULL,
  prof_id INT(5) NOT NULL,
  semester CHAR(5) NOT NULL,
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
