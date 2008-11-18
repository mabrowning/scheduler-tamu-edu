#! /usr/bin/python

import MySQLdb
import sys

db = MySQLdb.connect(user="course",passwd="shoot",db="schedule")
cur = db.cursor()

def get_dept_id(dept):
	cur.execute("SELECT id FROM departments WHERE dept='"+dept+"';")
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		cur.execute("INSERT INTO departments (dept) VALUES( '"+dept+"' );")
		cur.execute("SELECT LAST_INSERT_ID();")
		id=cur.fetchone()[0]
		print "Adding new department: "+dept+" with id: "+str(id)
		return id
def get_course_id(dept,course):
	cur.execute("SELECT courses.id FROM departments,courses WHERE number="+course+" AND dept='"+dept+"' AND department_id=departments.id;")
	return str(cur.fetchone()[0])
def get_prof_id(dept,prof):
	cur.execute("SELECT id FROM profs WHERE department_id='"+str(dept)+"' AND display_name='"+MySQLdb.escape_string(prof)+"';")	
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		print "Adding new prof: "+prof+" to department_id: "+str(dept)
		cur.execute("INSERT INTO profs (department_id,display_name) VALUES( "+str(dept)+", '"+MySQLdb.escape_string(prof)+"');")
		cur.execute("SELECT LAST_INSERT_ID();")
		return cur.fetchone()[0]
def insert_grade(department_id,prof_id,course_number,section_number,A,B,C,D,F,TOT):
	cur.execute("INSERT INTO grades (department_id,prof_id,course_number,section_number,A,B,C,D,F,TOT) VALUES "+\
		"("+department_id+", "+prof_id+", "+course_number+", "+section_number+", "+A+", "+B+", "+C+", "+D+", "+F+", "+TOT+");")
fields={}
fields["department_id"]=(0,4)
fields["course_number"]=(5,3)
fields["section_number"]=(9,3)
fields["A"]=(18,7)
fields["B"]=(26,7)
fields["C"]=(34,7)
fields["D"]=(42,7)
fields["F"]=(50,7)
fields["TOT"]=(58,6)
fields["prof_id"]=(108,30)
for line in sys.stdin:
	line=line.strip(" \r\n")
	values={}
	for f in fields:
		values[f]=line[fields[f][0]:sum(fields[f])]
		if(values[f].strip(" ")==''):
			values[f]='0'
	if(values["prof_id"]=='0'):
		continue
	values["department_id"]=get_dept_id(values["department_id"])
	values["prof_id"]=get_prof_id(values["department_id"],values["prof_id"])
	for f in fields:
			values[f]=str(int(values[f]))
	if(values['TOT']=='0'):
		continue
	insert_grade(**values)
