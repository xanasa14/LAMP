<html>
<body>
<?php

$conn=mysql_connect("localhost","root","");

$db=mysql_select_db("stock_market");

$tbl="2017_11_29_11_44_01";

$query="select * from $tbl";


$rows = mysql_query($query);

//echo mysql_error();

$cols = mysql_num_fields($rows);
echo "<table>";
echo "<tr>";
for ($col = 0; $col<$cols; $col++){
	echo "<th>";
	echo mysql_field_name($rows,$col);
	echo "</th>";
	}
echo "</tr>";

while($row=mysql_fetch_array($rows)){
echo "<tr>";
for ($col = 0; $col<$cols; $col++){
	echo "<td>";
	echo $row[$col];
	echo "</td>";
	}
echo "</tr>";
}
echo "</table>";

?>
</body>
</html>
