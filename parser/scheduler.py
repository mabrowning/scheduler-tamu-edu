import MySQLdb

db = MySQLdb.connect(user="course",passwd="shoot",db="schedule")
cur = db.cursor()

def get_dept_id(dept):
	cur.execute("SELECT id FROM departments WHERE dept='"+str(dept)+"';")
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		cur.execute("INSERT INTO departments (dept) VALUES( '"+dept+"' );")
		cur.execute("SELECT LAST_INSERT_ID();")
		id=cur.fetchone()[0]
		print "Adding new department: "+dept+" with id: "+str(id)
		return id
def get_course_id(dept,course,description=""):
	cur.execute("SELECT id FROM allcourses WHERE number="+str(course)+" AND department_id="+str(dept)+";")
	id=cur.fetchone()
	if(id):
		return id[0]
	else:
		cur.execute("INSERT INTO allcourses (number,department_id,description_string) VALUES( "+course+", "+str(dept)+", '"+MySQLdb.escape_string(description)+"');")
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
def insert_section(course,section,dept,semester):
	cur.execute("INSERT INTO courses (semester,course_id) VALUES ( '"+semester+"', "+str(course)+");")
	cur.execute("SELECT LAST_INSERT_ID();")
	course=cur.fetchone()[0]
	sql="INSERT INTO sections (course_id, prof_id, number, seats, seats_avail, credit, honors, writing_intensive, description_string, notes"
	for i in range(len(section["tdr"])):
		sql+=", TDR"+str(i)
	sql+=" ) VALUES ("+str(course)+", "+str(section["prof"])+", "+section["section"]+", "+section["totalseats"]+", "+section["availseats"]+", "
	sql+=section["credit"].split(' ')[0]+", " 
	if ((int(section["section"])>=200 and int(section["section"])<300) or int(section["section"])==970):
		sql+="1, "
	else:
		sql+="0, "
	if int(section["section"])>=900:
		sql+="1, "
	else:
		sql+="0, "
	sql+="'"+MySQLdb.escape_string(section["description"])+"', '"+MySQLdb.escape_string(section["notes"].strip("\n"))
	for i in section["tdr"]:
		sql+="', '"+i
	sql+="');"
	cur.execute(sql)
def update_section(course,section,dept,semester):
	dept_id=get_dept_id(dept)
	sql="SELECT sections.id FROM sections,courses,allcourses WHERE courses.course_id=allcourses.id "+\
	"AND department_id="+str(dept_id)+" AND sections.number="+str(section["section"])+" AND allcourses.number="+str(course)+" AND semester='"+semester+"';"
	cur.execute(sql)
	id=cur.fetchone()[0]
	section["prof"]=get_prof_id(dept_id,section["prof"])
	sql="UPDATE sections SET prof_id="+str(section["prof"])+", seats="+section["totalseats"]+", seats_avail="+section["availseats"]+", "
	sql+="description_string='"+MySQLdb.escape_string(section["description"])+"', notes='"+MySQLdb.escape_string(section["notes"].strip("\n"))
	for i in range(len(section["tdr"])):
		sql+="', TDR"+str(i)+"='"+section["tdr"][i]
	sql+="' WHERE id="+str(id)+";"
	cur.execute(sql)
