<?php
$class=$_GET["class"];
$conn=mysql_connect('localhost','course','shoot')or die('Could not connect: ' . mysql_error());
mysql_select_db('2009A')or die('Could not select database');

$sql="SELECT * FROM ".$class." ORDER BY section";
$result=mysql_query($sql)or die('Query failed: ' . mysql_error());  $table .= "<table $tableFeatures>\n\n";
/*  $noFields = mysql_num_fields($result);
  $table .= "<tr>\n";
  for ($i = 0; $i < $noFields; $i++) {
    $field = mysql_field_name($result, $i);
    $table .= "\t<th>$field</th>\n";
  }
  $table .= "</tr>\n";  */
  while ($r = mysql_fetch_row($result)) {
    $table .= "<tr>";
    foreach ($r as $kolonne) {
      $table .= "<td>$kolonne</td>";
    }
    $table .= "</tr>\n";
  }
  $table .= "</table>\n\n";
  echo $table;
mysql_close($conn);

?>
