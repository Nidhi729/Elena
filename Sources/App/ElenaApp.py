from flask_cors import CORS
from flask import Flask, request, jsonify


from Sources.RoutingMgr.ProcessRoute import ProcessRoute
from Sources.MapMgr.GenerateMap import GenerateMap
from Sources.MapMgr.ProcessMap import ProcessMap


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
        
        
    def getRoute(self):
        payload = request.get_json()
        print(payload)
        source = payload['Source']
        destination  = payload['Destination']
        boolIsMax = bool(payload['Max_min']=='max')
        percentage = float(payload['Percentage'])
        
        srcParams = self.processMapObj.processLocationParams(source)
        destParams = self.processMapObj.processLocationParams(destination)
        
        route, dist, elevation = self.findRoute(srcParams, destParams, percentage, boolIsMax)
        
        respParams = dict()
        respParams['route'] = route
        respParams['distance'] = dist
        respParams['elevationGain'] = elevation
        
        resp = jsonify(respParams)
        resp.headers.add('Access-Control-Allow-Origin','*')
        return resp 
        
    def findRoute(self, srcParams, destParams, percentage, boolIsMax):
        graph, projectedGraph =  self.genMapObj.generateMap()
        
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
    # Add URL Rules
    appObj.add_url_rule('/get_route','route',app.getRoute,methods = ['POST'])
    # Execute the rule
    appObj.run(port=8080)
    
    
    
    