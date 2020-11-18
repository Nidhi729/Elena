'''
Created on Nov 13, 2020

'''

from src.MapMgr.ProcessMap import ProcessMap

import collections
import heapq 



class Djikstra(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.processMapObj = ProcessMap()

    def generatePath(self, revPath, start, end):
        path = []
        n = end
        path.append(n)
        while n != start:
            n = revPath[n]
            path.append(n)
        return path[::-1]

    def getShortestPath(self, G, start, end, option='length'):
        queue = []
        heapq.heappush(queue, (0, start))
        revPath = {}
        cost = {}
        revPath[start] = None
        cost[start] = 0

        while len(queue) > 0:
            (val, current) = heapq.heappop(queue)
            if current == end:
                break
            for cur, nxt, data in G.edges(current, data=True):
                cur_cost = cost[current]
                if option == 'length':
                    curCost = G.edges[cur, nxt, 0]['length']
                elif option == 'elevation':
                    curCost = self.processMapObj.getPathElevation(G, cur, nxt)
                if curCost > 0:
                    cur_cost += curCost
                if nxt not in cost or cur_cost < cost[nxt]:
                    cost[nxt] = cur_cost
                    heapq.heappush(queue, (cur_cost, nxt))
                    revPath[nxt] = current

        return self.generatePath(revPath, start, end)
    
    def getRoute(self, graph, startNode, endNode, percetage, boolIsMax=True):
        
        minDistance = self.processMapObj.getPathLength(graph, self.getShortestPath(graph, startNode, endNode))
        candidatePath = dict()

        for _ in range(100, int(percetage)+1,10):
            sign = -1 if boolIsMax else 1
            costMap = collections.defaultdict(int)
            elevationCostMap = collections.defaultdict(int)
            
            
            costMap[startNode] = 0
            elevationCostMap[startNode] = 0
             
            heap = []
            heapq.heappush(heap,(0, startNode))
            
            revPath = collections.defaultdict()
            
            revPath[startNode] = None
            
            while heap:
                _,currNode = heapq.heappop(heap) 
                if currNode == endNode:
                    if costMap[currNode] <= (percetage) / 100.0 * minDistance:
                        break
                    
                
                for _,nextNode,_ in graph.edges(currNode, data=True):
                    newCost = costMap[currNode] + graph.edges[currNode, nextNode, 0]['length']
                    currElevation = elevationCostMap[currNode] 
                    elevationCost = self.processMapObj.getElevationGain(graph, currNode, nextNode)
                    
                    if elevationCost >0:
                        currElevation += elevationCost
                        
                    if nextNode not in costMap or  newCost < costMap[nextNode] : # cur_cost < cost[nxt]:
                        costMap[nextNode] = newCost
                        elevationCostMap[nextNode] = currElevation
                        
                        heapq.heappush(heap,(sign*currElevation, nextNode))
                        revPath[nextNode] = currNode

            path = self.generatePath(revPath, startNode, endNode)
            candidatePath[self.processMapObj.getPathElevation(graph, path)] = path

        min_path_len = 10 ** 6
        max_path_len = 0
    
        for el in candidatePath.keys():
            if el <= min_path_len:
                min_path_len = el
            if el >= max_path_len:
                max_path_len = el
    
        if boolIsMax:
            path = candidatePath[max_path_len]
        else:
            path = candidatePath[min_path_len]
    
    
        getPathLatLong = self.processMapObj.getCoordinates(graph, path)
        getPathLength = self.processMapObj.getPathLength(graph, path)
        getPathElevation = self.processMapObj.getPathElevation(graph, path)
        
        return getPathLatLong, getPathLength, getPathElevation

