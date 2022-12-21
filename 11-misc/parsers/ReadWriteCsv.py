import csv

with open('Books for Sale.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    line_count = 0
    for row in csv_reader:
        if (line_count == 0):
            print (row)
            line_count = line_count + 1
        else:
            print (row[0] + "\t" + row[1] + "\t" + row[2])
            line_count = line_count + 1
    print ("Number of entries : " , line_count)

with open('Books for Sale.csv') as csv_file:    
    csv_dict_reader = csv.DictReader(csv_file)
    print (csv_dict_reader)
    for each_row in csv_dict_reader:
        print (each_row)

with open('Books for Sale Write.csv', mode='a') as csv_file:
    fieldnames = ['BookName', 'Status', 'Price']
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #csv_writer.writerow(['The logic of life','Sold','100'])
    csv_dict_writer.writeheader()
    csv_dict_writer.writerow({'BookName':'lady, you are not a man', 'Status':'Sold', 'Price':'100', 'New Column': 'What happens here' })