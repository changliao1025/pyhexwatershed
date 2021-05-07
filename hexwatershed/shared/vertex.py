from abc import ABCMeta, abstractmethod
import numpy as np

class pyvertex(object):
    __metaclass__ = ABCMeta  
    dX=0.0
    dY=0.0
    dZ=0.0
    dLongitude=0.0
    dLatitude=0.0
    def __init__(self, aParameter):
        if 'x' in aParameter:            
            self.dX             = float(aParameter['x'])
        
        if 'y' in aParameter:            
            self.dX             = float(aParameter['y'])
        
        if 'lon' in aParameter:            
            self.dLongitude      = float(aParameter['lon'])
        
        if 'lat' in aParameter:            
            self.dLatitude       = float(aParameter['lat'])

        return
    
    def __eq__(self, other):
        iFlag = -1
        
        c = self.calculate_distance(other)
        if( c < 0.0000001 ):
            iFlag= 1
        else:
            iFlag= 0       

        return iFlag
    
    def calculate_distance(self, other):
        dDistance=0.0
        x1 = self.dX
        y1 = self.dY
        x2 = other.dX
        y2 = other.dY
        a = (x1-x2) * (x1-x2)
        b = (y1-y2) * (y2-y2)
        c = np.sqrt(a+b)

        dDistance = c

        return dDistance

