<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
<script>var mousescroll=true;</script>
<script src="schedule.js"></script>
<link rel="stylesheet" type="text/css" href="schedule.css">
<title>Schedule Planner trial</title>
</head>
<body style='margin-top:5px;' onload="Init();">
<h3>Spring 2009 Schedule Planner -- Trial Edition</h3>
Testing
<div id='bigcontainer'>
<div id='mediumcontianer'>
<div id='times'>
<?php 
$start_hour=8;
$last_hour=19;
for($i=8;$i<20;$i++)
{
$j=($i%12);
if($i==0||$i==12)$j="12";
if($i>10)
	$j=$j.":00PM";
else
	$j=$j.":00AM";
echo "<div class='hour' id='".$i."'><span class='hourlabel'>".$j."</span></div>\n";
echo "<div class='halfhour'></div>\n";

}
?>
</div>
<div id='cal'>
<div id='M' class='day'></div>
<div id='T' class='day'></div>
<div id='W' class='day'></div>
<div id='R' class='day'></div>
<div id='F' class='day'></div>
</div>
</div>
</div>
<div id='container'>
<strong>Add course:</strong><input maxlength=4 size=4 id='tdept' onkeypress='entsub(event);'><input maxlength=3 size=3 id='tclass' onkeypress='entsub(event);'>
<BUTTON onclick='GetClass("","");'>Add</button>
<br/><em>Ex: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NUEN  &nbsp;&nbsp;&nbsp; 101</em>
<br/><strong>Total Hours: <span id='hours'>0</span></strong>
<div id='controllerDIV'></div>
</div>

<script>function log(str){document.getElementById('log').innerHTML+=str+"<br/>";}</script>
<div id='log' style='position:absolute;left:810px;width:300px;'></div>
</body>
</html>
