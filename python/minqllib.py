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

import re
import MySQLdb

symbols = {}

import pygtk
pygtk.require('2.0')
import gtk
import random
def prettyprint(list):
	ret =  "-"*15
	for i in list:
		for j in i:
			ret += j
		ret += ""

def getQuickDialog(message,dianame):
        label = gtk.Label(message)
        dialog =  gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format=None)
        dialog.set_title(dianame)
        dialog.set_markup(message);
        response = dialog.run()
        dialog.destroy()

def responseToDialog(entry, dialog, response):
	dialog.response(response)
	
def gtkInput(q):
	dialog = gtk.MessageDialog(
		None,
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_QUESTION,
		gtk.BUTTONS_OK,
		None)
	dialog.set_markup(q)

	entry = gtk.Entry()

	entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)

	hbox = gtk.HBox()
	hbox.pack_start(gtk.Label("Size:"), False, 5, 5)
	hbox.pack_end(entry)



	dialog.vbox.pack_end(hbox, True, True, 0)
	dialog.show_all()

	dialog.run()
	text = entry.get_text()
	dialog.destroy()
	return text
	

def preprocess(input):
	iar = re.split("[\s|=#.,]",input)
	ret = []
	i = 0
	for literal in range(len(iar)):

		if '&' in iar[literal]:
			if '&' in input:
				if iar[literal][1:] in symbols:
					t = symbols[iar[literal][1:]]
				else:
					t = raw_input(iar[literal][1:]+":")
				input = input.replace(iar[literal],str(t))
				symbols[iar[literal][1:]] = t
				iar = re.split("[\s|=#.,]",input)

		i+= 1
	
	return input
		
def execute(input,cparams,mode = "Run"):
	query = ""
	
	validator = False
	inputArr = re.split("=>",input)
	input = inputArr[0].strip(" \n\t")
	input = preprocess(input)
	if len(inputArr) > 1:
		symbols[inputArr[1].strip(" \n")] = ""
	
		
	if "<-" in input:
		validator = True
		tokens = input.split('<-')
		if tokens[1].strip(" \n") == "@CONSOLE":
			symbols[tokens[0].strip()] = raw_input(tokens[0].strip()+": ")
		elif tokens[1].strip(" \n") == "@GTK":
			symbols[tokens[0].strip()] = gtkInput(tokens[0].strip())
		
		else:
			input = input.replace('^','DISTINCT ')
			query = "SELECT " + re.sub(r'\s<-\s',' FROM ',input)
			if "|" in input:
				t = input.split("|")
				wc = "WHERE "+ t[1]
				query = t[0] + " " + wc
				query = "SELECT " + re.sub(r'\s<-\s',' FROM ',query)
			query = query.replace('(','ORDER BY (')
			query = query.replace('{','LIMIT ')
			query = query.replace('}',' ')
			query = query.replace('[','GROUP BY (')
			query = query.replace(']',')')
		
			
	elif '->' in input:   
                validator = True
		x = re.sub(r'\s->\s',' ',input)
		y = re.split('->',input)
		if ':' in y[1]:
			qt = ""	
			fields = y[1].split(',')
			for f in fields:
				fd = f.split(":")
				qt += fd[0]+" "+fd[1]+","

			query = "CREATE TABLE "+y[0]+" ("+qt[:-1]+")"
		elif '=' in y[0]:
			query = "UPDATE "+ y[1] + " SET " + y[0]  
			if "|" in x:
				t = y[1].split("|")
				query = "UPDATE "+ t[0] + " SET " + y[0]  
				wc = " WHERE "+ t[1]
				query += wc
			
			
		else:
			if y[1].strip(' \t\n\r') == "@CONSOLE":
				import pprint
				pprint.pprint(y[0])
			
			elif y[1].strip(' \t\n\r') == "@GTK":
				getQuickDialog(y[0],"Message")
			else:
				query = "INSERT INTO "+y[1]+" values("+y[0]+")"
			
	elif '#' in input:
		validator = True
		x = input.split('#')
		if x[1]!="":
			query = "DELETE FROM "+ x[0] + " WHERE " + x[1]
		else:
			query = "DELETE FROM "+ x[0]
	elif '$' in input:
		validator = True
		
		query = input
		if "|" in input:
			t = input.split("|")
			wc = "WHERE "+ t[1]
			query = t[0] + " " + wc
			
		query = query.replace('$TABLES','SHOW TABLES')
		query = query.replace('$DATABASES','SHOW DATABASES')
		query = query.replace('(','ORDER BY (')
		query = query.replace('[','GROUP BY (')
		query = query.replace(']',')')
		
		print query
		
	else:
		if len(inputArr) > 1:
			symbols[inputArr[1].strip(" \n")] = input
		
	
	if query != "":
		if mode != "compile":
			ret = {}	
			ret["query"] = query
			try:
				con = MySQLdb.Connect(host=cparams[0], port=3306, user=cparams[1], passwd=cparams[2] , db=cparams[3])
			except:
				print "Oops ! problem in connection!"
			try:
				cursor = con.cursor()
				cursor.execute(query)
				results = cursor.fetchall()
				ret["results"] = results
				con.close()
			except:
				print "Oops Problem In the Query!!"
				return -1
			retr = []
			for ix in ret["results"]:
				retr.append(list(ix))
			ret["results"] = retr
			
			if len(inputArr) > 1:
				symbols[inputArr[1].strip(" \n")] = retr
			return ret
		else:
			return query		
	return validator


