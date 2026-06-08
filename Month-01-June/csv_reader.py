import csv
def csv_reader(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"Name: {row['name']} | Age: {row['age']} | City: {row['city']} ")

csv_reader("people.csv")
