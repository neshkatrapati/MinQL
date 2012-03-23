#Basic Import Statements
import re

#Symbols is a Dictionary used for storing MinQL Variables
symbols = {}

#GTK Based Info Dialog [Requires PyGTK 2.0]
def getQuickDialog(message,dianame):
	import pygtk
	pygtk.require('2.0')
	import gtk
	import random
        label = gtk.Label(message)
        dialog =  gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format=None)
        dialog.set_title(dianame)
        dialog.set_markup(message);
        response = dialog.run()
        dialog.destroy()

#Sub method for getQuickDialog
def responseToDialog(entry, dialog, response):
	dialog.response(response)
	
#GTK Based Input Dialog [Requires PyGTK 2.0] [Used for taking variable inputs]	
def gtkInput(q):
	import pygtk
	pygtk.require('2.0')
	import gtk
	import random
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
	
#MinQL String Preprocessor, Responsible for taking inputs and managing variables
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
#MinQL Query Compiler, Returns a MySQL Query	
def compile(input,mode = "Run"):
	query = ""
	
	#Checking for redirectable outputs such as * <- abc => demoVar
	inputArr = re.split("=>",input)
	input = inputArr[0].strip(" \n\t")
	
	#Preprocessing the Query
	input = preprocess(input)
	
	#Initializing output variable 
	if len(inputArr) > 1:
		symbols[inputArr[1].strip(" \n")] = ""
	
			
	if "<-" in input:
		tokens = input.split('<-')
		
		#Take Input
		if tokens[1].strip(" \n") == "@CONSOLE":
			symbols[tokens[0].strip()] = raw_input(tokens[0].strip()+": ")
		elif tokens[1].strip(" \n") == "@GTK":
			symbols[tokens[0].strip()] = gtkInput(tokens[0].strip())
		
		else:
			#Its a Select Query!
			input = input.replace('^','DISTINCT ')
			query = "SELECT " + re.sub(r'\s<-\s',' FROM ',input)
			if "|" in input:
				t = input.split("|")
				wc = "WHERE "+ t[1]
				query = t[0] + " " + wc
				query = "SELECT " + re.sub(r'\s<-\s',' FROM ',query)
			query = query.replace('(','ORDER BY (')
			query = query.replace('[','GROUP BY (')
			query = query.replace(']',')')
		
			
	elif '->' in input:   
                
		x = re.sub(r'\s->\s',' ',input)
		y = re.split('->',input)
		#Create Query
		if ':' in y[1]:
			qt = ""	
			fields = y[1].split(',')
			for f in fields:
				fd = f.split(":")
				qt += fd[0]+" "+fd[1]+","

			query = "CREATE TABLE "+y[0]+" ("+qt[:-1]+")"
		#Update Query
		elif '=' in y[0]:
			query = "UPDATE "+ y[1] + " SET " + y[0]  
			if "|" in x:
				t = y[1].split("|")
				query = "UPDATE "+ t[0] + " SET " + y[0]  
				wc = " WHERE "+ t[1]
				query += wc
			
			
		else:
			
			#Get Output
			if y[1].strip(' \t\n\r') == "@CONSOLE":
				import pprint
				pprint.pprint(y[0])
			
			elif y[1].strip(' \t\n\r') == "@GTK":
				getQuickDialog(y[0],"Message")
			else:
				#Insert Query
				query = "INSERT INTO "+y[1]+" values("+y[0]+")"
			
	elif '#' in input:
		#Delete Query
		x = input.split('#')
		if x[1]!="":
			query = "DELETE FROM "+ x[0] + " WHERE " + x[1]
		else:
			query = "DELETE FROM "+ x[0]
	else:
		if len(inputArr) > 1:
			symbols[inputArr[1].strip(" \n")] = input
		
		
	return query		

#Compile from File	
def fromfile(filename):
	file = open(filename)
	for line in file.readlines():
		if line != "":
			print compile(line)
		

