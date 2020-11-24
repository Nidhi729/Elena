import logging

import osmnx as ox

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
            raise Exception('INPUT NOT IN VALID FORMAT or INVALID LOCATION. Desired format Address,Town,State. Error %s' %err)
        
            
    def isLocationValid(self, graph, latitude, longitude):
        logging.log(20,'Validating if point is valid')
        _, dist = ox.get_nearest_node(graph,(latitude, longitude),method='euclidean' , return_dist=True)
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

    
    def getPathElevation(self, graph, path):
        elevation = 0
        for idx in range(len(path)-1):
            currElevation = self.getElevationGain(graph, path[idx], path[idx+1])
            elevation += currElevation if currElevation > 0 else 0 
        return elevation
    

    def getPathLength(self, graph , path):
        pathLength = 0
        for idx in range(1,len(path)):
            pathLength += self.getLength(graph, path[idx-1], path[idx])
        return pathLength
    
    
    def getCoordinates(self,graph, path):
        coord = []
        for node in path:
            coord.append((graph.nodes[node]['y'], graph.nodes[node]['x']))
        return coord



    def getDistFromPercentage(self,deviation, percent):
        if percent:
            return percent / 100.0 * deviation
        return percent * deviation
    