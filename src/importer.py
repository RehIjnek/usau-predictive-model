import csv

def import_urls(file_name):
    urls = []

    with open(file_name, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        urls = [row[0] for row in reader]

    return urls
