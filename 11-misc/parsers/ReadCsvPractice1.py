from asyncore import read
import csv

columns = []
rows = []

with open('csvpractice1.csv', 'r') as file:
    reader = csv.reader(file)
    columns = next(reader)
    for row in reader:
        rows.append(row)
        print (row)

print ("Printing Columns")
for col in columns:
    print(col, end='')
print()


