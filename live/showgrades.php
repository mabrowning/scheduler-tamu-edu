<?php
$dept=strtoupper($_GET["dept"]);
$course=$_GET["course"];
$prof=strtoupper($_GET["prof"]);
$semester=$_GET["semester"];
$color=$_GET["color"];
$target="";
if($course)
	$target.= " course='$course'";
if($course and $prof)
	$target.= " AND";
if($prof)
	$target.= " prof LIKE '%$prof%'";
if($semester and $prof)
	$target.= " AND";
if($semester)
	$target.= " semester='$semester'";

include ("/jpgraph/jpgraph.php");
$conn=mysql_connect('localhost','course','shoot')or die('Could not connect: ' . mysql_error());
mysql_select_db('TAMUGRADES')or die('Could not select database');

$sql="SELECT * FROM $dept WHERE $target";
$result=mysql_query($sql)or errormessage(mysql_error(),$color);
$A=$B=$C=$D=$F=$T=0;
function errormessage($string,$color) {
	include "jpgraph/jpgraph_canvas.php";
	$graph = new CanvasGraph(250,100,'auto');
	$graph->SetMargin(00,00,00,00);
	if($color){
		$graph->SetColor($color);
		$graph->SetMarginColor($color);
		$graph->InitFrame(false,$color);
		}
	$text= new Text($string,10,37);
	$text->Stroke($graph->img);
	$graph->Stroke();
}
if(mysql_num_rows($result)==0){
  errormessage("There are no grades associated with\nthis course or professor or both",$color);
	mysql_close($conn);
}
else{
include ("jpgraph/jpgraph_bar.php");
while ($r = mysql_fetch_row($result)) {
	$A+=$r[3];
	$B+=$r[4];
	$C+=$r[5];
	$D+=$r[6];
	$F+=$r[7];
	$T+=$r[8];
}
mysql_close($conn);
function cbFmtPercentage($aVal) {
    return sprintf("%.1f%%",100*$aVal); // Convert to string
}
if($T!=0)
	$data=array($A/$T,$B/$T,$C/$T,$D/$T,$F/$T);
else
	$data=array(0,0,0,0,0);
$graph = new Graph(250,100,'auto');
$graph->SetScale("textlin");
$graph->SetMargin(0,0,20,20);
$graph->SetFrame(false);
$graph->xaxis->SetTickLabels(array("A","B","C","D","F"));
$graph->yaxis->Hide();
$bplot = new BarPlot($data);
$bplot->value->SetFormatCallback("cbFmtPercentage");
$bplot->value->Show();
$bplot->SetWidth(0.5);
if($color){
	$graph->SetFrame(true,$color);
	$graph->SetColor($color);
	$graph->SetMarginColor($color);
	$bplot->SetFillColor($color.":0.75");
	}
$bplot->SetShadow('darkgray');
$graph->Add($bplot);
$graph->Stroke();
}
?>
