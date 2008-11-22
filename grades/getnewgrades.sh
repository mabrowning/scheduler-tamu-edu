#!/bin/bash

#
sem=$1
[ -z $1 ] && echo "usage: getnew.sh semester Example: ./getnew.sh 2007C"
echo "are you SURE you want to download and add the grades from $1 to the database?"
read var1
for i in AD AG AR BA CA CD ED EL EN EX GB GE GS LA MS SC UT VM
do
	#This hardcodes admissions.tamu.edu becuase my DNS server was slow
	wget "http://165.91.18.172/Registrar/FacultyStaff/Report/TXT_GRDDist/$sem/$i$sem.txt"
done
for filename in *.txt
do
	sed -e '/^[A-Z]/!d' -e '/DEPA.*/d' -e '/UNIV.*/d' < $filename >$filename.new
	./update_grades.py < $filename.new
done
mv *.txt old/
mv *.new parsed/

