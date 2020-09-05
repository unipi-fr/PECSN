import csv

with open('test.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    lista = []

    for row in reader:
        lista.append(row)

with open('test.tsv', mode= 'w', newline= '', encoding="utf8") as tsv_file:
    TSVWriter = csv.writer(tsv_file, dialect='excel-tab')
    TSVWriter.writerows(lista)