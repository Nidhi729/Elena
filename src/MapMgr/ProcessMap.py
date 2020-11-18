import osmnx as ox
import networkx as nx
import logging
import heapq
import collections
from geopy.geocoders import Nominatim

from src.MapMgr.GenerateMap import GenerateMap

class ProcessMap(object):
    '''
    Class to interact with osmnx api and translate address to required format
    '''
    def __init__(self):
        self.geolocator = Nominatim(user_agent='elena')
        self.genMapObj = GenerateMap()
        
    
    def getLocationParams(self, location):
        try:
            locationParams = location.split(',') 
            params = dict()
            params['town'] = locationParams[1].strip()
            params['state'] = locationParams[2].strip()
            params['latitude'] = self.geolocator.geocode(location).latitude
            params['longitude'] = self.geolocator.geocode(location).longitude
            return params
        except Exception as err:
            raise Exception('INPUT NOT IN VALID FORMATE. Desired format Address,Town,State. Error %s' %err)
        
            
    def isLocationValid(self, graph, latitude, longitude):
        logging.log(20,'Validating if point is valid')
        _, dist = ox.get_nearest_node(graph, (latitude, longitude), return_dist=True)
        if dist > 10000: # Distance from the nearest node
            logging.log(40,'The location is not within 10000 nodes from the nearest node')
            return False
        logging.log(20,'Valid location')
        return True
    
    def getNearestNode(self, graph, latitude, longitude):
        return ox.get_nearest_node(graph, (latitude, longitude))
    
    def getElevationGain(self, graph, startNode, endNode):
        if startNode == endNode:
            return 0
        return graph.nodes[startNode]['elevation'] - graph.nodes[endNode]['elevation']

    def getLength(self,graph, start, end):
        return graph.edges[start, end, 0]['length']
    
    
    def getpath(self, revPath, origin, destination):
        route_by_length_minele = []
        p = destination
        route_by_length_minele.append(p)
        while p != origin:
            p = revPath[p]
            route_by_length_minele.append(p)
        route_by_length_minele = route_by_length_minele[::-1]
        return route_by_length_minele
    
    
    def generatePath(self, revPath, start, end):
        path = []
        n = end
        path.append(n)
        while n != start:
            n = revPath[n]
            path.append(n)
        return path[::-1]
    
    
    def getPathElevation(self, graph, path):
        total_elevation = 0
    
        for i in range(len(path) - 1):
            curr_elevation = self.getElevationGain(graph, path[i], path[i + 1])
            if curr_elevation > 0:
                total_elevation += curr_elevation
    
        return total_elevation


    def getPathLength(self, graph , path):
        total_length = 0
    
        for i in range(len(path) - 1):
            total_length += self.getLength(graph, path[i], path[i + 1])
    
        return total_length

    
    def getLatLong(self,graph, path):
        coord = []
        for node in path:
            coord.append((graph.nodes[node]['y'], graph.nodes[node]['x']))
        return coord


    def getShortestPath(self, graph, start, end, option='length'):
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
            for cur, nxt, data in graph.edges(current, data=True):
                cur_cost = cost[current]
                if option == 'length':
                    curCost = self.getLength(graph, cur, nxt)
#                 elif option == 'elevation':
#                     # this part mostly doesn't even work
#                     curCost = self.getPathElevation(graph, cur, nxt)
                if curCost > 0:
                    cur_cost += curCost
                if nxt not in cost or cur_cost < cost[nxt]:
                    cost[nxt] = cur_cost
                    heapq.heappush(queue, (cur_cost, nxt))
                    revPath[nxt] = current
    
        return self.generatePath(revPath, start, end)
    

    def getEucledeanDistance(self, graph, start, end):
        x1, y1 = graph.nodes()[start]['x'], graph.nodes()[start]['y']
        x2, y2 = graph.nodes()[end]['x'], graph.nodes()[end]['y']
    
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
        return dist
    

    def getFromAllPaths(self,G, start, end, percent, max_ele=True):
        min_distance = self.getPathLength(G, self.getShortestPath(G, start, end))
        shortest_paths = list(nx.all_shortest_paths(G, start, end))
    
        print(percent)
        max_path_length = (1.0 + float(percent)) * min_distance
    
        elevation_gain = {}
        for p in shortest_paths:
            path_dist = self.getPathLength(G, p)
            if path_dist > max_path_length:
                print(min_distance, max_path_length)
                continue
            elevation_gain[self.getPathElevation(G, p)] = p
    
        ordered_paths = collections.OrderedDict(sorted(elevation_gain.items()))
    
        keys = ordered_paths.keys()
    
        if max_ele:
            key = max(elevation_gain.iterkeys(), key=(lambda key: elevation_gain[key]))
        else:
            key = min(elevation_gain.iterkeys(), key=(lambda key: elevation_gain[key]))
    
        return elevation_gain[key], self.getPathElevation(G, elevation_gain[key]), self.getPathLength(G, elevation_gain[key])
    

    def getDistFromPercentage(self,min_distance, percent):
        if percent > 1:
            return (percent) / 100.0 * min_distance
        return (percent) * min_distance

    
#     def findRoute(self, srcParams, destParams, percentage, boolIsMax):
#         graph, projectedGraph =  self.genMapObj.generateMap()
#         
#         if not self.isLocationValid(graph, srcParams['latitude'], srcParams['longitude']):
#             raise Exception('INVALID SOURCE')
#         
#         if not self.isLocationValid(graph, destParams['latitude'], destParams['longitude']):
#             raise Exception('INVALID DESTINATION')
#         
#         
#         startNode = self.getNearestNode(graph, srcParams['latitude'], srcParams['longitude'])
#         endNode = self.getNearestNode(graph, destParams['latitude'], destParams['longitude'])
#         
#         
#         return self.processRouteObj.getPath(graph, startNode, endNode, percentage, boolIsMax)
#         # Need to load by the algo and other things to get the main code base up and running
#         
#         # Check if start and end point with in amherst regious
#         
    
    
    