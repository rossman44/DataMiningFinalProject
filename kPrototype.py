# Assignment 2 - Data Mining
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
import random
start_time = time.time()

def getData():
    data = []
    with open('nashville_0433_2016-05-22.csv', 'rb') as csvfile: #When testing a different dataset we just switched out the name
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            count = 0
            for item in row:
                if (count == 7 and item in (None, "")): #Any empty values will be replaced by the average for that attribute
                    dataRow.append(5.235)
                elif (count == 10 and item in (None, "")):
                    dataRow.append(1.7177)
                elif (count == 8 and item in (None, "")):
                    dataRow.append(1.94)
                else:
                    dataRow.append(item)
                count = count + 1
            if (dataRow[6] in (None, "")):
            else:
                data.append(dataRow)
        del data[0]
    return data

def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)


def getRandomCentroid(k, dataSet):
    centroids = []
    count = 0
    while (count < k):
        centroids.append(dataSet[random.randint(0, len(dataSet) - 1)])
        count = count + 1
    return centroids

#Need Separate call for Algorithm 2


def determineCluster(dataSet, centroids):
    clusterArray = []
    for row in dataSet: #look at each row to find which cluster it belongs too
        count = 0
        closestCentroid = 0
        shortestDistance = 10000 #initialized shortest distance high
        while (count < len(centroids)): #compare each row in dataset to each centroid
            lam = 0.15
            euc = findEuclideanDistance(centroids[count], row)
            modes = findKModes(centroids[count], row)
            totalClusterDist = euc + modes * lam #lam is the lambda value for our K-Prototype equation to balance out weight of categorical attributes
            if (totalClusterDist < shortestDistance):
                shortestDistance = totalClusterDist
                closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
            count = count + 1
        clusterArray.append(closestCentroid)
    return clusterArray

#find the K-Means dissimilarity measurement
def findEuclideanDistance(centroid, dataRow):
    distance = (3*(float(centroid[6]) - float(dataRow[6])))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + ((float(centroid[9]) - float(dataRow[9])))**2 + ((float(centroid[10]) - float(dataRow[10])))**2 + ((float(centroid[11]) - float(dataRow[11])))**2 + ((float(centroid[12]) - float(dataRow[12])))**2 #includes weights
    distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
    return distance

#finds the K-Modes dissimilarity measurement
def findKModes(centroid, dataRow):
    total = 0
    if (centroid[2] != dataRow[2]): #if the room type between each data point being checked is not the same, it will add 1 to the dissimilarity value that gets returned
        total = total + 1
    if (centroid[4] != dataRow[4]):
        total = total + 1
    return total

def adjustCentroids(clusterArray, k, dataSet): 
    kCounter = 1
    updatedCentroids = []
    while (kCounter <= k):
        dataCount = 0
        cluster = []
        while (dataCount < len(dataSet)): 
            if (kCounter == clusterArray[dataCount]):
                cluster.append(dataSet[dataCount])
            dataCount = dataCount + 1
        if (len(cluster) > 1):
            newCentroid = calculateAverageCentroid(cluster)
            updatedCentroids.append(newCentroid)
        kCounter = kCounter + 1
    return updatedCentroids

#Takes teh cluster and returns a list of just the attribute values at the specified index
def getListofCategorical(cluster, index):
    count = 0
    catList = []
    while (count < len(cluster)):
        catList.append(cluster[count][index])
        count = count + 1
    return catList

#need separate function
def calculateAverageCentroid(cluster):
    count = 0
    newCentroid = []
    newCentroid.append(0) #this is so that the new centroid matches the same list size as the rows
    newCentroid.append(0)

    col2List = getListofCategorical(cluster, 2)
    from collections import Counter
    data = Counter(col2List)
    newCentroid.append(data.most_common(1)[0][0]) #returns the most common
    #print(data.most_common(1)[0][0]) # show what mode function returns

    newCentroid.append(0)

    col4List = getListofCategorical(cluster, 4)
    from collections import Counter
    data = Counter(col4List)
    newCentroid.append(data.most_common(1)[0][0])

    newCentroid.append(0)
    
    columnAverage6 = 0
    columnAverage7 = 0
    columnAverage8 = 0
    columnAverage9 = 0
    columnAverage10 = 0
    columnAverage11 = 0
    columnAverage12 = 0

    for row in cluster:
        columnAverage6 = columnAverage6 + float(row[6])
    columnAverage6 = float(columnAverage6) / float(len(cluster))
    newCentroid.append(columnAverage6)

    for row in cluster:
        columnAverage7 = columnAverage7 + float(row[7])
    columnAverage7 = float(columnAverage7) / float(len(cluster))
    newCentroid.append(columnAverage7)

    for row in cluster:
        columnAverage8 = columnAverage8 + float(row[8])
    columnAverage8 = float(columnAverage8) / float(len(cluster))
    newCentroid.append(columnAverage8)

    for row in cluster:
        columnAverage9 = columnAverage9 + float(row[9])
    columnAverage9 = float(columnAverage9) / float(len(cluster))
    newCentroid.append(columnAverage9)

    for row in cluster:
        columnAverage10 = columnAverage10 + float(row[10])
    columnAverage10 = float(columnAverage10) / float(len(cluster))
    newCentroid.append(columnAverage10)

    for row in cluster:
        columnAverage11 = columnAverage11 + float(row[11])
    columnAverage11 = float(columnAverage11) / float(len(cluster))
    newCentroid.append(columnAverage11)

    for row in cluster:
        columnAverage12 = columnAverage12 + float(row[12])
    columnAverage12 = float(columnAverage12) / float(len(cluster))
    newCentroid.append(columnAverage12)

    return newCentroid

def isCentroidsCorrect(centroids, newCentroids):
    count = 0
    isSame = True
    while (count < len(centroids)):
        if (centroids[count] != newCentroids[count]): #checks if old centroids are the same as the new centroids
            isSame = False
        count = count + 1
    return isSame

#Executes the clustering model
def executeKPrototype(k, dataSet):
    centroids = getRandomCentroid(k, dataSet)
    clusterArray = determineCluster(dataSet, centroids) #finds what cluster each value in the dataSet belongs too
    newCentroids = adjustCentroids(clusterArray, k, dataSet) 
    count = 0
    #Higher cluster tests would sometimes get in a loop of fine tuning categorical attributes so we put a 200 iteration max
    while (isCentroidsCorrect(centroids, newCentroids) == False and count < 200): #Will run until the centroids change, or after 200 iterations because there were some issues with categorical attributes flip flopping back and forth when centroids are very close
        centroids = newCentroids
        clusterArray = determineCluster(dataSet, centroids)
        newCentroids = adjustCentroids(clusterArray, k, dataSet)
        count = count + 1
    prepData(clusterArray, dataSet)

def prepData(clusterArray, dataSet):
    arr = []
    count = 0
    while (count < len(clusterArray)):
        row = []
        index = 0
        while (index < len(dataSet[count])):
            row.append(dataSet[count][index])
            index = index + 1
        row.append(clusterArray[count])
        arr.append(row)
        count = count + 1

    printResults(arr, "NashvilleOutput.csv")

def normalizeOahu(dataata):
    totalNormalizedSet = []
    for row in data:
        normalizedSet = []
        normalizedSet.append(row[0])
        normalizedSet.append(row[1])
        normalizedSet.append(row[2])
        normalizedSet.append(row[3])
        normalizedSet.append(row[4])
        normalizedSet.append(row[5])
        #Initial normalization was mostly basic. Divide value by 95th percentile
        normalizedSet.append(float(row[6]) / 5.0) 
        normalizedSet.append(float(row[7]) / 12.0)
        normalizedSet.append(float(row[8]) / 4.0)
        normalizedSet.append(float(row[9]) / 650.00)
        normalizedSet.append(float(row[10]) / 3.0)
        
        #With extremely close latitutde longitude values we brought them within a 0-1 scale and divided by the distance between the min and max
        normalizedSet.append(
            (float(row[11]) - 35.999726) / (36.366593 - 35.999726)) 
        normalizedSet.append(
            (float(row[12]) + 87.034983) / (-86.546457 + 87.034983))

        totalNormalizedSet.append(normalizedSet)
    return totalNormalizedSet 


def main():
    k = int(sys.argv[1])
    data = getData()
    #data = getWineData()
    data = normalizeOahu(data)
    executeKPrototype(k, data)
    #executeKMeans(k, wineData)

if __name__ == "__main__":
    main()

