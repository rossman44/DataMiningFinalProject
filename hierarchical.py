# Hierarchical Model - Data Mining Final Project
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
import random
start_time = time.time()

def getData():
    data = []
    with open('Oahu_chopped.csv', 'rb') as csvfile:
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
            if (dataRow[6] in (None, "")): #If the overall satisfaction column is empty, we throw out the whole row
                print("")
            else:
                hier = [] #We have to turn our data from a list of lists to a list of list of lists to work correctly for our hierarchical model
                hier.append(dataRow)
                data.append(hier)
        del data[0] #deletes the header
        #print(data)
    return data

def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)


#Dear Grader: the commented out function is the euclidean distance method that did not incorporat our custom weighting. We toggled between weighted and non weighted for testing

#Need Separate call for algorithm 2 
# def findEuclideanDistance(centroid, dataRow):
#     #print(dataRow)
#     distance = (3*(float(centroid[6]) - float(dataRow[6])))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + ((float(centroid[9]) - float(dataRow[9])))**2 + ((float(centroid[10]) - float(dataRow[10])))**2 + ((float(centroid[11]) - float(dataRow[11])))**2 + ((float(centroid[12]) - float(dataRow[12])))**2 #includes weights
#     distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
#     return distance

#Calculates Euclidean Distance between each numerical attribute. The integer values being multiplied to the differences are how much we wanted to weight the attributes by
def findEuclideanDistance(centroid, dataRow):
    distance = (3*(float(centroid[6]) - float(dataRow[6])))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + (1.5 * (float(centroid[9]) - float(dataRow[9])))**2 + ((float(centroid[10]) - float(dataRow[10])))**2 + (0.5 * (float(centroid[11]) - float(dataRow[11])))**2 + (0.5 * (float(centroid[12]) - float(dataRow[12])))**2 #includes weights
    distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
    return distance

#The KModes part of the K-Prototype calculation. 
def findKModes(pointA, pointB):
    total = 0
    if (pointA[2] != pointB[2]): #if the room type between each data point being checked is not the same, it will add 1 to the dissimilarity value that gets returned
        total = total + 1
    if (pointA[4] != pointB[4]):
        total = total + 1
    return total

#In order to use the imported Counter class to find the mode we had format all of the Categorical attributes into a list
def getListofCategorical(cluster, index):
    catList = []
    count = 0
    while (count < len(cluster)):
            #print(cluster)
            catList.append(cluster[count][index])
            count = count + 1
    return catList

#This finds the average or mode for each attribute in the cluster
def calculateAverageCentroid(cluster):
    count = 0
    newCentroid = []
    newCentroid.append(0) #this is so that the new centroid matches the same list size and format as the rows
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
    newCentroid.append(data.most_common(1)[0][0]) #adds the most common value to the centroid

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

    hier = [] #This is needed to turn the list of lists to a list of list of lists
    hier.append(newCentroid)

    return hier

#Can use for both
# def isCentroidsCorrect(centroids, newCentroids):
#     count = 0
#     isSame = True
#     #print(centroids)
#     while (count < len(centroids)):
#         if (centroids[count] != newCentroids[count]):
#             isSame = False
#         count = count + 1
#     return isSame

#Needs separate for calls
def executeHierarchical(k, dataSet):

    while (len(dataSet) > k):
        closestA = 0 #We store the indexes of the two closest points
        closestB = 1
        countA = 0
        smallestDist = 1000.0 #initializes smallestDist as somehthing large
        while (countA < len(dataSet) - 1): #Since the dataSet is a list of clusters, each time clusters get merged the length of the dataSet goes down
            countB = countA + 1
            while(countB < len(dataSet)):
                pointA = dataSet[countA]
                pointB = dataSet[countB]
                if (len(dataSet[countA]) > 1): #If the cluster currently has more than one record in it we compare the average centroid 
                    pointA = calculateAverageCentroid(dataSet[countA])
                if (len(dataSet[countB]) > 1):
                    pointB = calculateAverageCentroid(dataSet[countB])                 
                lam = 0.15 #This value was hardcoded and changed as we needed to test different things
                kmeans = findEuclideanDistance(pointA[0], pointB[0])
                modes = findKModes(pointA[0], pointB[0])
                totalClusterDist = kmeans + modes * lam 
                if (totalClusterDist < smallestDist):
                    smallestDist = totalClusterDist
                    closestA = countA
                    closestB = countB
                countB = countB + 1
            countA = countA + 1
        #print("Through Third While")
        for row in dataSet[closestB]:
            dataSet[closestA].append(row)
        del(dataSet[closestB]) #appends B to A and deletes B
        print(len(dataSet))

    prepData(dataSet)

def prepData(dataSet):
    arr = []
    clusterNum = 1

    for cluster in dataSet:
        for review in cluster:
            row = []
            for item in review:
                row.append(item)
            row.append(clusterNum)
            arr.append(row)
        clusterNum = clusterNum + 1

    printResults(arr, "OahuOutput.csv")

def normalizeOahu(data):
    totalNormalizedSet = []
    for cluster in data:
        for row in cluster:
            normalizedSet = []
            normalizedSet.append(row[0])
            normalizedSet.append(row[1])
            normalizedSet.append(row[2])
            normalizedSet.append(row[3])
            normalizedSet.append(row[4])
            normalizedSet.append(row[5])
            #Initial normalization was mostly basic. Divide value by 95th percentile
            normalizedSet.append(float(row[6]) - 4.0 / (5.0 - 4.0)) 
            normalizedSet.append(float(row[7]) / 12.0)
            normalizedSet.append(float(row[8]) / 4.0)
            normalizedSet.append(float(row[9]) / 650.00)
            normalizedSet.append(float(row[10]) / 3.0)
        
            #With extremely close latitutde longitude values we brought them within a 0-1 scale and divided by the distance between the min and max
            normalizedSet.append(
                (float(row[11]) - 35.999726) / (36.366593 - 35.999726)) 
            normalizedSet.append(
                (float(row[12]) + 87.034983) / (-86.546457 + 87.034983))
            hier = []
            hier.append(normalizedSet)
            totalNormalizedSet.append(hier)
    return totalNormalizedSet 


def main():
    k = int(sys.argv[1])
    data = getData()
    data = normalizeOahu(data)
    executeHierarchical(k, data)

if __name__ == "__main__":
    main()

