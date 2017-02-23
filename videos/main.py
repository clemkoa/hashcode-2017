import numpy as np
import math
dataDirectory = 'data/'

def loadMatrixFromFile(fileFullName):
    f = open(fileFullName)
    content = f.readlines()

    info = content[0].split()

    rows = int(info[0])
    columns = int(info[1])
    minIngredient = int(info[2])
    maxCell = int(info[3])

    print 'minIngredient: ' + str(minIngredient)
    print 'maxCell: ' + str(maxCell)

    matrix = np.zeros((rows, columns), dtype = int)

    content.pop(0)

    #  T is 0, M is 1
    for i in range(rows):
        for j in range(columns):
            if content[i][j] == 'M':
                matrix[i][j] = 1

    return (matrix, rows, columns, minIngredient, maxCell)

# numberOfMushrooms = int(np.sum(np.sum(matrix)))
# numberOfTomatoes = int(rows * columns - numberOfMushrooms)
#
# print 'numberOfMushrooms: ' + str(numberOfMushrooms)
# print 'numberOfTomatoes: ' + str(numberOfTomatoes)
#
# print matrix[0:10]
#
# maxNumberOfSlices = min(numberOfTomatoes, numberOfMushrooms) / minIngredient
# print 'maxNumberOfSlices: ' + str(maxNumberOfSlices)

def isSliceOkay(matrix, startRow, endRow, startColumn, endColumn, minIngredient, maxCell):
    (x, y) = matrix.shape
    if endRow >= x or endColumn >= y:
        return False
    subMatrix = matrix[startRow:endRow, startColumn:endColumn]

    if 2 in np.squeeze(subMatrix):
        return False
    numberOfMushrooms = int(np.sum(np.sum(subMatrix)))
    numberOfTomatoes = int((startRow - endRow) * (startColumn - endColumn) - numberOfMushrooms)

    return (numberOfMushrooms >= minIngredient) and (numberOfTomatoes >= minIngredient) and ((numberOfTomatoes + numberOfMushrooms) <= maxCell)

def updateSlice(matrix, startRow, endRow, startColumn, endColumn):
    matrix[startRow:endRow, startColumn:endColumn] = 2
    return matrix

def solveForMatrix(matrix, rows, columns, minIngredient, maxCell):
    sizes = []
    sizes.append((1, maxCell))
    sizes.append((maxCell, 1))
    sizes.append((int(math.sqrt(2 * minIngredient)), int(math.sqrt(2 * minIngredient))))
    sizes.append((minIngredient, 2))
    sizes.append((2, minIngredient))
    sizes.append((2 * minIngredient, 1))
    sizes.append((1, 2 * minIngredient))

    results = []

    totalCellCovered = 0
    for (sizeX, sizeY) in sizes:
        print (sizeX, sizeY)
        i = 0
        j = 0
        localCount = 0

        while i < rows and j < columns:
            if isSliceOkay(matrix, i, i + sizeX, j, j + sizeY, minIngredient, maxCell):
                updateSlice(matrix, i, i + sizeX, j, j + sizeY)
                results.append([i, j, i + sizeX - 1, j + sizeY - 1])
                localCount += 1
            i += 1
            if i >= rows:
                i = 0
                j += 1
        totalCellCovered += localCount * sizeX * sizeY

    # print matrix
    # np.savetxt('test.csv', matrix[1:100, 1:100].astype(int), fmt='%i', delimiter=",")
    print 'Done.'
    print 'Cells covered: ' + str(totalCellCovered)
    print 'Total cells: ' + str(rows * columns)
    return results

def writeResults(results):
    outputFile = 'output/' + fileName + '.txt'
    f = open(outputFile, 'w')
    f.write(str(len(results)) + '\n')
    for r in results:
        f.write(str(r[0]) + ' ' + str(r[1]) + ' ' + str(r[2]) + ' ' + str(r[3]) + '\n')

    f.close()


class DataVideos():
    def __init__(self, fileName):
        f = open('data/' + fileName)
        content = f.readlines()

        info = content[0].split()
        self.V = int(info[0])
        self.E = int(info[1])
        self.R = int(info[2])
        self.C = int(info[3])
        self.X = int(info[4])

        self.sizes = [int(a) for a in content[1].split()]

        self.latencies = []
        self.ping = []

        n = self.E
        print n
        i = 2
        while n != 0:
            self.latencies.append(int(content[i].split()[0]))
            k = int(content[i].split()[1])
            self.ping.append({})
            for j in range(k):
                a,b = content[i + 1 + j].split()
                self.ping[self.E - n][a] = b
            i += k +1
            n -= 1

        offset = i
        self.requests = np.zeros((self.V, self.E), dtype = int)
        for k in range(offset, offset + self.R):
            a,b,k = [int(a) for a in content[k].split()]
            self.requests[a][b] = k
        print self.requests
if __name__ == "__main__":
    names = ['me_at_the_zoo.in'] #, 'videos_worth_spreading.in', 'trending_today.in', 'kittens.in']
    # names = {'small': (2, 2), 'medium': (3, 4), 'big' :(2, 7), 'example': (3, 2)}
    for fileName in names:
        data = DataVideos(fileName)


        # rows = int(info[0])
        # columns = int(info[1])
        # minIngredient = int(info[2])
        # maxCell = int(info[3])
        #
        # print 'minIngredient: ' + str(minIngredient)
        # print 'maxCell: ' + str(maxCell)
