import csv

with open("test_with_solutions.csv","rb") as f:
	with open("test_with_solutions.tsv","wb") as o:
		ass=csv.reader(f)
		out=csv.writer(o, delimiter='	')
		for i in ass:
			
			out.writerow([i[0],i[2][1:-1]])