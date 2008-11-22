<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="style.css">
<link rel="stylesheet" type="text/css" href="schedule.css">
<script type="test/javascript" src="schedule.js"></script>
<script type="test/javascript" src="mootools.js"></script>
<title>Schedule Planner</title>
</head>
<body style='margin-top:5px;' onload="Init();">
<h3>Spring 2009 Schedule Planner -- Development</h3>
<div id='schedulecontainer'>
</div><!-- mediumcontainer -->
<div id='container'>
	<div id='courseselector'>
		<strong>Add course:</strong><input maxlength=4 size=4 id='tdept' onkeypress='entsub(event);'>
		<input maxlength=3 size=3 id='tcourse' onkeypress='entsub(event);'>
		<BUTTON onclick='courseget.GetCourse(curcor(),"");'>Add</button>
		<br><em>Ex: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NUEN  &nbsp;&nbsp;&nbsp; 101</em>
	</div>
	<div id='coursebrowser'></div>
	<strong>Total Hours: <span id='hours'>0</span></strong>
	<div id='controllerDIV'></div>
</div>

<script type="text/javascript">i
function log(str){return;document.getElementById('log').innerHTML+=str+"<br>";}
</script>
<div id='log' style='position:absolute;right:0px;width:350px;top:0px;bottom:0px;overflow:scroll;'></div>
</body>
</html>
