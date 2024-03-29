**MinQL** (Pronounced Min - cool) is a minimalistic query language based on the MySQL's Query Language. MinQL is achieved through python and php but, script for ruby also will be available shortly. The syntax goes as follows

**ALERT RUBY BINARIES ARE NOT YET READY!!**


Running In Interactive Mode
========================
For now only python minql can do this via the minqli script.


	[/home]$ python minqli.py -->> [For Interactive Console]               

	


Syntax
======

SELECT 
------

* `* <- table`  - Compiles to  `SELECT * FROM table`

* `* <- table | age > 25`  Compiles to `SELECT * FROM table WHERE age>25`

* `* <- table (field)` Compiles to `SELECT * FROM table ORDER BY (field)`

* `* <- table [field]`  Compiles to `SELECT * FROM table GROUP BY (field)`

* `* <- table {a,b}`  Compiles to `SELECT * FROM table LIMIT a,b`

CREATE 
-----

`abc -> a:int,b:text` Compiles to `CREATE TABLE abc (a int,b text)`

INSERT
------

`10,20,30 -> numbers` Compiles to `INSERT INTO numbers VALUES(10,20,30)`

UPDATE
-----

`a=a+10 -> mytab | a>10` Compiles to `UPDATE mytab SET a=a+10 where a>10`

DELETE
-----

* `abc #` Compiles to `DELETE FROM abc`

* `abc # a>10` Compiles to `DELETE FROM abc WHERE a>10`

Features
===================================================
**MinQL** also accepts variables. For Example :

`&field <- users `

prompts user for field in Interactive script or takes an array of variables in non interactive script

# Running the Interactive Script

* Use the Connect command to connect to the database `connect host username pwd dbname`

* Use Store to Store a connection `store conname host username pwd dbname`

* Retrieving that connection `connect conname`

* Help for list of supported commands

* Tutorial command for interactive tutorial

* We may also put to the Console, Or Graphical Alert 
using @CONSOLE,@GTK Redirectors. 

`Hello World My Name is &name -> @CONSOLE`

* Similarly We can get inputs from the @CONSOLE,@GTK

**Heads Up @GTK Requires pyGTK2.0!**



See Also
======================
* [Docs for Python]  (https://github.com/freeEdu/MinQL/blob/master/python/README.md)
* [Docs for PHP] (https://github.com/freeEdu/MinQL/blob/master/php/README.md)

