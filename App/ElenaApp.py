from flask_cors import CORS
from flask import Flask, request, jsonify

from geopy.geocoders import Nominatim

class ElenaApp():
    
    def __init__(self):
        self.geolocator = None 
        self.app = None 
        self.initialize_app()
        
    def get_app(self):
        return self.app
    
    def initialize_app(self):
        self.app = Flask(__name__)
        # CORS
        CORS(self.app)
        self.geolocator = Nominatim(user_agent='elena')
    

    def sample(self):
        return 'OK'
    
if __name__ == '__main__':
    app = ElenaApp()
    # Application Object
    appObj = app.get_app()
    # Add URL Rules
    appObj.add_url_rule('/','index',app.sample,methods = ['GET','POST'])
    # Execute the rule
    appObj.run(port=2001)
    
    
    
    