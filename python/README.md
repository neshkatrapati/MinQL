Python MinQL DOCS
============

**REFER SYNTAX OF MinQL in the Main [README](https://github.com/freeEdu/MinQL/blob/master/README.md) Page**

## Using MinQL in Python

* Import minql.py in your file
* Call minql_compile method for compiling MinQL to MySQL
	- `minql_compile(query [,variables])` where variables is an array of variables used in the query
	- Returns a MySQL query
* Call minql_fromfile method to compile MinQL from a file
	- `minql_compile(filename)` **No Support for variables here**
* Call minql_show_symbols to show the symbol table
