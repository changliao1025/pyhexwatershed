from abc import ABCMeta, abstractmethod
import json
import datetime
from json import JSONEncoder
import numpy as np
from pyearth.system.define_global_variables import *
from osgeo import gdal, osr, ogr
pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class hexwatershed(object):
    __metaclass__ = ABCMeta  
    iFlag_flowline=1
    iFlag_merge_reach=1
    iMesh_type=3    
    iFlag_resample_method=2 
    lMeshID_outlet = -1
    
    #sFilename_flowline=''
    sFilename_dem=''
    sFilename_elevation=''
    sFilename_model_configuration=''
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    
    sWorkspace_data=''
    sWorkspace_scratch=''
    
    sWorkspace_project=''
    
    sWorkspace_simulation=''
    sWorkspace_simulation_flowline=''
    sWorkspace_simulation_case=''
    
    sRegion=''
    sModel=''
    iMesh_type ='hexagon'

    sCase=''
    sDate=''
    

    sFilename_spatial_reference=''
    sFilename_flowline_pystream=''
    def __init__(self, aParameter):
        print('HexWatershed compset is being initialized')
        self.sFilename_model_configuration    = aParameter[ 'sFilename_model_configuration']

        self.sWorkspace_data = aParameter[ 'sWorkspace_data']
        self.sWorkspace_scratch    = aParameter[ 'sWorkspace_scratch']
        self.sWorkspace_project= aParameter[ 'sWorkspace_project']
        self.sWorkspace_bin= aParameter[ 'sWorkspace_bin']
        
        self.sRegion               = aParameter[ 'sRegion']
        self.sModel                = aParameter[ 'sModel']

        #required with default variables

        #optional
        if 'iFlag_flowline' in aParameter:
            self.iFlag_flowline             = int(aParameter[ 'iFlag_flowline'])

        if 'iFlag_resample_method' in aParameter:
            self.iFlag_resample_method             = int(aParameter[ 'iFlag_resample_method'])

        if 'lMeshID_outlet' in aParameter:
            self.lMeshID_outlet             = int(aParameter[ 'lMeshID_outlet'])
        
        #test for numpy array
        
        self.sWorkspace_simulation = self.sWorkspace_scratch + slash + '04model' + slash \
            + self.sModel + slash + self.sRegion +  slash + 'simulation'
        sPath = self.sWorkspace_simulation
        Path(sPath).mkdir(parents=True, exist_ok=True)

       
        iCase_index = int(aParameter['iCase_index'])
        sCase_index = "{:03d}".format( iCase_index )
        sDate   = aParameter[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default

        self.iCase_index =   iCase_index
        sCase = self.sModel  + self.sDate + sCase_index
        self.sCase = sCase

        self.sMesh_type =  aParameter['sMesh_type']
        
        sMesh_type = self.sMesh_type
        if sMesh_type =='hexagon': #hexagon
            self.iMesh_type = 1
        else:
            if sMesh_type =='square': #sqaure
                self.iMesh_type = 2
            else:
                if sMesh_type =='latlon': #latlon
                    self.iMesh_type = 3
                else:
                    if sMesh_type =='mpas': #mpas
                        self.iMesh_type = 4
                    else:
                        if sMesh_type =='tin': #tin
                            self.iMesh_type = 5
                        else:
                            print('Unsupported mesh type?')

        self.sWorkspace_simulation_case = self.sWorkspace_simulation + slash + sCase + slash + self.sMesh_type 
        sPath = self.sWorkspace_simulation_case
        Path(sPath).mkdir(parents=True, exist_ok=True)


        self.sFilename_spatial_reference = aParameter['sFilename_spatial_reference']
        self.sFilename_dem = aParameter['sFilename_dem']


        self.sFilename_mesh = self.sWorkspace_simulation_case + slash + aParameter['sFilename_mesh']    

        self.sFilename_mesh_info  =   self.sWorkspace_simulation_case + slash + aParameter['sFilename_mesh_info']    
        self.sFilename_elevation = self.sWorkspace_simulation_case + slash + aParameter['sFilename_elevation']
        self.sFilename_flowline_info  =   self.sWorkspace_simulation_case + slash + aParameter['sFilename_flowline_info']    

        self.sWorkspace_data_project = self.sWorkspace_data +  slash + self.sWorkspace_project


        self.sFilename_pystream_config = aParameter['sFilename_pystream_config']

        return    
    def save_as_json(self, sFilename_output):
        jsonStr = json.dumps(self.__dict__, cls=NumpyArrayEncoder) 
        #jsonStr = json.dumps(self.__dict__)

        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4, cls=NumpyArrayEncoder)
        
        print(jsonStr)
        return

        return
    def setup(self):
        return
    def run(self):
        return
    def save(self):
        return