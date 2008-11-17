#! /usr/bin/python

import pickle
import MySQLdb

db = MySQLdb.connect(user="course",passwd="shoot",db="2009A")
cur = db.cursor()

def append(dept,course,section):
	sql="INSERT INTO "+dept+course+" ( section,prof,descrip,credit,seats,seatsleft"
	for i in range(len(section["tdr"])):
		sql+=",TDR"+str(i)
	sql+=" ) VALUES ('"
	sql+=section["section"]+"','"
	sql+=MySQLdb.escape_string(section["prof"])+"','"
	sql+=MySQLdb.escape_string(section["description"])+"','"
	sql+=section["credit"]+"','"
	sql+=section["totalseats"]+"','"
	sql+=section["availseats"]
	for i in section["tdr"]:
		sql+="','"+i	
	sql+="');"
	cur.execute(sql)

f = open("courses.pkl","rb")
sects=pickle.load(f)
depts=pickle.load(f)
courses=pickle.load(f)
f.close()
print "adding fresh depts, profs, courses and sections to empty database"

for de in sects:
	for co in sects[de]:
		create(depts[de],courses[de][co])
print "updating database contents"
for de in sects:
	for co in sects[de]:
		for se in sects[de][co]:
			append(depts[de],courses[de][co],se)
