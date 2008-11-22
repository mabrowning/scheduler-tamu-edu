#! /usr/bin/python

import urllib
from HTMLParser import HTMLParser
import pickle

class CoursesHTMLParser(HTMLParser):
	"This handles HTML pages from courses.tamu.edu and extracts the desired link payloads"
	def __init__(self,target="viewcourses"):
		HTMLParser.__init__(self)
		self.target=target
		self.flag=False
		self.payload={}
	def handle_starttag(self, tag, attrs):
		if(tag=="a"):
			if(attrs[0][1].capitalize().find(self.target.capitalize())>-1):
				self.flag=True
				self.tempx=attrs[0][1].rpartition("&")[0].rpartition("=")[2]
	def handle_data(self, data):
		if(self.flag):
			self.payload[self.tempx]=data.split(" ")[2]
	def handle_endtag(self, tag):
		if(self.flag):
			self.flag=False
class SectionHTMLParser(HTMLParser):
	"This handles HTML pages from courses.tamu.edu and extracts the section attributes"
	def __init__(self):
		HTMLParser.__init__(self)
		self.sections=[]
		self.temp={}
		self.temp["tdr"]=[]
		self.temp["notes"]=""
		self.tagflag=""
		self.strongflag=""
		self.secnum="0"
		self.diddata=False
		self.noteflag=False
	def handle_starttag(self, tag, attrs):
		args=self.handle_args(attrs)
		if(tag=="td" and "class" in args and args["class"]=="sectionheading"):
			if(self.secnum!="0"):
				self.sections.append(self.temp)
				self.temp={}
				self.temp["tdr"]=[]
				self.temp["notes"]=""
				self.diddata=False
				self.noteflag=False
			self.strongflag="description"
		if(tag=="strong"):
			self.tagflag="strong"
		if(tag=="td" and self.diddata):
			self.diddata=False
			self.noteflag=True
		if(self.noteflag and tag=="a"):
			self.temp["notes"]+='<a target="new" href="'+args["href"]+'">'
		if(self.noteflag and tag=="br"):
			self.temp["notes"]+="\n"
	def handle_data(self, data):
		if self.strongflag == "credit":
			self.temp[self.strongflag]=data.strip("CR \r\n")
			self.strongflag=""
		elif self.strongflag=="description":
			ds=data.split("-")[1:]
			data=""
			for i in ds:
				data+=i.strip(" \r\n")+" - "
			self.secnum=data.split(" ")[0].strip()
			self.temp["section"]=self.secnum
			self.temp["description"]=data.strip("0123456789- \r\n")
			self.strongflag=""
		elif self.strongflag=="tdr":
			tdr=data.split(";")[-1:][0].strip(" \t\r\n")
			if tdr!="":
				self.temp["tdr"].append(tdr)
			self.noteflag=False
		elif self.strongflag != "":
			self.temp[self.strongflag]=data.strip(" \r\n")
			self.strongflag=""
			self.diddata=True
		elif(self.tagflag=="strong"):
			if data=="Instructor:":
				self.strongflag="prof"
			elif data=="Total Seats:":
				self.strongflag="totalseats"
			elif data=="Available Seats":
				self.strongflag="availseats"
			elif data=="Credits:":
				self.strongflag="credit"
			elif data=="Locations:":
				self.strongflag="tdr"
		elif(self.noteflag):
			self.temp["notes"]+=data.strip(" \t\r\n").replace("\r\n"," ")
	
		self.tagflag="None"
	def handle_endtag(self, tag):
		if (tag=="td" and self.strongflag=="tdr"):
			self.strongflag=""
		if tag=="table":
			self.sections.append(self.temp)
		if (tag=="a" and self.noteflag):
			self.temp["notes"]+="</a>"
		self.tagflag=="None"
	def handle_args(self, attrs):
		args={}
		for i in attrs:
			args[i[0]]=i[1]
		return args
def getdepts(x):
	"This returns a dictionary of DEPT:base64_codes pairs corresponding the department list"
	
	dept=CoursesHTMLParser("viewcourses")
	dept.feed(urllib.urlopen("http://courses.tamu.edu/viewdepartments.aspx?x="+x).read())
	return dept.payload
def getcourses(x):
	"This returns a dictionary of DEPT:base64_codes pairs corresponding the course list in a particular department"
	
	dept=CoursesHTMLParser("viewsections")
	dept.feed(urllib.urlopen("http://courses.tamu.edu/viewcourses.aspx?x="+x).read())
	return dept.payload
def getsects(x):
	"This returns a dictionary containing all the sections and their attributes in a course"

	section=SectionHTMLParser()
	section.feed(urllib.urlopen("http://courses.tamu.edu/viewsections_pf.aspx?x="+x).read().replace("&","AND").replace("</A<","</A><").replace("<A <","<"))
	# The replace needs to be done because HTMLParser stops a 'handle_data()' response at an '&'
	# and some course descriptions have '&' in them
	return section.sections

print "Getting the department list..."
#depts=getdepts("K22FPSHrTqwkOV9VFP/yQw==")
depts=getdepts("bqPHRw6nsa27Rp2YPdL5qw==")
print depts
courses={}
sects={}
# in the following code, de and co are the Base64 keys. 
# depts[de] contains the strings corresponding to the keys
# courses[de][co] contains the course number in department with key 'de' associated with key 'co'

# sects[de][co] contains not a string, but an array of associatiave arrays with the following fields
# ["section"]     -> section number
# ["description"] -> course description
# ["totalseats"]  -> total seats in section
# ["availseats"]  -> available seats in the section
# ["prof"]   -> the instructor teaching it. duh ;)
# ["credit"] -> string containing the number of credits; format is "%d"
# ["tdr"]    -> a simple array of strings containing the time, day, room strings
# ["notes"]  -> contains notes about the section (like, is it honors?, et c)


for de in depts:
	print depts[de]
	sects[de]={}
	courses[de]=getcourses(de)
	for co in courses[de]:
		print "   "+courses[de][co]+" ",
		sects[de][co]=getsects(co)
		
# save this shit! It takes a long time to download, what if we crash in the next step?
f = open("courses.pkl","wb")
pickle.dump(sects, f)
pickle.dump(depts, f)
pickle.dump(courses, f)
pickle.dump("2009A",f)
f.close()
print "saved everything to courses.pkl!  Make sure to run ./interpret.py"

