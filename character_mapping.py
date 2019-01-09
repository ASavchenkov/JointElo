import csv


with open('characters.csv', 'r') as character_file:
    reader = csv.reader(character_file, skipinitialspace=True)
    for row in reader:
        for element in row:
            print(element)
