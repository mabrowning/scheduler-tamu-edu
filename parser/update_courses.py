#! /usr/bin/python

import pickle
import MySQLdb

db = MySQLdb.connect(user="course",passwd="shoot",db="schedule")
cur = db.cursor()
def get_dept_id(dept):
	cur.execute("SELECT id FROM departments WHERE dept='"+dept+"';")
	return str(cur.fetchone()[0])
def get_course_id(dept,course):
	cur.execute("SELECT courses.id FROM departments,courses WHERE number="+course+" AND dept='"+dept+"' AND department_id=departments.id;")
	return str(cur.fetchone()[0])
def update_prof(dept,prof):
	cur.execute("SELECT profs.id FROM departments,profs WHERE dept='"+dept+"' AND display_name='"+MySQLdb.escape_string(prof)+"';")	
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		cur.execute("INSERT INTO profs (department_id,display_name) VALUES( "+get_dept_id(dept)+", '"+MySQLdb.escape_string(prof)+"');")
		cur.execute("SELECT LAST_INSERT_ID();")
		return cur.fetchone()[0]
def update_section(course,section,dept):
	sql="UPDATE sections SET prof_id="+str(section["prof"])+", seats="+section["totalseats"]+", seats_avail="+section["availseats"]+", "
	sql+="description_string='"+MySQLdb.escape_string(section["description"])+"', notes='"+MySQLdb.escape_string(section["notes"].strip("\n"))
	for i in range(len(section["tdr"])):
		sql+="', TDR"+str(i)+"='"+section["tdr"][i]
	sql+="' WHERE course_id="+get_course_id(dept,course)+" AND number="+section["section"]+";"
	cur.execute(sql)
f = open("courses.pkl","rb")
sects=pickle.load(f)
depts=pickle.load(f)
courses=pickle.load(f)
f.close()
print "updating profs and sections..."
profs={}
for de in sects:
	profs[de]={}
	for co in sects[de]:
		for se in sects[de][co]:
			if(se["prof"] in profs[de]):
				se["prof"]=profs[de][se["prof"]]
			else:
				profs[de][se["prof"]]=update_prof(depts[de],se["prof"])
				se["prof"]=profs[de][se["prof"]]
			update_section(courses[de][co],se,depts[de])
