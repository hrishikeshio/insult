import csv
with open("train.csv","rb") as f:
    reader = csv.reader(f)
    for row in reader:
        print row[2].decode('unicode-escape')
        
        
