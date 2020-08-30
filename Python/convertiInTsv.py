import csv


with open('test0.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    lista = []

    for row in reader:
        lista.append(row)

with open('test0.tsv', mode= 'w', newline= '', encoding="utf8") as tsv_file:
    TSVWriter = csv.writer(tsv_file, dialect='excel-tab')
    TSVWriter.writerows(lista)