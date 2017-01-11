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
    maxIngredient = int(info[3])

    print 'minIngredient: ' + str(minIngredient)
    print 'maxIngredient: ' + str(maxIngredient)

    matrix = np.zeros((rows, columns))

    content.pop(0)

    #  T is 0, M is 1
    for i in range(rows):
        for j in range(columns):
            if content[i][j] == 'M':
                matrix[i][j] = 1

    return (matrix, rows, columns, minIngredient, maxIngredient)

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
    subMatrix = matrix[startRow:endRow, startColumn:endColumn]

    if 2 in np.squeeze(subMatrix):
        return False
    numberOfMushrooms = int(np.sum(np.sum(subMatrix)))
    numberOfTomatoes = int((startRow - endRow) * (startColumn - endColumn) - numberOfMushrooms)

    return (numberOfMushrooms >= minIngredient) and (numberOfTomatoes >= minIngredient) and ((numberOfTomatoes + numberOfMushrooms) <= maxCell)

def updateSlice(matrix, startRow, endRow, startColumn, endColumn):
    matrix[startRow:endRow, startColumn:endColumn] = 2
    return matrix

def solveForMatrix(matrix, rows, columns, minIngredient, maxIngredient, sizeX, sizeY):
    i = 0
    j = 0

    print matrix

    results = []
    while i < rows and j < columns - sizeY + 1:
        if isSliceOkay(matrix, i, i + sizeX, j, j + sizeY, minIngredient, maxIngredient):
            updateSlice(matrix, i, i + sizeX, j, j + sizeY)
            results.append([i, j, i + sizeX - 1, j + sizeY - 1])
        i += 1
        if i >= rows - sizeX + 1:
            i = 0
            j += 1

    print 'Done.'
    print 'Cells covered: ' + str(len(results) * sizeX * sizeY)
    print 'Total cells: ' + str(rows * columns)
    return results

def writeResults(results):
    outputFile = 'output/' + fileName + '.txt'
    f = open(outputFile, 'w')
    f.write(str(len(results)) + '\n')
    for r in results:
        f.write(str(r[0]) + ' ' + str(r[1]) + ' ' + str(r[2]) + ' ' + str(r[3]) + '\n')

    f.close()


if __name__ == "__main__":
    names = {'small': (1, 5), 'medium': (1, 12), 'big' :(1, 14), 'example': (3, 2)}
    # names = {'small': (2, 2), 'medium': (3, 4), 'big' :(2, 7), 'example': (3, 2)}
    for fileName, size in names.iteritems():
        print 'Starting on file ' + fileName
        fileFullName = dataDirectory + fileName + '.in'
        (matrix, rows, columns, minIngredient, maxIngredient) = loadMatrixFromFile(fileFullName)
        # size = int(math.sqrt(maxIngredient))
        # print 'size: ' + str(size)
        (sizeX, sizeY) = size
        results = solveForMatrix(matrix, rows, columns, minIngredient, maxIngredient, sizeX, sizeY)
        writeResults(results)
