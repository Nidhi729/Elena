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
        
  
    
    
    
    
    