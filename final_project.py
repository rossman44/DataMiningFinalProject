# Assignment 2 - Data Mining
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
import random
start_time = time.time()

#Gets the data from income_tr
def getData():
    data = []
    with open('Oahu_3_15_2016.csv', 'rb') as csvfile:
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

# Gets the data from income_tr
# def getData():
#     data = []
#     with open('Oahu_3_15_2016.csv', 'rb') as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         csvCount = 0
#         while (csvCount < len(csvreader)):
#             dataRow = []
#             rowCount = 0
#             while (rowCount < len(csvreader[csvCount])):
#                 if (csvreader[csvCount][5] != 0):
#                     if csvreader[csvCount][7] in (None, ""):
#                         dataRow.append(2.812)
#                     else:
#                         dataRow.append(csvreader[csvCount][rowCount])
#                 rowCount = rowCount + 1
#             data.append(dataRow)
#             csvCount = csvCount + 1
#         del data[0]


        # for row in csvreader:
        #     dataRow = []
        #     for item in row:
        #         dataRow.append(item)
            
        #     if row[7] in (None, ""):
        #         print(row[7])
        #         row[7] = 2.812 #this is the average for that column
        #     if (row[5] != 0):
        #         data.append(dataRow)

        # del data[0]
    #print(data)
    # return data


def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)

#Can use for both
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
            #print((centroids[count])) #problem is centroids are empty
            lam = 0.3
            euc = findEuclideanDistanceSet1(centroids[count], row)
            modes = findKModes(centroids[count], row)
            totalClusterDist = euc + modes * lam #lam is the lambda value for our K-Prototype equation to balance out weight of categorical attributes
            if (totalClusterDist < shortestDistance):
                shortestDistance = totalClusterDist
                closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
            count = count + 1
        clusterArray.append(closestCentroid)
    return clusterArray

#Need Separate call for algorithm 2 
def findEuclideanDistanceSet1(centroid, dataRow):
    distance = (3*(float(centroid[6]) - float(dataRow[6])))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + ((float(centroid[9]) - float(dataRow[9])))**2 + ((float(centroid[10]) - float(dataRow[10])))**2 + ((float(centroid[11]) - float(dataRow[11])))**2 + ((float(centroid[12]) - float(dataRow[12])))**2 #includes weights
    distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
    return distance

def findKModes(centroid, dataRow):
    total = 0
    if (centroid[2] == dataRow[2]):
        total = total + 1
    if (centroid[4] == dataRow[4]):
        total = total + 1
    return total

#need separate call for algorithm 2 -- calls calculateAverageCentroid
def adjustCentroids(clusterArray, k, dataSet): #believe this works correctly now
    kCounter = 1
    updatedCentroids = []
    #print(clusterArray)
    while (kCounter <= k):
        dataCount = 0
        cluster = []
        while (dataCount < len(dataSet)): 
            if (kCounter == clusterArray[dataCount]):
                cluster.append(dataSet[dataCount])
            dataCount = dataCount + 1
        if (len(cluster) > 1):
            newCentroid = calculateAverageCentroid(cluster)
            #print(newCentroid)
            updatedCentroids.append(newCentroid)
        kCounter = kCounter + 1
    return updatedCentroids

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

    # column2item1 = 0
    # column2item2 = 0
    # column2item3 = 0

    # column4item1 = 0
    # column4item2 = 0
    # column4item3 = 0
    # column4item4 = 0
    # column4item5 = 0
    # column4item6 = 0
    # column4item7 = 0
    # column4item8 = 0
    # column4item9 = 0

    # while (count < len(cluster)):
    #     print(len(cluster[count][2]))
    #     if(len(cluster[count][2]) == 11):
    #         column2item1 = column2item1 + 1
    #     elif(len(cluster[count][2]) == 12):
    #         column2item2 = column2item2 + 1
    #     else:
    #         column2item3 = column2item3 + 1
    #     count = count + 1

    #     columnMode4 = columnMode4 + cluster[count][4]


    col2List = getListofCategorical(cluster, 2)
    from collections import Counter
    data = Counter(col2List)
    newCentroid.append(data.most_common(1)[0][0])
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

#Can use for both
def isCentroidsCorrect(centroids, newCentroids):
    count = 0
    isSame = True
    #print(centroids)
    while (count < len(centroids)):
        if (centroids[count] != newCentroids[count]):
            isSame = False
        count = count + 1
    return isSame

#Needs separate for calls
def executeKMeans(k, dataSet):
    centroids = getRandomCentroid(k, dataSet)
    clusterArray = determineCluster(dataSet, centroids) 
    newCentroids = adjustCentroids(clusterArray, k, dataSet) 
    count = 0
    while (isCentroidsCorrect(centroids, newCentroids) == False and count < 200):
        centroids = newCentroids
        clusterArray = determineCluster(dataSet, centroids)
        newCentroids = adjustCentroids(clusterArray, k, dataSet)
        print(count)
        print(centroids[0])
        count = count + 1
    prepData(clusterArray, dataSet)

#Can use for both ---JK u suck kyle
def prepData(clusterArray, dataSet):
    arr = []
    count = 0
    #arr.append(["ID", "Cluster"])
    while (count < len(clusterArray)):
        row = []
        index = 0
        while (index < len(dataSet[count])):
            row.append(dataSet[count][index])
            index = index + 1
        row.append(clusterArray[count])
        arr.append(row)
        count = count + 1

    printResults(arr, "OahuOutput.csv")

def normalizeOahu(wineData):
    count = 0
    totalNormalizedSet = []
    for row in wineData:
        normalizedSet = []
        normalizedSet.append(row[0])
        normalizedSet.append(row[1])
        normalizedSet.append(row[2])
        normalizedSet.append(row[3])
        normalizedSet.append(row[4])
        normalizedSet.append(row[5])
        print(row[6])
        normalizedSet.append(float(row[6]) / 5.0 )
        normalizedSet.append(float(row[7]) / 5.0 )
        normalizedSet.append(float(row[8]) / 4.0)
        normalizedSet.append(float(row[9]) / 688.95 )
        normalizedSet.append(float(row[10]) / 7.0 )
        normalizedSet.append((float(row[11]) - 21.25633) / (21.703755 - 21.25633))
        normalizedSet.append((float(row[12]) + 158.260712) / (158.260712 - 157.838787))

        totalNormalizedSet.append(normalizedSet)
    return totalNormalizedSet 


#Need Separate call for Algorithm 2
# def determineClusterWine(dataSet, centroids):
#     clusterArray = []
#     for row in dataSet: #look at each row to find which cluster it belongs too
#         count = 0
#         closestCentroid = 0
#         shortestDistance = 10000 #initialized shortest distance high
#         while (count < len(centroids)): #compare each row in dataset to each centroid
#             euc = findEuclideanDistanceSet2(centroids[count], row)
#             if (euc < shortestDistance):
#                 shortestDistance = euc
#                 closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
#             count = count + 1
#         clusterArray.append(closestCentroid)
#     return clusterArray

#Needs separate for calls
# def executeKMeansWine(k, dataSet):
#     centroids = getRandomCentroid(k, dataSet)
#     #print(centroids)
#     clusterArray = determineClusterWine(dataSet, centroids) #this first clusterArray works
#     newCentroids = adjustCentroidsWine(clusterArray, k, dataSet) #adjustCentroids is fucked ---update might not be fucked
#     #print(newCentroids)
#     #print(newCentroids)
#     while (isCentroidsCorrect(centroids, newCentroids) == False):
#         centroids = newCentroids
#         clusterArray = determineClusterWine(dataSet, centroids)
#         newCentroids = adjustCentroidsWine(clusterArray, k, dataSet)
#     prepData(clusterArray)


# def calculateAverageCentroidWine(cluster):
#     count = 1
#     newCentroid = []
#     newCentroid.append(0) #this is so that the new centroid matches the same list size as the rows
#     while (count <= 10):
#         columnAverage1 = 0
#         for row in cluster:
#             columnAverage1 = columnAverage1 + float(row[count])
#         count = count + 1
#         columnAverage1 = float(columnAverage1) / float(len(cluster))
#         newCentroid.append(columnAverage1) 

#     newCentroid.append(0) #so that averaged centroid matches row in dataset
#     newCentroid.append("string")
#     return newCentroid 

# def adjustCentroidsWine(clusterArray, k, dataSet): #believe this works correctly now
#     kCounter = 1
#     updatedCentroids = []
#     #print(clusterArray)
#     while (kCounter <= k):
#         dataCount = 0
#         cluster = []
#         while (dataCount < len(dataSet)): 
#             #print("Trying to find cluster match")
#             #print(kCounter)
#             #print(clusterArray[dataCount])
#             if (kCounter == clusterArray[dataCount]):
#                 cluster.append(dataSet[dataCount])
#                 #print("Yo we made it fam")
#             dataCount = dataCount + 1
#         #print(cluster)
#         if (len(cluster) > 1):
#             newCentroid = calculateAverageCentroidWine(cluster)
#             #print(newCentroid)
#             updatedCentroids.append(newCentroid)
#         kCounter = kCounter + 1
#     return updatedCentroids

# def findEuclideanDistanceSet2(centroid, dataRow):
#     distance = (float(centroid[1]) - float(dataRow[1]))**2 + (float(centroid[2]) - float(dataRow[2]))**2 + (float(centroid[3]) - float(dataRow[3]))**2 + (float(centroid[4]) - float(dataRow[4]))**2 + (float(centroid[5]) - float(dataRow[5]))**2 + (float(centroid[6]) - float(dataRow[6]))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + (float(centroid[9]) - float(dataRow[9]))**2 + (float(centroid[10]) - float(dataRow[10]))**2 + (float(centroid[11]) - float(dataRow[11]))**2
#     distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
#     return distance


# Gets the data from income_te
# def getWineData():
#     teData = []
#     with open('wine.csv', 'rb') as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         for row in csvreader:
#             dataRow = []
#             for item in row:
#                 dataRow.append(item)
#             teData.append(dataRow)
#         del teData[0]
#     return teData

def main():
    k = int(sys.argv[1])
    data = getData()
    #data = getWineData()
    data = normalizeOahu(data)
    executeKMeans(k, data)
    #executeKMeans(k, wineData)

if __name__ == "__main__":
    main()

