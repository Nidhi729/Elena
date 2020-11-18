from flask_cors import CORS
from flask import Flask, request, jsonify




from src.RoutingMgr.ProcessRoute import ProcessRoute
from src.MapMgr.GenerateMap import GenerateMap
from src.MapMgr.ProcessMap import ProcessMap

import logging
from flask_swagger import swagger

class ElenaApp():
    
    def __init__(self):
        self.app = None 
        self.initialize_app()
        self.genMapObj = GenerateMap()
        self.processMapObj = ProcessMap()
        self.processRouteObj = ProcessRoute()

        
    def get_app(self):
        return self.app
    
    def initialize_app(self):
        self.app = Flask(__name__)
        
        # CORS
     
        CORS(self.app)
        
        
    def spec(self):
        return jsonify(swagger(self.app))
        
    def getRoute(self):
        try:
            
            payload = request.get_json()
            source = payload['Source']
            destination  = payload['Destination']
            boolIsMax = bool(payload['Max_min']=='max')
            percentage = float(payload['Percentage'])
            
            srcParams = self.processMapObj.getLocationParams(source)
            destParams = self.processMapObj.getLocationParams(destination)
            
            route, dist, elevation = self.findRoute(srcParams, destParams, percentage, boolIsMax)
            
            respParams = dict()
            respParams['Route'] = route
            respParams['Distance'] = dist
            respParams['Elevation Gain'] = elevation
        
        except Exception as err:
            print(err)
            respParams = dict()
            respParams['Error'] = 'Failed to fetch route. Error : %s' %err 
            
        print(respParams)
        resp = jsonify(respParams)
        resp.headers.add('Access-Control-Allow-Origin','*')
        
        return resp 
        
    def findRoute(self, srcParams, destParams, percentage, boolIsMax):
        graph =  self.genMapObj.generateMap()
        
        if not self.processMapObj.isLocationValid(graph, srcParams['latitude'], srcParams['longitude']):
            raise Exception('INVALID SOURCE')
        
        if not self.processMapObj.isLocationValid(graph, destParams['latitude'], destParams['longitude']):
            raise Exception('INVALID DESTINATION')
        
        startNode = self.processMapObj.getNearestNode(graph, srcParams['latitude'], srcParams['longitude'])
        endNode = self.processMapObj.getNearestNode(graph, destParams['latitude'], destParams['longitude'])
        
        return self.processRouteObj.getPath(graph, startNode, endNode, percentage, boolIsMax)

    
if __name__ == '__main__':
    app = ElenaApp()
    
#     routeObj = ProcessRoute()
    # Application Object
    appObj = app.get_app()
    
    appObj.add_url_rule('/','swagger',app.spec)
    # Add URL Rules
    appObj.add_url_rule('/getRoute','route',app.getRoute,methods = ['POST'])
    # Execute the rule
    appObj.run(port=8080)
    
    
    
    