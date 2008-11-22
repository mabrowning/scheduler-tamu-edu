#! /usr/bin/python

import pickle
from scheduler import *
f = open("courses.pkl","rb")
sects=pickle.load(f)
depts=pickle.load(f)
courses=pickle.load(f)
semester=pickle.load(f)
f.close()
print "updating profs and sections..."
for de in sects:
	for co in sects[de]:
		for se in sects[de][co]:
			update_section(courses[de][co],se,depts[de])
