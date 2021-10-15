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
    iFlag_resample_method=2 
    iFlag_flowline=1
    iFlag_global = 0
    iFlag_stream_burning_topology=1
    iFlag_merge_reach=1
    iMesh_type=4    

    iFlag_use_mesh_dem=0
    
    #lCellID_outlet = -1    
    
    sFilename_dem=''  
    sFilename_model_configuration=''
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    sFilename_basins=''
    
    sWorkspace_data=''   
    
    sWorkspace_project=''
    
    sWorkspace_model_region=''    
    sWorkspace_output_case=''
    
    sRegion=''
    sModel=''
    iMesh_type ='hexagon'

    sCase=''
    sDate=''    

    sFilename_spatial_reference=''


    def __init__(self, aParameter):
        print('HexWatershed compset is being initialized')
        self.sFilename_model_configuration    = aParameter[ 'sFilename_model_configuration']

        self.sWorkspace_data = aParameter[ 'sWorkspace_data']
        self.sWorkspace_output    = aParameter[ 'sWorkspace_output']
        self.sWorkspace_project= aParameter[ 'sWorkspace_project']
        self.sWorkspace_bin= aParameter[ 'sWorkspace_bin']
        
        self.sRegion               = aParameter[ 'sRegion']
        self.sModel                = aParameter[ 'sModel']
        
        #required with default variables


        if 'iFlag_resample_method' in aParameter:
            self.iFlag_resample_method       = int(aParameter[ 'iFlag_resample_method'])

        if 'iFlag_flowline' in aParameter:
            self.iFlag_flowline             = int(aParameter[ 'iFlag_flowline'])

        if 'iFlag_global' in aParameter:
            self.iFlag_global             = int(aParameter[ 'iFlag_global'])

        if 'iFlag_use_mesh_dem' in aParameter:
            self.iFlag_use_mesh_dem             = int(aParameter[ 'iFlag_use_mesh_dem'])

        if 'iFlag_stream_burning_topology' in aParameter:
            self.iFlag_stream_burning_topology       = int(aParameter[ 'iFlag_stream_burning_topology'])

        #optional
        if 'iFlag_save_elevation' in aParameter:
            self.iFlag_save_elevation  = int(aParameter[ 'iFlag_save_elevation'])

        #if 'lCellID_outlet' in aParameter:
        #    self.lCellID_outlet             = int(aParameter[ 'lCellID_outlet'])

        if 'dMissing_value_dem' in aParameter:
            self.dMissing_value_dem             = float(aParameter[ 'dMissing_value_dem'])

        if 'dBreach_threshold' in aParameter:
            self.dBreach_threshold             = float(aParameter[ 'dBreach_threshold'])

        if 'dAccumulation_threshold' in aParameter:
            self.dAccumulation_threshold             = float(aParameter[ 'dAccumulation_threshold'])
        
        #test for numpy array
        
        self.sWorkspace_model_region = self.sWorkspace_output   + slash \
            + self.sModel + slash + self.sRegion 
        sPath = self.sWorkspace_model_region
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

        self.sWorkspace_output_case = self.sWorkspace_model_region + slash + sCase + slash 
        sPath = self.sWorkspace_output_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_data_project = self.sWorkspace_data +  slash + self.sWorkspace_project
        self.sFilename_spatial_reference = aParameter['sFilename_spatial_reference']
        self.sFilename_dem = aParameter['sFilename_dem']
        self.sFilename_elevation = self.sWorkspace_output_case + slash + sMesh_type + "_elevation.shp"
        self.sFilename_mesh = self.sWorkspace_output_case + slash + sMesh_type + ".shp"
        self.sFilename_mesh_info  =   self.sWorkspace_output_case + slash + sMesh_type + "_mesh_info.json"   
        
        self.sFilename_flowline_info  =   self.sWorkspace_output_case + slash + sMesh_type + "_flowline_info.json"   

        if 'sFilename_basins' in aParameter:
            self.sFilename_basins = aParameter['sFilename_basins']
        else:
            self.sFilename_basins = ''
        
      

        return    
    def save_as_json(self, sFilename_output):
        #jsonStr = json.dumps(self.__dict__, cls=NumpyArrayEncoder) 
        

        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=NumpyArrayEncoder)
        
        #print(jsonStr)
        return

     
    def setup(self):
        return
    def run(self):
        return
    def save(self):
        return