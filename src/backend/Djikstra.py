import Algorithm
import networkx as nx
from heapq import *
import sys

def generatePath(revPath, start, end):
    path = []
    n = end
    path.append(n)
    while n != start:
        n = revPath[n]
        path.append(n)
    return path[::-1]


def shortestPath(G, start, end, option='length'):
    queue = []
    heappush(queue, (0, start))
    revPath = {}
    cost = {}
    revPath[start] = None
    cost[start] = 0

    while len(queue) > 0:
        (val, current) = heappop(queue)
        if current == end:
            break
        for cur, nxt, data in G.edges(current, data=True):
            cur_cost = cost[current]
            if option == 'length':
                curCost = G.edges[cur, nxt, 0]['length']
            elif option == 'elevation':
                curCost = Algorithm.getPathElevation(G, cur, nxt)
            if curCost > 0:
                cur_cost += curCost
            if nxt not in cost or cur_cost < cost[nxt]:
                cost[nxt] = cur_cost
                heappush(queue, (cur_cost, nxt))
                revPath[nxt] = current

    return generatePath(revPath, start, end)



def getRoute(Graph, start, end, percent, maxElevation=True):

    if start not in Graph or end not in Graph:
        msg = 'Either source {} or target {} is not in G'
        raise nx.NodeNotFound(msg.format(start, end))

    minDistance = Algorithm.getPathLength(Graph, shortestPath(Graph, start, end))
    flooredPercent = (percent / 10) * 10


    for length in range(100, int(flooredPercent)+1, 10):
        queue = []
        heappush(queue, (0, start))
        revPath = {}
        cost = {}
        costEle = {}
        revPath[start] = None
        cost[start] = 0
        costEle[start] = 0

        minPathLen = sys.maxint
        maxPathLen = 0
        pathMin = sys.maxint
        pathMax = 0

        while len(queue) != 0:
            (val, cur) = heappop(queue)
            if cur == end and (cost[cur] <= ((percent) / 100.0 * minDistance if percent>1 else (percent) * minDistance)):
                break
            for curNode, nextNode, data in Graph.edges(cur, data=True):
                curCost = cost[curNode] + Graph.edges[curNode, nextNode, 0]['length']
                curElevcost = costEle[curNode]
                ecost = Algorithm.getElevationGain(Graph, curNode, nextNode)
                if ecost > 0:
                    curElevcost +=  ecost
                if nextNode not in cost or curCost < cost[nextNode]:
                    costEle[nextNode] = curElevcost
                    cost[nextNode] = curCost
                    preference = -curElevcost if maxElevation else curElevcost
                    heappush(queue, (preference, nextNode))
                    revPath[nextNode] = curNode

        path = generatePath(revPath, start, end)
        value = Algorithm.getPathElevation(Graph, path)

        if(minPathLen >= value):
            pathMin = path
            minPathLen = value
        if(maxPathLen <= value):
            pathMax = path
            maxPathLen = value

    path  = pathMax if maxElevation else pathMin

    return Algorithm.getCoordinates(Graph, path), Algorithm.getPathLength(Graph, path), Algorithm.getPathElevation(Graph, path)
