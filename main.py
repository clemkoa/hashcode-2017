#!/usr/bin/env python

import numpy as np
import math
import time
dataDirectory = 'data/'

def loadMatrixFromFile(fileFullName):
    f = open(fileFullName)
    content = f.readlines()

    info = content[0].split()

    rows = int(info[0])
    columns = int(info[1])
    minIngredients = int(info[2])
    maxCells = int(info[3])

    print 'minIngredients: ' + str(minIngredients)
    print 'maxCells: ' + str(maxCells)

    matrix = np.zeros((rows, columns), dtype = np.int64)

    content.pop(0)

    #  T is 0, M is 1
    for i in range(rows):
        for j in range(columns):
            if content[i][j] == 'M':
                matrix[i][j] = 1

    return (matrix, rows, columns, minIngredients, maxCells)

# numberOfMushrooms = int(np.sum(np.sum(matrix)))
# numberOfTomatoes = int(rows * columns - numberOfMushrooms)
#
# print 'numberOfMushrooms: ' + str(numberOfMushrooms)
# print 'numberOfTomatoes: ' + str(numberOfTomatoes)
#
# print matrix[0:10]
#
# maxNumberOfSlices = min(numberOfTomatoes, numberOfMushrooms) / minIngredients
# print 'maxNumberOfSlices: ' + str(maxNumberOfSlices)

def isSliceOkay(matrix, startRow, endRow, startColumn, endColumn, minIngredients, maxCells):
    (x, y) = matrix.shape
    if endRow >= x or endColumn >= y:
        return False
    subMatrix = matrix[startRow:endRow, startColumn:endColumn]

    if 2 in np.squeeze(subMatrix):
        return False
    numberOfMushrooms = int(np.sum(np.sum(subMatrix)))
    numberOfTomatoes = int((startRow - endRow) * (startColumn - endColumn) - numberOfMushrooms)

    return (numberOfMushrooms >= minIngredients) and (numberOfTomatoes >= minIngredients) and ((numberOfTomatoes + numberOfMushrooms) <= maxCells)

def updateSlice(matrix, startRow, endRow, startColumn, endColumn):
    matrix[startRow:endRow, startColumn:endColumn] = 2
    return matrix

def solveForMatrix(matrix, rows, columns, minIngredients, maxCells):
    sizes = []
    sizes.append((1, maxCells))
    sizes.append((maxCells, 1))
    sizes.append((int(math.sqrt(2 * minIngredients)), int(math.sqrt(2 * minIngredients))))
    sizes.append((minIngredients, 2))
    sizes.append((2, minIngredients))

    results = []

    totalCellCovered = 0
    for (sizeX, sizeY) in sizes:
        print (sizeX, sizeY)
        i = 0
        j = 0
        localCount = 0

        while i < rows and j < columns:
            if isSliceOkay(matrix, i, i + sizeX, j, j + sizeY, minIngredients, maxCells):
                updateSlice(matrix, i, i + sizeX, j, j + sizeY)
                results.append([i, j, i + sizeX - 1, j + sizeY - 1])
                localCount += 1
            i += 1
            if i >= rows:
                i = 0
                j += 1
        totalCellCovered += localCount * sizeX * sizeY
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

# Incoming results are meant for use when slicing in numpy
# e.g. startRow, endRow (exclusive), startColumn, endColumn (exclusive)
def writeResultsPaul(fileName, results):
    outputFile = 'output/' + fileName + '.txt'
    f = open(outputFile, 'w')
    f.write(str(len(results)) + '\n')
    for r in results:
        f.write(str(r[0]) + ' ' + str(r[2]) + ' ' + str(r[1]-1) + ' ' + str(r[3]-1) + '\n')

    f.close()


if __name__ == "__main__":
    names = ['example', 'small']
    for fileName in names:
        fileFullName = dataDirectory + fileName + '.in'
        (fullMatrix, _, _, minIngredients, maxCells) = loadMatrixFromFile(fileFullName)
        fullRows, fullColumns = fullMatrix.shape
        print(fullMatrix)

        rowPartitioning = 1
        columnPartitioning = 1
        debug = False

        filledCells = 0
        finalSlices = []
        for a in range(rowPartitioning):
            print('{}% done'.format(100.0 * float(a) / float(rowPartitioning)))
            for b in range(columnPartitioning):
                mA = int(np.floor(float(a * fullRows) / float(rowPartitioning)))
                MA = int(np.floor(float((a + 1) * fullRows) / float(rowPartitioning)))
                mB = int(np.floor(float(b * fullColumns) / float(columnPartitioning)))
                MB = int(np.floor(float((b + 1) * fullColumns) / float(columnPartitioning)))

                matrix = fullMatrix[mA:MA, mB:MB]
                (rows, columns) = matrix.shape

                minCells = 2 * minIngredients
                minRows = min(int(np.floor(float(minCells) / float(columns))), rows - 1)
                maxRows = maxCells

                mask = np.full((matrix.shape[0], matrix.shape[0]), 1, dtype = np.int64)
                mask = np.tril(mask)
                temp = np.dot(mask, matrix)

                slices = []
                start = time.time()
                for startRow in range(rows):
                    if debug:
                        print('startRow: {}'.format(startRow))

                    for i in range(minRows, min(maxRows, rows - startRow)):
                        # Initialize
                        currentBackCursor = int(np.ceil(-float(maxCells) / float(i + 1)))
                        currentMinCursor = 0
                        currentTomatoes = 0
                        currentMushrooms = 0

                        for j in range(columns):
                            if debug:
                                print('')
                                print('Column: {}'.format(j))

                            currentTomatoes += temp[i][j]
                            currentMushrooms += (i + 1) - temp[i][j]
                            currentBackCursor += 1

                            if debug:
                                print('currentTomatoes: {}'.format(currentTomatoes))
                                print('currentMushrooms: {}'.format(currentMushrooms))

                                print('currentBackCursor: {}'.format(currentBackCursor))
                                print('currentMinCursor: {}'.format(currentMinCursor))
                                print('currentItem: {}'.format(temp[i][currentMinCursor]))

                            done = False
                            while not done:
                                done = True

                                tomatoesUnderCursor = temp[i][currentMinCursor]
                                mushroomsUnderCursor = (i + 1) - tomatoesUnderCursor
                                if (currentTomatoes - tomatoesUnderCursor >= minIngredients) and (currentMushrooms - mushroomsUnderCursor >= minIngredients):
                                    if debug:
                                        print('Enough stuff')
                                        print('Tomatoes under cursor: {}'.format(tomatoesUnderCursor))
                                        print('Mushrooms under cursor: {}'.format(mushroomsUnderCursor))
                                    currentTomatoes -= tomatoesUnderCursor
                                    currentMushrooms -= mushroomsUnderCursor
                                    currentMinCursor += 1
                                    done = False

                                if not done and debug:
                                    print('currentTomatoes: {}'.format(currentTomatoes))
                                    print('currentMushrooms: {}'.format(currentMushrooms))

                                    print('currentBackCursor: {}'.format(currentBackCursor))
                                    print('currentMinCursor: {}'.format(currentMinCursor))
                                    print('currentItem: {}'.format(temp[i][currentMinCursor]))
                                    print('')

                            if (currentTomatoes >= minIngredients) and (currentMushrooms >= minIngredients):
                                if debug:
                                    print('We may have enough ingredients')
                                for k in range(max(0, currentBackCursor), currentMinCursor + 1):
                                    if debug:
                                        print((startRow, startRow + i + 1, k, j + 1))
                                    slices.append((startRow, startRow + i + 1, k, j + 1))

                    # Update temp for new startRow
                    temp = temp[1:, :] - matrix[startRow, :]

                numSlices = len(slices)
                if debug:
                    print('')
                    print('Summary:')
                    print('Example is {} x {}'.format(*matrix.shape))
                    print('Found {} possible slices'.format(numSlices))
                    print('In {}'.format(time.time() - start))

                # ### Check all slices ###
                # for p in slices:
                #     isValid = ((p[1] - p[0]) * (p[3] - p[2]) <= maxCells)
                #     isValid = isValid and (np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 1) >= minIngredients)
                #     isValid = isValid and (np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 0) >= minIngredients)
                #
                #     if not isValid:
                #         print(p)
                #         print(matrix[p[0]:p[1], p[2]:p[3]])
                #         print((p[1] - p[0]) * (p[3] - p[2]) <= maxCells)
                #         print(np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 1) >= minIngredients)
                #         print(np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 0) >= minIngredients)
                #         print('')
                #
                # ### Check for all possible slices, brute force ###
                # start = time.time()
                # possibilities = []
                # for i in range(rows):
                #     for i_ in range(i + 1, rows + 1):
                #         for j in range(columns):
                #             for j_ in range(j + 1, columns + 1):
                #                 p = (i, i_, j, j_)
                #                 isValid = ((p[1] - p[0]) * (p[3] - p[2]) <= maxCells)
                #                 isValid = isValid and (np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 1) >= minIngredients)
                #                 isValid = isValid and (np.sum(matrix[p[0]:p[1], p[2]:p[3]] == 0) >= minIngredients)
                #
                #                 if isValid:
                #                     possibilities.append(p)
                # print('Brute force slice count: {}'.format(len(possibilities)))
                # print('In {}'.format(time.time() - start))

                ### Create the collision matrix ###
                if numSlices > 8000:
                    print('Too many slices')
                    exit(1)

                start = time.time()
                collision = np.zeros((numSlices, numSlices), dtype = bool)
                sizes = np.zeros((numSlices,), dtype = np.int64)
                ids = np.arange(numSlices, dtype = np.int64)
                for i in range(numSlices):
                    p1 = slices[i]
                    sizes[i] = (p1[1] - p1[0]) * (p1[3] - p1[2])
                    for j in range(i + 1, numSlices):
                        p2 = slices[j]

                        if (p1[0] < p2[1]) and (p1[1] > p2[0]): # Possible collision
                            if (p1[2] < p2[3]) and (p1[3] > p2[2]):
                                collision[i, j] = True
                                collision[j, i] = True

                costs = np.dot(collision, sizes)
                while np.sum(costs) != 0:
                    worst = np.argmax(costs)

                    costs = np.delete(costs - sizes[worst] * collision[:, worst], worst)
                    collision = np.delete(np.delete(collision, worst, axis = 0), worst, axis = 1)
                    sizes = np.delete(sizes, worst)
                    ids = np.delete(ids, worst)

                filledCells += np.sum(sizes)
                for i in ids:
                    p = slices[i]
                    finalSlices.append((mA + p[0], mA + p[1], mB + p[2], mB + p[3]))
                if debug:
                    print('')
                    print('Summary:')
                    print('Found distribution for {} cells'.format(np.sum(sizes)))
                    print('Filled at {}%'.format(100.0 * float(np.sum(sizes)) / float(rows * columns)))
                    print('In {}'.format(time.time() - start))

        print('')
        print('')
        print('Final summary:')
        print('Found distribution for {} cells'.format(filledCells))
        print('Filled at {}%'.format(100.0 * float(filledCells) / float(fullRows * fullColumns)))
        print('Used {} slices'.format(len(finalSlices)))

        writeResultsPaul(fileName, finalSlices)
