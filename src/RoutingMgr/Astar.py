'''
Created on Nov 13, 2020

'''
from src.MapMgr.ProcessMap import ProcessMap
import heapq


class Astar(object):
    '''
    classdocs
    '''


    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.processMapObj = ProcessMap()



    # For computing the h cost between two nodes
    def heuristic(self, graph , node, end):
        x1, y1 = graph.nodes[node]['x'], graph.nodes[node]['y']
        x2, y2 = graph.nodes[end]['x'], graph.nodes[end]['y']
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return dist


    def generatePath(self, revPath, start, end):
        path = []
        n = end
        path.append(n)
        while n != start:
            n = revPath[n]
            path.append(n)
        return path[::-1]

    def getShortestPath(self, G, start, end, option='length'):
        queue = []
        heapq.heappush(queue, (0, start))
        revPath = {}
        cost = {}
        revPath[start] = None
        cost[start] = 0

        while len(queue) > 0:
            (val, current) = heapq.heappop(queue)
            if current == end:
                break
            for cur, nxt, data in G.edges(current, data=True):
                cur_cost = cost[current]
                if option == 'length':
                    curCost = G.edges[cur, nxt, 0]['length']
                elif option == 'elevation':
                    curCost = self.processMapObj.getPathElevation(G, cur, nxt)
                if curCost > 0:
                    cur_cost += curCost
                if nxt not in cost or cur_cost < cost[nxt]:
                    cost[nxt] = cur_cost
                    heapq.heappush(queue, (cur_cost, nxt))
                    revPath[nxt] = current

        return self.generatePath(revPath, start, end)



    def getRoute(self, graph, start, end, percentage, isMax=True):
        # get the shortest path
        minDistance = self.processMapObj.getPathLength(graph, self.getShortestPath(graph, start, end))
        #print("shortest path length: ", minDistance)

        # Any path found should be less than this value
        threshold = (percentage/100) * minDistance
        print("Max Route Length:", threshold)

        closed = set()
        open = set()

        open.add(start)

        # for storing the parent of every node
        parent = {}
        parent[start] = None

        # for storing the g and h cost of the nodes
        node_costs = {}
        node_costs[start] = {}
        node_costs[start]['g'] = 0
        node_costs[start]['h'] = 0

        # for storing all the routes found
        routes = []


        def getNextNode(nodes, node_costs):
            return min(nodes, key = lambda item: sum(node_costs[item].values()))



        while open:
            current = getNextNode(open, node_costs)
            open.remove(current)

            if current == end:
                if node_costs[current]['g'] <= threshold:
                    path = []
                    path_node = current
                    while path_node is not None:
                        path.append(path_node)
                        path_node = parent[path_node]
                    path.reverse()

                    elevation_p = self.processMapObj.getPathElevation(graph, path)
                    path_elevation = -1*elevation_p if isMax else elevation_p
                    path_length = self.processMapObj.getPathLength(graph, path)
                    path_details = self.processMapObj.getCoordinates(graph, path)

                    print("found a path with length = " + str(node_costs[current]['g']) + " and elevation = " + str(elevation_p))

                    heapq.heappush(routes, (path_elevation, path_length, path_details))

                    #reset final node length
                    node_costs[current]['g'] = float('inf')
                else:
                    # Found route exceeding threshold
                    break
            else:
                closed.add(current)
                for neighbor in graph[current]:
                    if neighbor in closed:
                        continue

                    if neighbor in open:
                        old_neighbor_g_cost = node_costs[neighbor]['g']

                        current_g_cost = node_costs[current]['g']
                        current_move_cost = graph.edges[current, neighbor, 0]['length']

                        new_neighbor_g_cost = current_g_cost + current_move_cost

                        if old_neighbor_g_cost > new_neighbor_g_cost:
                            node_costs[neighbor]['g'] = new_neighbor_g_cost
                            parent[neighbor] = current
                    else:
                        current_g_cost = node_costs[current]['g']
                        current_move_cost = graph.edges[current, neighbor, 0]['length']

                        neighbor_g_cost = current_g_cost + current_move_cost
                        neighbor_h_cost = self.heuristic(graph, current, end)

                        parent[neighbor] = current
                        node_costs[neighbor] = {}
                        node_costs[neighbor]['g'] = neighbor_g_cost
                        node_costs[neighbor]['h'] = neighbor_h_cost
                        open.add(neighbor)

        if routes:
            path_elevation, path_length, path_details = heapq.heappop(routes)
            if isMax: path_elevation *= -1
            return path_details, path_length, path_elevation


        raise ValueError('No path found between the start and end locations.')
