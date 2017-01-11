import numpy as np

dataDirectory = 'data/'

fileName = dataDirectory + 'small.in'

f = open(fileName)
content = f.readlines()

info = content[0].split()

rows = int(info[0])
columns = int(info[1])
minIngredient = int(info[2])
maxIngredient = int(info[3])

matrix = np.zeros((rows, columns))

content.pop(0)

#  T is 0, M is 1
for i in range(rows):
    for j in range(columns):
        if content[i][j] == 'M':
            matrix[i][j] = 1

print matrix

numberOfMushrooms = int(np.sum(np.sum(matrix)))
numberOfTomatoes = int(rows * columns - numberOfMushrooms)

print 'numberOfMushrooms: ' + str(numberOfMushrooms)
print 'numberOfTomatoes: ' + str(numberOfTomatoes)
# print matrix
