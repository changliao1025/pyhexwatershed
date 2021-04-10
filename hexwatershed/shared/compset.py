from abc import ABCMeta, abstractmethod
import json
import parameter

class compset(object):
    __metaclass__ = ABCMeta  

    iFlag_mesh_type=1



    
    
    def __init__(self, aParameter):


        return    
    def save_as_json(self):
        jsonStr = json.dumps(self.__dict__)

        return
    def setup(self):
        return
    def run(self):
        return
    def save(self):
        return