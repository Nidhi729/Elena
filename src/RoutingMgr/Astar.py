'''
Created on Nov 13, 2020

'''
from src.MapMgr.ProcessMap import ProcessMap

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
    def heuristic(self, graph , nodeA, nodeB):
        return self.processMapObj.getElevationGain(graph, nodeA, nodeB)



    def getRoute(self, graph, start, end, percentage, isMax=True):
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


        def getNextNode(nodes, node_costs, isMax):
            return max(nodes, key = lambda item: sum(node_costs[item].values())) if isMax else min(nodes, key = lambda item: sum(node_costs[item].values()))



        while open:
            current = getNextNode(open, node_costs, isMax)
            open.remove(current)

            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return self.processMapObj.getCoordinates(graph, path), self.processMapObj.getPathLength(graph, path), self.processMapObj.getPathElevation(graph, path)

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
                    neighbor_h_cost = self.heuristic(graph, current, neighbor)

                    parent[neighbor] = current
                    node_costs[neighbor] = {}
                    node_costs[neighbor]['g'] = neighbor_g_cost
                    node_costs[neighbor]['h'] = neighbor_h_cost
                    open.add(neighbor)

        raise ValueError('No path found between the start and end locations.')
