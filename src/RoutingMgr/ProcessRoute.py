from src.MapMgr.ProcessMap import ProcessMap
from src.RoutingMgr.Djikstra import Djikstra
from src.RoutingMgr.Astar import Astar


class ProcessRoute(object):

    def __init__(self):
        self.processMapObj = ProcessMap()
        self.djikstraObj = Djikstra()
        self.astarObj = Astar()

    def getPath(self, graph, startNode, endNode, percentage, boolIsMax):

        try:

            pathDjikstra, distanceDjikstra, elevationDjikstra = self.djikstraObj.getRoute(graph, startNode, endNode, percentage, boolIsMax)
            pathAstar, distanceAstar, elevationAstar = self.astarObj.getRoute(graph, startNode, endNode, percentage, boolIsMax)
            
            if boolIsMax:
                if(elevationDjikstra > elevationAstar):
                    return pathDjikstra, distanceDjikstra, elevationDjikstra
                else:
                    return pathAstar, distanceAstar, elevationAstar
            else:
                if (elevationDjikstra < elevationAstar):
                    return pathDjikstra, distanceDjikstra, elevationDjikstra
                else:
                    return pathAstar, distanceAstar, elevationAstar
        except Exception as err:
            raise Exception('Failed to fetch path. Error %s'%err)
