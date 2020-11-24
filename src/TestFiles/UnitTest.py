import unittest

from src.MapMgr.GenerateMap import GenerateMap
from src.MapMgr.ProcessMap import ProcessMap
from src.RoutingMgr.Djikstra import Djikstra
from src.RoutingMgr.Astar import Astar


class Test(unittest.TestCase):

    def setUp(self):
        self.graph = GenerateMap().generateMap('Amherst', 'MA')
        self.generateMapObj = GenerateMap()
        self.processMapObj = ProcessMap()
        self.djikstraObj = Djikstra()

    def tearDown(self):
        pass

    # Checks for Invalid Location
    def testInValidLocation(self):
        self.assertFalse(ProcessMap().isLocationValid(self.graph, float('inf'), float('inf')))

    # Checks for Valid Location
    def testIsValidLocation(self):
        location = 'umass,amherst,ma'
        params = ProcessMap().getLocationParams(location)
        self.assertTrue(ProcessMap().isLocationValid(self.graph, params['latitude'], params['longitude']))

    # Checks for Path elevation
    def testGetPathElevation(self):
        pathElevation = self.processMapObj.getPathElevation(self.graph, self.djikstraObj.getShortestPath(self.graph, 6775672013, 6775672007))
        self.assertEqual(pathElevation, 9)

    # Checks for path length
    def testGetPathLength(self):
        path = self.processMapObj.getPathLength(self.graph, self.djikstraObj.getShortestPath(self.graph, 6775672013, 6775672007))
        self.assertEqual(382.52, path)

    # Checks for valid coordinates
    def testValidCoordinatesOfLocation(self):
        location = 'umass,amherst,ma'
        params = ProcessMap().getLocationParams(location)
        self.assertEqual(params['latitude'], 42.3869382)
        self.assertEqual(params['longitude'], -72.52991477067445)

    # Checks for nearest Node
    def testGetNearestNode(self):
        nearestNode = self.processMapObj.getNearestNode(self.graph, 42.37, -72.51)
        self.assertEqual(nearestNode, 66612947)

    # Checks for Djikstra's Algorithm
    def testDjikstraRoute(self):
        src = 'umass,amherst,ma'
        destination = 'boulder,amherst,ma'
        srcParams = ProcessMap().getLocationParams(src)
        destParams = ProcessMap().getLocationParams(destination)
        startNode = ProcessMap().getNearestNode(self.graph, srcParams['latitude'], srcParams['longitude'])
        endNode = ProcessMap().getNearestNode(self.graph, destParams['latitude'], destParams['longitude'])
        _, dist, elevation = Djikstra().getRoute(self.graph, startNode, endNode, 120, False)
        # Distance Gain
        self.assertEqual(dist, 4417.54)
        # Elevation Gain
        self.assertEqual(elevation, 45)

    # Checks for A* star route length is with the threshold
    def testIsAStarRouteWithinThreshold(self):
        source = 'Boulders, Amherst, MA'
        destination = 'UMass, Amherst, MA'
        srcParams = ProcessMap().getLocationParams(source)
        destParams = ProcessMap().getLocationParams(destination)

        graph = self.graph

        start = ProcessMap().getNearestNode(graph, srcParams['latitude'], srcParams['longitude'])
        end = ProcessMap().getNearestNode(graph, destParams['latitude'], destParams['longitude'])

        minDistance = ProcessMap().getPathLength(graph, Astar().getShortestPath(graph, start, end))

        percentage = 150
        # Any path found should be less than this value
        threshold = (percentage / 100) * minDistance

        _, pathLength, _ = Astar().getRoute(graph, start, end, percentage, isMax=True)

        self.assertTrue(pathLength <= threshold)

    # checks for validity of A* path
    def testAstarValidPath(self):
        source = 'Boulders, Amherst, MA'
        destination = 'UMass, Amherst, MA'
        srcParams = ProcessMap().getLocationParams(source)
        destParams = ProcessMap().getLocationParams(destination)

        graph = self.graph

        start = ProcessMap().getNearestNode(graph, srcParams['latitude'], srcParams['longitude'])
        end = ProcessMap().getNearestNode(graph, destParams['latitude'], destParams['longitude'])

        pathDetails, _, _ = Astar().getRoute(graph, start, end, percentage=123, isMax=True)

        srcDetails = (srcParams['latitude'], srcParams['longitude'])
        destDetails = (destParams['latitude'], destParams['longitude'])

        srcFromAstar = pathDetails[0]
        destFromAstar = pathDetails[1]

        def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
            return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

        # check that if route is computed
        self.assertTrue(len(pathDetails) >= 2)

        # check that a* star route's source and destination longitude and latitude is closer to the input provided
        self.assertTrue(isclose(srcFromAstar[0], srcDetails[0], rel_tol=1e-03))
        self.assertTrue(isclose(srcFromAstar[1], srcDetails[1], rel_tol=1e-03))

        self.assertTrue(isclose(destFromAstar[0], destDetails[0], rel_tol=1e-03))
        self.assertTrue(isclose(destFromAstar[1], destDetails[1], rel_tol=1e-03))


if __name__ == "__main__":
    unittest.main()
