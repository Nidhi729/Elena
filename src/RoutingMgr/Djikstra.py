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

    def getShortestPath(self, graph, start, end):
        queue = []
        
        heapq.heappush(queue, (0, start))
        revPath = {}
        cost = {}
        
        revPath[start] = None
        cost[start] = 0

        while len(queue) > 0:
            currCost,currNode = heapq.heappop(queue)
            if currNode == end:
                break
            
            for _,nextNode,_ in graph.edges(currNode, data=True):
                #currCost = cost[currNode]
                currCost += graph.edges[currNode, nextNode, 0]['length']
                
                if nextNode not in cost or currCost < cost[nextNode]:
                    cost[nextNode] = currCost
                    heapq.heappush(queue,(currCost,nextNode))
                    revPath[nextNode] = currNode
            
        return self.generatePath(revPath, start, end)
    
    def getRoute(self, graph, startNode, endNode, percetage, boolIsMax=True):
        
        minDistance = self.processMapObj.getPathLength(graph, self.getShortestPath(graph, startNode, endNode))
        paths = dict()

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
            paths[self.processMapObj.getPathElevation(graph, path)] = path



        minPathDistance = float('inf')
        maxPathDistance = float('-inf')
        
        
        for path in paths.keys():
            minPathDistance = min(minPathDistance, path)
            maxPathDistance = max(maxPathDistance, path)
            
        if boolIsMax:
            path = paths[maxPathDistance]
        else:
            path = paths[minPathDistance]
            

        getPathLatLong = self.processMapObj.getCoordinates(graph, path)
        getPathLength = self.processMapObj.getPathLength(graph, path)
        getPathElevation = self.processMapObj.getPathElevation(graph, path)
        
        return getPathLatLong, getPathLength, getPathElevation

