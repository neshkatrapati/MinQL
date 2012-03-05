while TRUE do
	print "minql# "
	input = gets.chomp()
	if input.include?("<-")
		query = "SELECT " + input.gsub('<-',' FROM ')
		if input.include?("|")
			t = input.split("|")
			wc = "WHERE "+ t[1]
			query = t[0] + " " + wc
			query = "SELECT " + query.gsub('<-',' FROM ')
		end
	elsif input.include?("->")                  
		y = input.split('->')
		if y[1].include?(":")
			qt = ""	
			fields = y[1].split(',')
			fields.each do |f| 
				fd = f.split(":")
				qt += fd[0]+" "+fd[1]+","
			end

			query = "CREATE TABLE "+y[0]+" ("+qt[0,qt.length-1]+")"

		elsif y[0].include?("=")
			query = "UPDATE "+ y[1] + " SET " + y[0]  
			if y[1].include?("|")
				t = y[1].split("|")
				wc = " WHERE "+ t[1]
				query = "UPDATE "+t[0]+" SET "+y[0]+" "+wc
			end
		else
			query = "INSERT INTO "+y[1]+" values("+y[0]+")"
		end

	elsif input.include?("#")
		x = input.split('#')
		if x.length > 1
			query = "DELETE FROM "+ x[0] + " WHERE " + x[1].to_s
		else
			query = "DELETE FROM "+ x[0]
		end
	
	else
		puts "Sorry!"			
	end
	puts query
end
