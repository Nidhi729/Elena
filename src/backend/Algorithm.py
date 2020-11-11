import osmnx as ox
import Djikstra

def getElevationGain(Graph, start, end):
    if start == end:
        return 0
    return Graph.nodes[start]['elevation'] - Graph.nodes[end]['elevation']

def getPathElevation(Graph, path):
    elevation = 0

    for i in range(len(path) - 1):
        curElevation = getElevationGain(Graph, path[i], path[i + 1])
        if curElevation > 0:
            elevation += curElevation

    return elevation


def getPathLength(Graph, path):
    pathLength = 0

    for i in range(len(path) - 1):
        pathLength += Graph.edges[path[i], path[i+1], 0]['length']

    return pathLength


def getCoordinates(Graph, path):
    coordinates = []
    for nodes in path:
        coordinates.append((Graph.nodes[nodes]['y'], Graph.nodes[nodes]['x']))
    return coordinates


def getRoute(Graph, start, end, percent, maxElevation=True, algo='Djikstra'):

    if algo == "Djikstra":
        return Djikstra.getRoute(Graph, start, end, percent, maxElevation)

    if algo == "Astar":
        return Astar.getRoute(Graph, start, end, percent, maxElevation)


