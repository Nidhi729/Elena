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
    
    
    