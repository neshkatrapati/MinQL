PHP MinQL DOCS
============

**REFER SYNTAX OF MinQL in the Main README Page**

## Using MinQL in PHP

* Include/Require minql.php in your file
* Call minql_compile method for compiling MinQL to MySQL
	- `minql_compile($query [,$variables])` where variables is an array of variables used in the query
	- Returns a MySQL query
* Call minql_query method to compile and execute MinQL
	- `minql_compile($query , $connection [,$variables])` where connection is mysql connection
	- Returns a MySQL resource
* Call minql_show_symbols to show the symbol table
