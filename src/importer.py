import csv

def import_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            return row
