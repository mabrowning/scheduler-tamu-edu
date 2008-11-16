<?php
$name=$_REQUEST["name"];
$user=$_REQUEST["user"];
$courses=explode(",",$_REQUEST["courses"]);
$sections=explode(",",$_REQUEST["sections"]);
if($name)
{
	$conn=mysql_connect('localhost','course','shoot')or die('Could not connect: ' . mysql_error());
	mysql_select_db('users')or die('Could not select database');
	$user=mysql_real_escape_string($user);
	$user = str_ireplace(".", "", $user);
	$name=mysql_real_escape_string($name);
	$name = str_ireplace(".", "", $name);
	$sql="SELECT name FROM saves WHERE name='$name' AND user='$user'";
	$result=mysql_query($sql)or die('Query failed: ' . mysql_error());
	if(mysql_num_rows($result)==0)
	{
		echo"Creating new save file: ".$name."...\r\n";
		$sql="INSERT INTO saves (name,user) VALUES ('$name','$user')";
		$result=mysql_query($sql)or die('Query failed: ' . mysql_error());
		$sql="CREATE TABLE save$user$name (course TEXT, section TEXT)";
		$result=mysql_query($sql)or die('Error Creating Save file; Query failed: ' . mysql_error());
		echo "Created save file save$user$name";
	}
	else
	{
		echo("Overwriting old save file: ".$name."...\r\n");
		$sql="DROP TABLE save$user$name";
		$result=mysql_query($sql)or die('Error removing old save file; Query failed: ' . mysql_error());
		$sql="CREATE TABLE save$user$name(course TEXT, section TEXT)";
		$result=mysql_query($sql)or die('Error creating new save file; Query failed: ' . mysql_error());
	}
	for($i=0;$i<count($courses);$i++)
	{
		$sql="INSERT INTO save$user$name(course, section) VALUES ('".$courses[$i]."','".$sections[$i]."')";
		$result=mysql_query($sql)or die('Error inserting save values; Query failed: ' . mysql_error());
	}
	mysql_close($conn);
}
else
{
	echo "NOT saved";
}


?>
