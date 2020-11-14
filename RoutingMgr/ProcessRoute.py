from MapMgr.ProcessMap import ProcessMap

from flask import request, jsonify


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
        
        route, dist, elevation = self.findRoute(srcParams, destParams, percentage, boolIsMax)
        
        
    def findRoute(self, srcParams, destParams, percentage, isMax):
        pass 