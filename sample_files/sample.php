<?php
/*
Copyright 2012
Ganesh Katrapati <ganesh.katrapati@gmail.com>
This file is part of MinQL.

MinQL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MinQL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MinQl. If not, see <http://www.gnu.org/licenses/>.*/

require '../php/minql.php';

//Simple SELECT Query
$query = minql_compile("* <- abc");
echo $query;
echo "\n";

//Variable SELECT Query
$query = minql_compile("&f1,&f2,&f3 <- abc",array("a","b","c"));
echo $query;
echo "\n";

//Insert Query
$query = minql_compile("&f1,&f2,&f3 -> abc",array(10,20,30));
echo $query;
echo "\n";

//Create Query
$query = minql_compile("abcd -> a:int,b:text,c:text,d:int");
echo $query;
echo "\n";

//Update Query
$query = minql_compile("&f1=&f1+10 -> abc | &f1>20",array("a"));
echo $query;
echo "\n";

//Delete Query
$query = minql_compile("abc # a > 20");
echo $query;
echo "\n";

?>