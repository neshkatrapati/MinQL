import sys
from minqllib import *
if len(sys.argv)>1:
	file = open(sys.argv[2],"r")
	for line in file.readlines():
		if line != "":
			print execute(line)
else:
	while True:
		input = raw_input("minql# ")
		print execute(input)
