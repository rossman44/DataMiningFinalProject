import csv
import math
import sys
import time
import random
start_time = time.time()


def getData():
    data = []
    with open('nashville_0433_2016-05-22.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            count = 0
            for item in row:
                if (count == 7 and item in (None, "")):
                    dataRow.append(2.812)
                elif (count == 10 and item in (None, "")):
                    dataRow.append(3.465)
                elif (count == 8 and item in (None, "")):
                    dataRow.append(1.387)
                else:
                    dataRow.append(item)
                count = count + 1
            if (dataRow[6] in (None, "")):
                print("hit it")
            else:
                data.append(dataRow)
        del data[0]
    return data


def normalizeNashville(originalData):
    count = 0
    totalNormalizedSet = []
    for row in originalData:
        normalizedSet = []
        normalizedSet.append(row[0])
        normalizedSet.append(row[1])
        normalizedSet.append(row[2])
        normalizedSet.append(row[3])
        normalizedSet.append(row[4])
        normalizedSet.append(row[5])
        print(row[6])
        normalizedSet.append(float(row[6]) - 4.0)
        normalizedSet.append(float(row[7]) / 12.0)
        normalizedSet.append(float(row[8]) / 4.0)
        normalizedSet.append(float(row[9]) / 650.00)
        normalizedSet.append(float(row[10]) / 3.0)
        normalizedSet.append(
            (float(row[11]) - 35.999726) / (36.366593 - 35.999726))
        normalizedSet.append(
            (float(row[12]) + 87.034983) / (-86.546457 + 87.034983))

        totalNormalizedSet.append(normalizedSet)
    return totalNormalizedSet


def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)


def main():
    data = getData()
    data = normalizeNashville(data)
    printResults(data, 'nash_output.csv')
    print 'attempted to print'


if __name__ == "__main__":
    main()
