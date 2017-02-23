#!/usr/bin/env python
import numpy as np
import math, copy
dataDirectory = 'data/'

class DataVideos():
    def __init__(self, fileName):
        self.fileName = fileName
        f = open(dataDirectory + fileName)
        content = f.readlines()

        info = content[0].split()
        self.V = int(info[0])
        self.E = int(info[1])
        self.R = int(info[2])
        self.C = int(info[3])
        self.X = int(info[4])

        self.sizes = [int(a) for a in content[1].split()]

        self.latencies = []
        self.pings = [{} for a in range(self.E)] # Latencies from endpoints to caches
        self.reversePings = [{} for a in range(self.C)] # Latencies from endpoints to caches

        n = self.E
        i = 2
        while n != 0:
            self.latencies.append(int(content[i].split()[0]))
            k = int(content[i].split()[1])
            for j in range(k):
                a, b = content[i + 1 + j].split()
                self.pings[self.E - n][int(a)] = int(b)
                self.reversePings[int(a)][self.E - n] = int(b)
            i += k +1
            n -= 1

        offset = i
        self.requests = [{} for a in range(self.E)] # For each endpoint, a dictionary of videos and associated number of requests
        for k in range(offset, offset + self.R):
            a,b,k = [int(a) for a in content[k].split()]
            self.requests[b][a] = k
        print 'Done initialising file ' + str(fileName)
        result = self.findBaseline()
        self.writeResults(result)

    def findBaseline(self):
        result = {}
        for i in range(self.C):
            result[i] = []
            memoryUsed = 0
            videoId = 0
            while memoryUsed < self.X:
                memoryUsed += self.sizes[videoId]
                videoId += 1
                if memoryUsed < self.X:
                    result[i].append(videoId)
        return result

    def writeResults(self, results):
        ###############       FORMAT        ################
        # result is a dict, the keys are serverIds
        # the values are list(videoIds)

        outputFile = 'output/' + self.fileName + '.txt'
        f = open(outputFile, 'w')
        f.write(str(len(results)) + '\n')
        for r in results:
            s = str(r)
            for v in results[r]:
                s = s + ' ' + str(v)
            s = s + '\n'
            f.write(s)

        f.close()

def UgoOptim(data):
    # Make a copy of requests
    requests = copy.deepcopy(data.requests)
    print(requests)

    cacheSolution = {}
    for cache in range(data.C): # Better order than from 0 to C-1
        availableSize = data.sizes[cache]

        # Aggregate wanted videos for this cache


    print('Solution:')
    print(cacheSolution)

if __name__ == "__main__":
    names = ['me_at_the_zoo.in', 'videos_worth_spreading.in', 'trending_today.in', 'kittens.in']
    for fileName in names:
        data = DataVideos(fileName)

        UgoOptim(data)
