import osmnx 
import pickle as pkl

from osmnx.core import save_to_cache
from osmnx.core import get_from_cache
from osmnx.utils import log


from MapMgr.ProcessMap import ProcessMap

from flask import request, jsonify
'''
Note this file is similar to the Algorithm,py file | copy paste the code over here

'''


class ProcessRoute(object):

    def __init__(self):
        self.processMap = ProcessMap()
        
    
    def getRoute(self):
        payload = request.get_json()
        
        source = payload['source']
        destination  = payload['destination']
        boolIsMax = bool(payload['maxMin']=='max')
        percentage = float(payload['percentage'])
        
        srcParams = self.processMap.processLocationParams(source)
        destParams = self.processMap.processLocationParams(destination)
        
        route, dist, elevation = self.processMap.findRoute(srcParams, destParams, percentage, boolIsMax)
        
        respParams = dict()
        respParams['route'] = route
        respParams['distance'] = dist
        respParams['elevationGain'] = elevation
        
        resp = jsonify(respParams)
        resp.headers.add('Access-Control-Allow-Origin','*')
        return resp 
    
    
    def isLocationValid(self, graph, latitude, longitude):
        _, dist = osmnx.get_nearest_node(graph, (latitude, longitude), return_dist=True)
        if dist > 10000:
            return False
        return True
    
    def getNearestNode(self, graph, latitude, longitude):
        return osmnx.get_nearest_node(graph, latitude, longitude)


    def getPath(self, graph, startNode, endNode, percetage, boolIsMax):
        # write function get_From_djikstra from lasamson
        
        pass 
        
  
    
    
    
    
    