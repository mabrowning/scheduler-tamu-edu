<?php
include('settings.php');
$conn=mysql_connect($mysql_host,$mysql_user,$mysql_pass)or die('Could not connect: ' . mysql_error());
mysql_select_db($mysql_schema)or die('Could not select database');


$dept=mysql_real_escape_string($_REQUEST["dept"]);
$number=mysql_real_escape_string($_REQUEST["number"]);
$semester=mysql_real_escape_string($_REQUEST["semester"]);


$JSON=Array();
$sql="SELECT sections.number, TDR0, TDR1, TDR2, TDR3, TDR4, seats, seats_available, sections.description_string, notes, credit, display_name ";
$sql.="FROM sections,courses,allcourses,departments,profs WHERE allcourses.number=".$number." AND dept='".$dept."' AND ";
$sql.="sections.semester='".$semester."' AND sections.course_id=courses.id AND courses.course_id=allcourses.id AND ";
$sql.="allcourses.department_id=departments.id AND profs.department_id=departments.id AND prof_id=profs.id";
print $sql;
$result=mysql_query($sql)or die('Query failed: ' . mysql_error());
while($JSON[]=mysql_fetch_array($result,MYSQL_ASSOC));
mysql_close($conn);

?>
