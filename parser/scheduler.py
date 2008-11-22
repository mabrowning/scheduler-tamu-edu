import MySQLdb

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
	cur.execute("SELECT id FROM allcourses WHERE number="+course+" AND department_id="+str(dept)+";")
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		cur.execute("INSERT INTO allcourses (number,department_id) VALUES( "+course+", "+str(dept)+" );")
		cur.execute("SELECT LAST_INSERT_ID();")
		id=cur.fetchone()[0]
		print "Adding new course: "+course+" with id: "+str(id)
		return id
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
def insert_grade(A):
	cur.execute("INSERT INTO grades ("+', '.join(A)+") VALUES ("+', '.join(["%s" % x for x in A.values()])+");")
