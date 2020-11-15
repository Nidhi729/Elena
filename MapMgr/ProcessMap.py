from geopy.geocoders import Nominatim

from RoutingMgr.ProcessRoute import ProcessRoute

from MapMgr.GenerateMap import GenerateMap

class ProcessMap(object):
    '''
    Class to interact with osmnx api and translate address to required format
    '''
    def __init__(self):
        self.geolocator = Nominatim(user_agent='elena')
        self.genMapObj = GenerateMap()
        self.processRouteObj = ProcessRoute()
        
    
    def processLocationParams(self, location):
        locationParams = location.split(',')
        
        params = dict()
        params['town'] = locationParams[1].strip()
        params['state'] = locationParams[2].strip()
        params['latitude'] = self.geolocator.geocode(location).latitude
        params['longitude'] = self.geolocator.geocode(location).longitude
        
        return params
    
    def findRoute(self, srcParams, destParams, percentage, boolIsMax):
        graph, projectedGraph =  self.genMapObj.generateMap()
        
        if not self.processRouteObj.isLocationValid(graph, srcParams['latitude'], srcParams['longitude']):
            raise Exception('INVALID SOURCE')
        
        if not self.processRouteObj.isLocationValid(graph, destParams['latitude'], destParams['longitude']):
            raise Exception('INVALID SOURCE')
        
        
        startNode = self.processRouteObj.getNearestNode(graph, srcParams['latitude'], srcParams['longitude'])
        endNode = self.processRouteObj.getNearestNode(graph, destParams['latitude'], destParams['longitude'])
        
        
        return self.processRouteObj.getPath(graph, startNode, endNode, percentage, boolIsMax)
        # Need to load by the algo and other things to get the main code base up and running
        
        # Check if start and end point with in amherst regious
        
    
    
    