<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
<script>var mousescroll=true;</script>
<script src="schedule.js"></script>
<link rel="stylesheet" type="text/css" href="schedule.css">
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
		<BUTTON onclick='GetCourse("","");'>Add</button>
		<br/><em>Ex: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NUEN  &nbsp;&nbsp;&nbsp; 101</em>

	<div id='coursebrowser'><script type='text/javascript'>browser=new Browser(); </script></div>
	<strong>Total Hours: <span id='hours'>0</span></strong>
	<div id='controllerDIV'></div>
</div>

<script>function log(str){document.getElementById('log').innerHTML+=str+"<br/>";}</script>
<div id='log' style='position:absolute;right:300px;width:300px;top:0px;height:800px;overflow:scroll;'></div>
</body>
</html>
