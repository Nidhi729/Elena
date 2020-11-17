from abc import ABCMeta, abstractmethod


class GenerateMapInterface(ABCMeta):
    __metaclass__ = ABCMeta
   
    @abstractmethod
    def generateMap(self): 
        pass 
    @abstractmethod
    def clearMap(self):
        pass 
    
    @abstractmethod
    def addElevationData(self):
        pass 
    