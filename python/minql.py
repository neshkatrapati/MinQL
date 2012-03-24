#Basic Import Statements
import re

#Symbols is a Dictionary used for storing MinQL Variables
symbols = {}

	
#MinQL String Preprocessor, Responsible for taking inputs and managing variables
def minql_preprocess(input,vars = []):
	iar = re.split("[\s|=#.,]",input)
	ret = []
	i = 0
	count = 0
	for literal in range(len(iar)):

		if '&' in iar[literal]:
			if '&' in input:
				if iar[literal][1:] in symbols:
					t = symbols[iar[literal][1:]]
				else:
					t = vars[count]
					count = count + 1
					
				input = input.replace(iar[literal],str(t))
				symbols[iar[literal][1:]] = t
				iar = re.split("[\s|=#.,]",input)

		i+= 1
	
	return input
#MinQL Query Compiler, Returns a MySQL Query	
def minql_compile(input,vars = []):
	query = ""
	
	#Checking for redirectable outputs such as * <- abc => demoVar
	inputArr = re.split("=>",input)
	input = inputArr[0].strip(" \n\t")
	
	#Preprocessing the Query
	input = minql_preprocess(input,vars)
	
	#Initializing output variable 
	if len(inputArr) > 1:
		symbols[inputArr[1].strip(" \n")] = ""
	
			
	if "<-" in input:
		tokens = input.split('<-')
		
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
def minql_fromfile(filename):
	file = open(filename)
	for line in file.readlines():
		if line != "":
			print compile(line)

def minql_show_symbols():
	print symbols