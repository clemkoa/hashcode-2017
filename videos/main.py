#!/usr/bin/env python
import numpy as np
import math, copy
dataDirectory = 'data/'
import operator
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
        result = self.findBaselineBetter()
        result = self.improveResults(result)
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

    def findBaselineBetter(self):
        result = {}
        for i in range(self.C):
            result[i] = []
            memoryUsed = 0
            j = 0
            endpoints = self.reversePings[i]
            videos = {}

            for endpoint in endpoints:
                for videoId in self.requests[endpoint]:
                    if videoId not in videos:
                        videos[videoId] = 0
                    videos[videoId] += self.requests[endpoint][videoId] / self.sizes[videoId]
            v = sorted(videos.items(), key=operator.itemgetter(1))[::-1]
            while memoryUsed < self.X:
                memoryUsed += self.sizes[v[j][0]]
                if memoryUsed < self.X:
                    result[i].append(v[j][0])
                j += 1
        return result

    def improveResultsWithForbidden(self, result, forbidden):
        for i in range(self.C):
            result[i] = []
            memoryUsed = sum([self.sizes[j] for j in result[i]])
            j = len(result[i])
            endpoints = self.reversePings[i]
            videos = {}

            for endpoint in endpoints:
                for videoId in self.requests[endpoint]:
                    if videoId not in videos:
                        videos[videoId] = 0
                    videos[videoId] += self.requests[endpoint][videoId] / self.sizes[videoId]
            v = sorted(videos.items(), key=operator.itemgetter(1))[::-1]

            m = 0
            while memoryUsed < self.X:
                if m > self.V:
                    break
                m += 1
                if v[j][0] not in forbidden[i]:
                    memoryUsed += self.sizes[v[j][0]]
                    if memoryUsed < self.X:
                        print 'appending some stuff'
                        result[i].append(v[j][0])
                    j += 1
        return result

    def improveResults(self, results):
        score = np.zeros((self.C, self.C, self.V))
        videos = [[[] for i in range(self.C)] for j in range(self.C)]

        for i in range(self.C):
            print i
            iEndpoints = self.reversePings[i]
            videos1 = []
            for endpoint in iEndpoints:
                videosFromEndpoints = self.requests[endpoint]
                for video in videosFromEndpoints:
                    if video not in videos1:
                        videos1.append(video)
            for j in range(self.C):
                if i < j:
                    jEndpoints = self.reversePings[j]
                    videos2 = []
                    for endpoint in jEndpoints:
                        videosFromEndpoints = self.requests[endpoint]
                        for video in videosFromEndpoints:
                            if video not in videos2:
                                videos2.append(video)
                    v =  set(videos1).intersection(videos2)
                    videos[i][j] = list(v)
                    # FOR EACH VIDEO GET SCORE

        for i in range(self.C):
            iEndpoints = self.reversePings[i]
            for j in range(self.C):
                jEndpoints = self.reversePings[j]
                for video in videos[i][j]:
                    d1 = 0
                    total1 = 0
                    n1 = 0

                    d2 = 0
                    total2 = 0
                    n2 = 0
                    for endpoint in iEndpoints:
                        total1 += 1
                        if video in self.requests[endpoint]:
                            d1 += 1
                            if endpoint in jEndpoints:
                                n1 +=1
                    for endpoint in jEndpoints:
                        total2 += 1
                        if video in self.requests[endpoint]:
                            d2 += 1
                            if endpoint in iEndpoints:
                                n2 +=1

                    score[i][j][video] = 1.0 * n1 / d1
                    score[j][i][video] = 1.0 * n2 / d2

        forbidden = [[] for i in range(self.C)]
        for i in range(self.C):
            for j in range(self.C):
                for v in range(self.V):
                    if score[i][j][v] > 0.01:
                        print 'removing ' + str(v)
                        print results[j]
                        results[j] = [x for x in results[j] if x != v]
                        print results[j]
                        forbidden[j].append(v)
                        # return []

        print('forbidden')
        # GET THE OTHERS
        result = self.improveResultsWithForbidden(results, forbidden)
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
    names = ['me_at_the_zoo.in']#, 'videos_worth_spreading.in', 'trending_today.in', 'kittens.in']
    for fileName in names:
        data = DataVideos(fileName)

        # UgoOptim(data)
