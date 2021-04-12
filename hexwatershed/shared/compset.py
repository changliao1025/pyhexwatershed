from abc import ABCMeta, abstractmethod
import json

from osgeo import gdal, osr, ogr

class pycompset(object):
    __metaclass__ = ABCMeta  
    iFlag_flowline=1
    iFlag_merge_reach=1
    iFlag_mesh_type=3  #1: tri 2: square 3: lat/lon 4:hexagon 5:mpas    
    iFlag_resample_method=2 
    lMeshID_outlet = -1
    
    sFilename_flowline=''
    sFilename_dem=''

    
    
    def __init__(self, aParameter):
        print('HexWatershed compset is being initialized')
        #self.aParameter = aParameter

        #required with default variables

        #optional
        if 'iFlag_flowline' in aParameter:
            self.iFlag_flowline             = int(aParameter[ 'iFlag_flowline'])

        if 'iFlag_merge_reach' in aParameter:
            self.iFlag_merge_reach             = int(aParameter[ 'iFlag_merge_reach'])

        if 'iFlag_mesh_type' in aParameter:
            self.iFlag_mesh_type             = int(aParameter[ 'iFlag_mesh_type'])

        if 'iFlag_resample_method' in aParameter:
            self.iFlag_resample_method             = int(aParameter[ 'iFlag_resample_method'])

        if 'lMeshID_outlet' in aParameter:
            self.lMeshID_outlet             = int(aParameter[ 'lMeshID_outlet'])
        
        


        return    
    def save_as_json(self, sFilename_output):
        jsonStr = json.dumps(self.__dict__)

        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)
        
        #print(jsonStr)
        return

        return
    def setup(self):
        return
    def run(self):
        return
    def save(self):
        return