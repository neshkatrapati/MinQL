import re
import MySQLdb
def preprocess(input):
	iar = re.split("[\s|=#.,]",input)
	ret = []
	i = 0
	for literal in range(len(iar)):

		if '&' in iar[literal]:
			if '&' in input:
				t = raw_input(iar[literal][1:]+":")
				input = input.replace(iar[literal],t)
				iar = re.split("[\s|=#.,]",input)

		i+= 1
	
	return input
		
def execute(input):
	con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="1234" , db="demo")
	cursor = con.cursor()
	input = preprocess(input)
	if "<-" in input:
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
		y = re.split('\s',x)
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
				t = x.split("|")
				wc = " WHERE "+ t[1]
				query += wc
			
			
		else:
			query = "INSERT INTO "+y[1]+" values("+y[0]+")"
	elif '#' in input:
		x = input.split('#')
		if x[1]!="":
			query = "DELETE FROM "+ x[0] + " WHERE " + x[1]
		else:
			query = "DELETE FROM "+ x[0]
	
	ret = {}	
	print query	
	ret["query"] = query
	cursor.execute(query)
	results = cursor.fetchall()
	ret["results"] = results
	con.close()
	retr = []
	for ix in ret["results"]:
		retr.append(list(ix))
	ret["results"] = retr
	return ret


