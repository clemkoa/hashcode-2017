import numpy as np
import math
dataDirectory = 'data/'

def writeResults(results):
    outputFile = 'output/' + fileName + '.txt'
    f = open(outputFile, 'w')
    f.write(str(len(results)) + '\n')
    for r in results:
        f.write(str(r[0]) + ' ' + str(r[1]) + ' ' + str(r[2]) + ' ' + str(r[3]) + '\n')

    f.close()

if __name__ == "__main__":
    fileFullName = dataDirectory + 'busy_day.in'
    f = open(fileFullName)
    content = f.readlines()
    globalInfo = [int(a) for a in content[0].split()]

    rows = globalInfo[0]
    columns = globalInfo[1]
    droneNumber = globalInfo[2]
    turns = globalInfo[3]
    maxPayload = globalInfo[4]
    productTypes = int(content[1])
    productTypeWeights = [int(a) for a in content[2].split()]
    wharehousesNumber = int(content[3])
    print(wharehousesNumber)

    wharehousesPositions = []
    wharehousesProducts = []
    for i in range(4, 4 + 2 * wharehousesNumber, 2):
        wharehousesPositions.append((int(content[i].split()[0]), int(content[i].split()[1])))
        wharehousesProducts.append([int(p) for p in content[i + 1].split()])

    orderNumber = int(content[4 + 2 * wharehousesNumber])
    orders = []
    for order in range(5 + 2 * wharehousesNumber, 5 + 2 * wharehousesNumber + 3 * orderNumber, 3):
        orderPositions = [int(a) for a in content[order].split()]
        orderItemNumber = int(content[order+1])
        orderItems = [int(a) for a in content[order+2].split()]
        orders.append({'orderPositions': orderPositions, 'orderItemNumber': orderItemNumber, 'orderItems': orderItems})
