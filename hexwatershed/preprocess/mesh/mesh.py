
from abc import ABCMeta, abstractmethod
class mesh(object):
    """Abstract base class for
    """
    aParameter = {}
    dLatitude_bot = -90
    dLatitude_top = 90
    dLongitude_left = -180
    dLongitude_right = 180
    aRectangle=[]
    sFilename_mesh=''
    __metaclass__ = ABCMeta    
    @abstractmethod
    def __init__(self, aParameter):

        pass
    @abstractmethod
   
    def calculate_mesh_area(self):

        pass