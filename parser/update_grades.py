#! /usr/bin/python
from scheduler import *
import sys
fields={}
fields["department_id"]=(0,4)
fields["course_id"]=(5,3)
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
	values["course_id"]=  get_course_id(values["department_id"],values["course_id"])
	values["prof_id"]=      get_prof_id(values["department_id"],values["prof_id"])
	for f in fields:
			values[f]=str(int(values[f]))
	if(values['TOT']=='0'):
		continue
	insert_grade(values)
