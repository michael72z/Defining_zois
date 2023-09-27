import csv
import math
import numpy as np
import time

x_value = 0
total_1 = 30
total_2 = 30

filename = './drone.csv'
fieldnames = ["x_value", "total_1", "total_2"]

with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
            "total_2": total_2
        }

        csv_writer.writerow(info)
        print(x_value, total_1, total_2)

        if x_value < 50:
            total_1 = 30
        else:
            total_1 = 20

        x_value += 0.0001
        total_2 = total_1 + math.sin(math.degrees(x_value / 50)) / (math.sqrt(x_value))

    time.sleep(0.0001)
