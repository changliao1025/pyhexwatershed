from abc import ABCMeta, abstractmethod

class cell(object):
    __metaclass__ = ABCMeta    
    
    @abstractmethod
    def calculate_cell_area(self, sInput):

        pass
