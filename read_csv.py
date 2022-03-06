import csv

file = open("key_data.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(len(header))
print(header)
rows = []
for row in csvreader:
    rows.append(row)
print(rows)
file.close()