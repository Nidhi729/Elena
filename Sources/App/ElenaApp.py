from flask_cors import CORS
from flask import Flask, request, jsonify


from Sources.RoutingMgr.ProcessRoute import ProcessRoute


class ElenaApp():
    
    def __init__(self):
        self.app = None 
        self.initialize_app()
        
        
    def get_app(self):
        return self.app
    
    def initialize_app(self):
        self.app = Flask(__name__)
        # CORS
        CORS(self.app)

    
if __name__ == '__main__':
    app = ElenaApp()
    routeObj = ProcessRoute()
    # Application Object
    appObj = app.get_app()
    # Add URL Rules
    appObj.add_url_rule('/getRoute','route',routeObj.getRoute,methods = ['POST'])
    # Execute the rule
    appObj.run(port=2001)
    
    
    
    