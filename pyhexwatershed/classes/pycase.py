import os
from abc import ABCMeta, abstractmethod
import datetime
import json

from json import JSONEncoder

from pathlib import Path
import numpy as np
from pyflowline.classes.pycase import flowlinecase
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)


class CaseClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, list):
            pass  
        if isinstance(obj, flowlinecase):
            return -1 
            
        return JSONEncoder.default(self, obj)

class hexwatershedcase(object):
    __metaclass__ = ABCMeta  
    iFlag_resample_method=2 
    iFlag_flowline=1
    iFlag_global = 0
    iFlag_multiple_outlet = 0
    iFlag_elevation_profile = 0
    iFlag_stream_burning_topology=1
    iFlag_create_mesh= 1
    iFlag_simplification= 0
    iFlag_intersect= 0
    iFlag_merge_reach=1
    iMesh_type=4   
    iFlag_save_mesh = 0 

    iFlag_use_mesh_dem=0
    nOutlet=1  
    dResolution_degree=0.0
    dResolution_meter=0.0
    dThreshold_small_river=0.0
    dLongitude_left = -180
    dLongitude_right = 180
    dLatitude_bot = -90
    dLatitude_top = 90
    sFilename_dem=''  
    sFilename_model_configuration=''
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    sFilename_basins=''
    
    sWorkspace_data=''   
    
    sWorkspace_project=''
    
    sWorkspace_model_region=''    
    
    
    sRegion=''
    sModel=''
    iMesh_type ='hexagon'

    sCase=''
    sDate=''    

    sFilename_spatial_reference=''
    pPyFlowline = None
    sWorkspace_output_pyflowline=''
    sWorkspace_output_hexwatershed=''
    aBasin = list()


    def __init__(self, aParameter):
        print('HexWatershed compset is being initialized')
        self.sFilename_model_configuration    = aParameter[ 'sFilename_model_configuration']

        if 'sWorkspace_data' in aParameter:
            self.sWorkspace_data = aParameter[ 'sWorkspace_data']
        
        if 'sWorkspace_output' in aParameter:
            self.sWorkspace_output    = aParameter[ 'sWorkspace_output']

        if 'sWorkspace_project' in aParameter:
            self.sWorkspace_project= aParameter[ 'sWorkspace_project']

        if 'sWorkspace_bin' in aParameter:
            self.sWorkspace_bin= aParameter[ 'sWorkspace_bin']

        if 'sRegion' in aParameter:
            self.sRegion               = aParameter[ 'sRegion']

        if 'sModel' in aParameter:
            self.sModel                = aParameter[ 'sModel']
        
        #required with default variables

        if 'iFlag_resample_method' in aParameter:
            self.iFlag_resample_method       = int(aParameter[ 'iFlag_resample_method'])

        if 'iFlag_flowline' in aParameter:
            self.iFlag_flowline             = int(aParameter[ 'iFlag_flowline'])

        if 'iFlag_create_mesh' in aParameter:
            self.iFlag_create_mesh             = int(aParameter[ 'iFlag_create_mesh'])

        if 'iFlag_simplification' in aParameter:
            self.iFlag_simplification             = int(aParameter[ 'iFlag_simplification'])

        if 'iFlag_intersect' in aParameter:
            self.iFlag_intersect             = int(aParameter[ 'iFlag_intersect'])

        if 'iFlag_global' in aParameter:
            self.iFlag_global             = int(aParameter[ 'iFlag_global'])

        if 'iFlag_multiple_outlet' in aParameter:
            self.iFlag_multiple_outlet             = int(aParameter[ 'iFlag_multiple_outlet'])    

        if 'iFlag_use_mesh_dem' in aParameter:
            self.iFlag_use_mesh_dem             = int(aParameter[ 'iFlag_use_mesh_dem'])

        if 'iFlag_stream_burning_topology' in aParameter:
            self.iFlag_stream_burning_topology       = int(aParameter[ 'iFlag_stream_burning_topology'])

        if 'iFlag_save_mesh' in aParameter:
            self.iFlag_save_mesh             = int(aParameter[ 'iFlag_save_mesh'])

        #optional
        if 'iFlag_save_elevation' in aParameter:
            self.iFlag_save_elevation  = int(aParameter[ 'iFlag_save_elevation'])

        if 'iFlag_elevation_profile' in aParameter:
            self.iFlag_elevation_profile  = int(aParameter[ 'iFlag_elevation_profile'])

        if 'nOutlet' in aParameter:
            self.nOutlet             = int(aParameter[ 'nOutlet'])

        if 'dMissing_value_dem' in aParameter:
            self.dMissing_value_dem             = float(aParameter[ 'dMissing_value_dem'])

        if 'dBreach_threshold' in aParameter:
            self.dBreach_threshold             = float(aParameter[ 'dBreach_threshold'])

        if 'dAccumulation_threshold' in aParameter:
            self.dAccumulation_threshold             = float(aParameter[ 'dAccumulation_threshold'])
        
        if 'sFilename_spatial_reference' in aParameter:
            self.sFilename_spatial_reference = aParameter['sFilename_spatial_reference']

        if 'sFilename_dem' in aParameter:
            self.sFilename_dem = aParameter['sFilename_dem']

        if 'sFilename_mesh_netcdf' in aParameter:
            self.sFilename_mesh_netcdf = aParameter['sFilename_mesh_netcdf']

        if 'iCase_index' in aParameter:
            iCase_index = int(aParameter['iCase_index'])
        else:
            iCase_index = 1
        sCase_index = "{:03d}".format( iCase_index )
        self.iCase_index =   iCase_index
        sCase = self.sModel  + self.sDate + sCase_index
        self.sCase = sCase

        sPath = str(Path(self.sWorkspace_output)  /  sCase)
        self.sWorkspace_output = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)
       
        
        sDate   = aParameter[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default

        
        if 'sMesh_type' in aParameter:
            self.sMesh_type =  aParameter['sMesh_type']
        else:
            self.sMesh_type = 'hexagon'
        
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
                            
        if 'dResolution_degree' in aParameter:
            self.dResolution_degree = float(aParameter['dResolution_degree']) 

        if 'dResolution_meter' in aParameter:
            self.dResolution_meter = float(aParameter['dResolution_meter']) 
        else:
            print('Please specify resolution.')

        if 'dLongitude_left' in aParameter:
            self.dLongitude_left = float(aParameter['dLongitude_left']) 

        if 'dLongitude_right' in aParameter:
            self.dLongitude_right = float(aParameter['dLongitude_right']) 

        if 'dLatitude_bot' in aParameter:
            self.dLatitude_bot = float(aParameter['dLatitude_bot']) 

        if 'dLatitude_top' in aParameter:
            self.dLatitude_top = float(aParameter['dLatitude_top']) 

        if 'sJob' in aParameter:
            self.sJob =  aParameter['sJob'] 
        
        self.sWorkspace_data_project = str(Path(self.sWorkspace_data ) / self.sWorkspace_project)
        self.sFilename_elevation = os.path.join(str(Path(self.sWorkspace_output)  ) , sMesh_type + "_elevation.json" )
        self.sFilename_mesh = os.path.join(str(Path(self.sWorkspace_output)  ) , sMesh_type + ".json" )
        self.sFilename_mesh_info  =  os.path.join(str(Path(self.sWorkspace_output)  ) , sMesh_type + "_mesh_info.json"  ) 
                
        if 'sFilename_basins' in aParameter:
            self.sFilename_basins = aParameter['sFilename_basins']
        else:
            self.sFilename_basins = ''              

        sPath = str(Path(self.sWorkspace_output)  /  sCase / 'hexwatershed')
        self.sWorkspace_output_hexwatershed = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        sPath = str(Path(self.sWorkspace_output)  /  sCase / 'pyflowline')
        self.sWorkspace_output_pyflowline = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)
        
        oPyflowline = flowlinecase(aParameter ,  iFlag_standalone_in = 0,\
             sModel_in = 'pyflowline',\
                     sWorkspace_output_in = self.sWorkspace_output_pyflowline)
        self.pPyFlowline = oPyflowline
        return    

    def tojson(self):
        sJson = json.dumps(self.__dict__, \
            sort_keys=True, \
                indent = 4, \
                    ensure_ascii=True, \
                        cls=CaseClassEncoder)
        return sJson

    def export_config_to_json(self, sFilename_output):
        #jsonStr = json.dumps(self.__dict__, cls=NumpyArrayEncoder)         

        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=CaseClassEncoder)
        
        #print(jsonStr)
        return

     
    def setup(self):


        return
    def run_pyflowline(self):



        return
    def run(self):
        return
    def save(self):
        return