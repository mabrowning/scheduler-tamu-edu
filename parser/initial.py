#! /usr/bin/python

import pickle
import MySQLdb

db = MySQLdb.connect(user="course",passwd="shoot",db="2009A")
cur = db.cursor()
def create_dept(dept):
	cur.execute("INSERT INTO departments (abbreviation) VALUES ('"+dept+"');")
	cur.execute("SELECT LAST_INSERT_ID();")
	return (dept,cur.fetchone()[0])
def create_course(dept,course):
	cur.execute("INSERT INTO courses (department_id, number) VALUES ("+str(dept)+","+course+");")
	cur.execute("SELECT LAST_INSERT_ID();")
	return (course,cur.fetchone()[0])
def create_prof(dept,prof):
	cur.execute("INSERT INTO profs (department_id, display_name) VALUES ("+str(dept)+", '"+MySQLdb.escape_string(prof)+"');")
	cur.execute("SELECT LAST_INSERT_ID();")
	return cur.fetchone()[0]
def create_section(course,section):
	sql="INSERT INTO sections (course_id, prof_id, number, seats, seats_avail, credit, honors, writing_intensive, description_string, notes"
	for i in range(len(section["tdr"])):
		sql+=", TDR"+str(i)
	sql+=" ) VALUES ("+str(course)+", "+str(section["prof"])+", "+section["section"]+", "+section["totalseats"]+", "+section["availseats"]+", "
	sql+=section["credit"].split(' ')[0]+", " 
	if (section["section"]>=200 and section["section"]<300) or section["section"]==970:
		sql+="1, "
	else:
		sql+="0, "
	if section["section"]>=900:
		sql+="1, "
	else:
		sql+="0, "
	sql+="'"+MySQLdb.escape_string(section["description"])+"', '"+MySQLdb.escape_string(section["notes"])
	for i in section["tdr"]:
		sql+="', '"+i
	sql+="');"
	cur.execute(sql)
f = open("courses.pkl","rb")
sects=pickle.load(f)
depts=pickle.load(f)
courses=pickle.load(f)
f.close()
print "adding departments..."
for de in depts:
	depts[de]=create_dept(depts[de])
print "adding courses..."
for de in courses:
	for co in courses[de]:
		courses[de][co]=create_course(depts[de][1],courses[de][co])
print "adding profs and sections..."
profs={}
for de in sects:
	profs[de]={}
	for co in sects[de]:
		for se in sects[de][co]:
			if(se["prof"] in profs[de]):
				se["prof"]=profs[de][se["prof"]]
			else:
				profs[de][se["prof"]]=create_prof(depts[de][1],se["prof"])
				se["prof"]=profs[de][se["prof"]]
			create_section(courses[de][co][1],se)
