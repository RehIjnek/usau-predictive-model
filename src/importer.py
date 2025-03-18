import csv

def import_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        return next(reader, None)
