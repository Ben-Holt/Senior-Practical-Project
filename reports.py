import csv

f = open('reports/auditlog', 'w')

writer = csv.writer(f)

writer.writerow(row)

f.close()