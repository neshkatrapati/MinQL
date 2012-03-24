**MinQL** (Pronounced Min - cool) is a minimalistic query language based on the MySQL's Query Language. MinQL is achieved through python and php but, script for ruby also will be available shortly. The syntax goes as follows

*!ALERT RUBY BINARIES ARE NOT YET READY*


Running In Interactive Mode
========================
For now only python minql can do this via the minqli script.
[/home]$ python minqli.py -->> [For Interactive Console]               
[/home]$ python minqli.py --file filename.minql -->> [For File Input]  

Syntax
======

SELECT 
------

`* <- table`  - compiles to  `SELECT * FROM table`
`* <- table | age > 25`  Compiles to `SELECT * FROM table WHERE age>25`

`* <- table (field)` Compiles to `SELECT * FROM table ORDER BY (field)`

`* <- table [field]`  Compiles to `SELECT * FROM table GROUP BY (field)`

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

`abc #` Compiles to `DELETE FROM abc`
`abc # a>10` Compiles to `DELETE FROM abc WHERE a>10`

===================================================
MinQL also accepts variables.For Example :
-----------------
|&field <- users |
-----------------
prompts user for field

We may also put to the Console, Or Graphical Alert 
using @CONSOLE,@GTK Redirectors. 
-------------------------------------------
| Hello World My Name is &name -> @CONSOLE|
-------------------------------------------

Similarly We can get inputs from the @CONSOLE,@GTK

[!Heads Up @GTK Requires pyGTK2.0!]

==================================================

