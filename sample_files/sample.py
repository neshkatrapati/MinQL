#!/usr/bin/env python
#Copyright 2012
#Ganesh Katrapati <ganesh.katrapati@gmail.com>
#This file is part of MinQL.

#MinQL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#MinQL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with MinQl. If not, see <http://www.gnu.org/licenses/>.

import sys

#Adding path importing
sys.path.append("../python/")

#Importing MinQL
from minql import *


#Simple SELECT Query
query = minql_compile("* <- abc");
print query;


#Variable SELECT Query
query = minql_compile("&f1,&f2,&f3 <- abc",["a","b","c"]);
print query;


#Insert Query
query = minql_compile("&f1,&f2,&f3 -> abc",[10,20,30]);
print query;


#Create Query
query = minql_compile("abcd -> a:int,b:text,c:text,d:int");
print query;


#Update Query
query = minql_compile("&f1=&f1+10 -> abc | &f1>20",["a"]);
print query;


#Delete Query
query = minql_compile("abc # a > 20");
print query;
