import unittest

from src.MapMgr.GenerateMap import GenerateMap

from src.MapMgr.ProcessMap import ProcessMap

from src.RoutingMgr.Djikstra import Djikstra


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = GenerateMap().generateMap('Amherst', 'MA')


    def tearDown(self):
        pass

# 
    def testInValidLocation(self):
        self.assertFalse(ProcessMap().isLocationValid(self.graph, float('inf'), float('inf')))
          
    def testIsValidLocation(self):
        location = 'umass,amherst,ma'
        params = ProcessMap().getLocationParams(location)
        self.assertTrue(ProcessMap().isLocationValid(self.graph, params['latitude'], params['longitude']))
    
    
    def testValidCoordinatesOfLocation(self):
        location = 'umass,amherst,ma'
        params = ProcessMap().getLocationParams(location)
        self.assertEqual(params['latitude'], 42.3869382)
        self.assertEqual(params['longitude'], -72.52991477067445)
        
    
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

if __name__ == "__main__":
    unittest.main()