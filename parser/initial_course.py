#! /usr/bin/python

import pickle
from scheduler import *
f = open("courses.pkl","rb")
sects=pickle.load(f)
depts=pickle.load(f)
courses=pickle.load(f)
f.close()
print "adding departments..."
for de in depts:
	depts[de]=get_dept_id(depts[de])
print "adding courses..."
for de in courses:
	for co in courses[de]:
		courses[de][co]=get_course_id(depts[de],courses[de][co],sects[de][co][0]["description"])
print "adding profs and sections..."
for de in sects:
	for co in sects[de]:
		for se in sects[de][co]:
			se["prof"]=get_prof_id(se["prof"])
			insert_section(courses[de][co],se,depts[de][0])
