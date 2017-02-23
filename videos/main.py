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
        self.reversePings = [{} for a in range(self.C)] # Latencies from caches to endpoints

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

    cacheSolution = {}
    for cache in range(data.C): # Better order than from 0 to C-1
        print('Cache: {}'.format(cache))

        # Aggregate wanted videos for this cache
        wantedVideos = {}
        for endpoint, cacheEndpointPing in data.reversePings[cache].iteritems():
            for video, Rn in requests[endpoint].iteritems():
                cost = Rn * (data.latencies[endpoint] - cacheEndpointPing) # Rn * (Ld - L)
                if video not in wantedVideos:
                    wantedVideos[video] = cost
                else:
                    wantedVideos[video] += cost
        videos = wantedVideos.keys()
        costs = wantedVideos.values()

        # Sort videos by cost function
        sortedCosts, sortedVideos = zip(*sorted(zip(costs, videos), reverse = True))
        sortedCosts = list(sortedCosts)
        sortedVideos = list(sortedVideos)
        sortedSizes = np.array(data.sizes)[sortedVideos]

        # Find all videos that can fit inside the cache, with that order
        availableSize = data.X
        lastVideo = -1
        while availableSize > 0:
            lastVideo += 1
            availableSize -= sortedSizes[lastVideo]
        # lastVideo is EXCLUSIVE, i.e. made for use with numpy [:lastVideo]
        cacheSolution[cache] = sortedVideos[:lastVideo]
        print(cacheSolution[cache])

        # Remove cached videos from endpoints?
        removeVideos = True
        # If not removed, could lead to the same videos being stored everywhere
        # If they are, we miss out on potentially closer caches

        if removeVideos:
            print('Removing videos')
            for endpoint in data.reversePings[cache].keys():
                for video in cacheSolution[cache]:
                    requests[endpoint].pop(video, None) # Remove video, even if it's not there

        print('')

    print('Solution:')
    print(cacheSolution)
    data.writeResults(cacheSolution)

if __name__ == "__main__":
    names = ['me_at_the_zoo.in', 'videos_worth_spreading.in', 'trending_today.in', 'kittens.in']
    for fileName in names:
        data = DataVideos(fileName)

        UgoOptim(data)
