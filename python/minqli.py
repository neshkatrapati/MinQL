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
from cmd import Cmd
import re
from minqllib import *

def prettyprint(list):
	print "-"*15
	for i in list:
		for j in i:
			print j,
		print ""


class  MinQL(Cmd):
	prompt = "(MinQL) "
	mode = "run"
	cparams = []
	con = None
	tutorial = False
	tuts = ["Hello! welcome to MinQL!!. This is an exciting tiny and turbo query languge made for fun. This tutorial will go through the basics of MinQL. Press 'help' for a start!",
		"These above commands are available in MinQL cmd line interpreter. So, first of all lets try 'mode' command. Type in 'mode compile'",
		"Now that you have typed 'mode compile' the MinQL interpreter is set to compile only mode. This doesnt execute any queries.Now, Type in a MinQL query say .. '* <- abc'",
		"See? this converts a simple and tiny MinQL to MySQL syntax. Type in a few more queries and see them compiled to MySQL. Press next to go to next phase",
		"The Other command in MinQL is connect. This is used to connect to a database. Type in connect [host] [your-username] [your-password] [database name] To connect to the database.",
		"Now that you have connected to database, type in 'mode 'run' to enter query execution mode.",
		"Type in your queries to get them executed. Ending the tutorial! .. Hope you have a good timt trying MinQL"
		]
	tmatcher = ["tutorial",
		    "help",
		    "mode compile",
		    "",
		    "no-inc",
		    "connect",
		    "mode run",
		    ]
	mrc = ""
	tutsi = 0
	def preloop(self):
		print "Welcome to MinQL CMD Line Interpreter. Press Help for options."

	def do_connect(self,arg):
		self.cparams = re.split("\s*",arg)
		self.con = MySQLdb.Connect(host=self.cparams[0], port=3306, user=self.cparams[1], passwd=self.cparams[2] , db=self.cparams[3])
		
		
	def do_mode(self,arg):
		if arg in ["compile","run"]:
			self.mode = arg
			print "Set Mode to "+self.mode
		else:
			print "No Such Mode "+arg
	
			
	def default(self,line):
		if self.mode == "run" and self.con == None:
				print "Type connect command to connect to a database"
				return
		get = execute(line,self.con,self.mode)
		if get != "" and self.mode == "run":
			print "Compiled Query: "+get["query"]
			prettyprint(get["results"])
		elif get!="" :
			print get
		else:
			print "Un recognized Query/Command"
	def do_tutorial(self,arg):
		self.tutorial = True
		
	def postcmd(self,stop,line):
		if line == "quit":
			return True
		if self.tutorial:
			if self.tutsi < len(self.tuts):
				t = re.split("\s*",line)
				if self.tmatcher[self.tutsi] in (t[0],line,"") or line == "next":
					print "Tutorial :: " + self.tuts[self.tutsi]
					self.tutsi += 1
				elif self.tmatcher[self.tutsi]== "no-inc":
					print "Tutorial :: Oops check your command again"
			else:
				self.tutorial = False;
		self.mrc = line
		return False
	def do_next(self,arg):
		pass
	def do_help(self,arg):
		print "="*10
		print "MinQL HELP" 
		print "="*10
		print "mode -> mode [compile/run] {Toggles between run mode and compile mode}"
		print "connect -> connect [database-host] [database-username] [database-password] [database-name] {Connects to a database}"
		print "Refer README.md for syntax"
		print "Type tutorial for interactive tutorial"
		print ""
	def do_quit(self,arg):
		print "Bye!"
		return True
MinQL().cmdloop()


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
