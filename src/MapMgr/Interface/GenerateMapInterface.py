from abc import ABCMeta, abstractmethod
#from _pyio import __metaclass__


class GenerateMapInterface():
    __metaclass__=ABCMeta
    @abstractmethod
    def test(self):
        pass 
#     
#     def generateMap(self, city, state): 
#         pass 
#     
#     def clearMap(self):
#         pass 
#     
#     def addElevationData(self):
#         pass 
#     