#!/usr/bin/env python
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
