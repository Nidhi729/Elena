import osmnx 
import heapq
import collections
import pickle as pkl


from Sources.MapMgr.ProcessMap import ProcessMap

from flask import request, jsonify

class ProcessRoute(object):

    def __init__(self):
        self.processMapObj = ProcessMap()
        
    
#     def getRoute(self):
#         payload = request.get_json()
#         
#         source = payload['source']
#         destination  = payload['destination']
#         boolIsMax = bool(payload['maxMin']=='max')
#         percentage = float(payload['percentage'])
#         
#         srcParams = self.processMapObj.processLocationParams(source)
#         destParams = self.processMapObj.processLocationParams(destination)
#         
#         route, dist, elevation = self.processMapObj.findRoute(srcParams, destParams, percentage, boolIsMax)
#         
#         respParams = dict()
#         respParams['route'] = route
#         respParams['distance'] = dist
#         respParams['elevationGain'] = elevation
#         
#         resp = jsonify(respParams)
#         resp.headers.add('Access-Control-Allow-Origin','*')
#         return resp 
    
    
#     
#     
#     def get_from_djikstra(G, start, end, percent, max_ele=True):
#         min_distance = get_path_length(G, get_shortest_path(G, start, end))
#         max_path_length = get_dis_from_percentage(min_distance, percent)
#         candidate_paths = {}
#         floored_percent = (percent / 10) * 10
#         iters = []
#         i = 100
#         while (i <= floored_percent):
#             iters.append(i)
#             i += 10
#             # print(i)
#     
#         for length in iters:
#             pat_len = get_dis_from_percentage(min_distance, length)
#             queue = []
#             heappush(queue, (0, start))
#             revPath = {}
#             cost = {}
#             cost_ele = {}
#             revPath[start] = None
#             cost[start] = 0
#             cost_ele[start] = 0
#             while len(queue) != 0:
#                 (val, cur) = heappop(queue)
#                 if cur == end:
#                     if cost[cur] <= pat_len:
#                         break
#                 for cur, nxt, data in G.edges(cur, data=True):
#                     cur_cost = cost[cur] + get_length(G, cur, nxt)
#                     cur_ecost = cost_ele[cur]
#                     ecost = get_elevation_gain(G, cur, nxt)
#                     if ecost > 0:
#                         cur_ecost = cur_ecost + ecost
#                     if nxt not in cost or cur_cost < cost[nxt]:
#                         cost_ele[nxt] = cur_ecost
#                         cost[nxt] = cur_cost
#                         if max_ele:
#                             priority = -cur_ecost
#                         else:
#                             priority = cur_ecost
#                         heappush(queue, (priority, nxt))
#                         revPath[nxt] = cur
#             path = generate_path(revPath, start, end)
#             print(get_path_elevation(G, path))
#             candidate_paths[get_path_elevation(G, path)] = path
#     
#         min_path_len = 10 ** 6
#         max_path_len = 0
#     
#         for el in candidate_paths.keys():
#             if el <= min_path_len:
#                 min_path_len = el
#             if el >= max_path_len:
#                 max_path_len = el
#     
#         if max_ele:
#             path = candidate_paths[max_path_len]
#         else:
#             path = candidate_paths[min_path_len]
#     
#         return get_lat_long(G, path), get_path_length(G, path), get_path_elevation(G, path)
#     
#         
    

    def getPath(self, graph, startNode, endNode, percetage, boolIsMax=True):
        minDistance = self.processMapObj.getPathLength(graph, self.processMapObj.getShortestPath(graph, startNode, endNode))
        #min_distance = get_path_length(G, get_shortest_path(G, start, end))
        maxPathLength = self.processMapObj.getDistFromPercentage(minDistance, percetage)
        #max_path_length = get_dis_from_percentage(min_distance, percent)
        candidatePath = dict()
        
        #candidate_paths = {}
        #floored_percent = (percent / 10) * 10
        iters = []
        i = 100
        while (i <= (percetage / 10) * 10):
            iters.append(i)
            i += 10
            
        for length in iters:
            pat_len = self.processMapObj.getDistFromPercentage(minDistance, percetage)
            queue = []
            heapq.heappush(queue, (0, startNode))
            revPath = {}
            cost = {}
            cost_ele = {}
            revPath[startNode] = None
            cost[startNode] = 0
            cost_ele[startNode] = 0
            while len(queue) != 0:
                (val, cur) = heapq.heappop(queue)
                if cur == endNode:
                    if cost[cur] <= pat_len:
                        break
                for cur, nxt, data in graph.edges(cur, data=True):
                    cur_cost = cost[cur] + self.processMapObj.getLength(graph, cur, nxt)
                    cur_ecost = cost_ele[cur]
                    ecost = self.processMapObj.getElevationGain(graph, cur, nxt)
                    if ecost > 0:
                        cur_ecost = cur_ecost + ecost
                    if nxt not in cost or cur_cost < cost[nxt]:
                        cost_ele[nxt] = cur_ecost
                        cost[nxt] = cur_cost
                        if boolIsMax:
                            priority = -cur_ecost
                        else:
                            priority = cur_ecost
                        heapq.heappush(queue, (priority, nxt))
                        revPath[nxt] = cur
            path = self.processMapObj.generatePath(revPath, startNode, endNode)
            #print(get_path_elevation(G, path))
            candidatePath[self.processMapObj.getPathElevation(graph, path)] = path
    
        min_path_len = 10 ** 6
        max_path_len = 0
    
        for el in candidatePath.keys():
            if el <= min_path_len:
                min_path_len = el
            if el >= max_path_len:
                max_path_len = el
    
        if boolIsMax:
            path = candidatePath[max_path_len]
        else:
            path = candidatePath[min_path_len]
    
    
        getPathLatLong = self.processMapObj.getLatLong(graph, path)
        getPathLength = self.processMapObj.getPathLength(graph, path)
        getPathElevation = self.processMapObj.getPathElevation(graph, path)
        
        return getPathLatLong, getPathLength, getPathElevation
    