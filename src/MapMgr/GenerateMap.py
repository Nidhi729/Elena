import osmnx 
import pickle as pkl
import os

import math
import time
import requests
import pathlib
import pandas as pd
import networkx as nx

from osmnx.core import save_to_cache
from osmnx.core import get_from_cache
from osmnx.utils import log

osmnx.config(log_file=True, log_console=True, use_cache=True)

from src.MapMgr.Interface import GenerateMapInterface


class GenerateMap():
    def __init__(self):
        self.PklFileName = '%s_%s.pkl'
        self.OpenElevationApiURL = 'https://api.open-elevation.com/api/v1/lookup?locations={}'

        
    def generateGraphPlot(self, graph):
        osmnx.log('Generating graph based on elevation !')
        nc = osmnx.plot.get_node_colors_by_attr(graph, 'elevation',cmap='plasma')
        osmnx.plot_graph(graph,node_size=5,edge_color='#333333', bgcolor='k')
        
    
    def generateMap(self, city='Amherst', state='MA'):
        mapFileName = self.PklFileName%(city,state)
        mapFilePath = pathlib.Path(mapFileName)
        
        if mapFilePath.is_file():
            return pkl.load(open(mapFileName, "rb"))
        else:
            params = dict()
            params['city']  = city
            params['state'] = state
            params['country'] = 'USA'
            # Osmnx to get the map
            graph = osmnx.graph_from_place(params, network_type='drive')
            graph = self.add_node_elevations_open(graph)
            graph = osmnx.add_edge_grades(graph)
            # Dump the file
            #self.generateGraphPlot(graph)
            pkl.dump(graph, open(mapFileName, "wb"))
            return graph
    
    
    def add_node_elevations_open(self, G, max_locations_per_batch=180,
                                 pause_duration=0.02):  # pragma: no cover
    
        url_template = 'https://api.open-elevation.com/api/v1/lookup?locations={}'
        node_points = pd.Series({node: '{:.5f},{:.5f}'.format(data['y'], data['x']) for node, data in G.nodes(data=True)})
        
        log('Requesting node elevations from the API in {} calls.'.format(
            math.ceil(len(node_points) / max_locations_per_batch)))
    
        results = []
        for i in range(0, len(node_points), max_locations_per_batch):
            chunk = node_points.iloc[i: i + max_locations_per_batch]
            locations = '|'.join(chunk)
            url = url_template.format(locations)
            log(len(url))
            # check if this request is already in the cache (if global use_cache=True)
            cached_response_json = get_from_cache(url)
            if cached_response_json is not None:
                response_json = cached_response_json
            else:
                try:
                    # request the elevations from the API
                    log('Requesting node elevations: {}'.format(url))
                    time.sleep(pause_duration)
                    response = requests.get(url)
                    response_json = response.json()
                    save_to_cache(url, response_json)
                except Exception as e:
                    log(e)
                    log('Server responded with {}: {}'.format(response.status_code, response.reason))
    
            # append these elevation results to the list of all results
            results.extend(response_json['results'])
    
        # sanity check that all our vectors have the same number of elements
        if not (len(results) == len(G.nodes()) == len(node_points)):
            raise Exception('Graph has {} nodes but we received {} results from the elevation API.'.format(len(G.nodes()),
                                                                                                           len(results)))
        else:
            log('Graph has {} nodes and we received {} results from the elevation API.'.format(len(G.nodes()),
                                                                                               len(results)))
    
        # add elevation as an attribute to the nodes
        df = pd.DataFrame(node_points, columns=['node_points'])
        df['elevation'] = [result['elevation'] for result in results]
        log(df['elevation'])
        df['elevation'] = df['elevation'].round(3)  # round to millimeter
        nx.set_node_attributes(G, name='elevation', values=df['elevation'].to_dict())
        log('Added elevation data to all nodes.')
    
        return G

    def clearPklFiles(self, city, state):
        mapFileName = '%s_%s.pkl'%(city,state)
        projectedFileName = '%s_%s_projection.pkl' %(city,state)
    
        os.remove(mapFileName)
        os.remove(projectedFileName)