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
from minqllib import *
def prettyprint(list):
	print "-"*15
	for i in list:
		for j in i:
			print j,
		print ""

if len(sys.argv)>1:
	mode = "Run"
	if sys.argv[1] == "--compile":
		mode = "Compile"
	file = open(sys.argv[2],"r")
	for line in file.readlines():
		if line != "":
			x = execute(line,mode)
			if x!="":
				print x
else:
	import os
	while True:
		input = raw_input("minql# ")
		if input == "exit" :
				exit(0)
		if input == "clear":
			os.system("clear")
			continue
		get = execute(input)
		if get != "":
			print "Compiled Query: "+get["query"]
			prettyprint(get["results"])
