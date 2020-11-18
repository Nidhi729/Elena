import heapq
import collections

from src.MapMgr.ProcessMap import ProcessMap

class ProcessRoute(object):

    def __init__(self):
        self.processMapObj = ProcessMap()
        

    def getPath(self, graph, startNode, endNode, percetage, boolIsMax=True):
        
        minDistance = self.processMapObj.getPathLength(graph, self.processMapObj.getShortestPath(graph, startNode, endNode))
        candidatePath = dict()

        for _ in range(100, int(percetage)+10,10):
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

            path = self.processMapObj.generatePath(revPath, startNode, endNode)
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
    
    
        getPathLatLong = self.processMapObj.getLatLong(graph, path)
        getPathLength = self.processMapObj.getPathLength(graph, path)
        getPathElevation = self.processMapObj.getPathElevation(graph, path)
        
        return getPathLatLong, getPathLength, getPathElevation
    