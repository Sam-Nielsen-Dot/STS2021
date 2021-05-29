import csv
i = 0

accuracy = 99

r = csv.reader(open('Datasets\\results.csv')) # Here your csv file
lines = list(r)

print(lines)
lines[i+1][7] = accuracy
print(lines)

writer = csv.writer(open('Datasets\\results.csv', 'w', newline=""))
writer.writerows(lines)