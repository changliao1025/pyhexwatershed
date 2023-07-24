import os
import stat
import platform
import pkg_resources
import datetime
import importlib
import json
from shutil import copy2
import subprocess
from json import JSONEncoder
from pathlib import Path
from osgeo import gdal, ogr, osr, gdalconst
import numpy as np
from pyflowline.classes.pycase import flowlinecase
from pyflowline.classes.vertex import pyvertex
from pyflowline.formats.read_flowline import read_flowline_geojson
from pyflowline.formats.export_flowline import export_flowline_to_geojson
from pyflowline.algorithms.split.find_flowline_confluence import find_flowline_confluence
from pyflowline.algorithms.merge.merge_flowline import merge_flowline

from pyhexwatershed.algorithms.auxiliary.export_json_to_geojson_polyline import export_json_to_geojson_polyline
from pyhexwatershed.algorithms.auxiliary.export_json_to_geojson_polygon import export_json_to_geojson_polygon
from pyhexwatershed.algorithms.auxiliary.merge_stream_edge_to_stream_segment import merge_stream_edge_to_stream_segment
from pyflowline.external.pyearth.gis.gdal.gdal_functions import gdal_read_geotiff_file, reproject_coordinates, reproject_coordinates_batch

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
            return obj.sWorkspace_output             
        return JSONEncoder.default(self, obj)

class hexwatershedcase(object):
   
    iFlag_profile = 0 
    iFlag_resample_method=2 
    iFlag_flowline=1
    iFlag_global = 0
    iFlag_antarctic=0
    iFlag_multiple_outlet = 0
    iFlag_elevation_profile = 0
    iFlag_stream_burning_topology=1
    iFlag_create_mesh= 1
    iFlag_simplification= 0
    iFlag_intersect= 0
    iFlag_merge_reach=1
    iMesh_type = 4   
    iFlag_save_mesh = 0 
    iFlag_use_mesh_dem=0
    iFlag_user_provided_binary= 0
    iFlag_slurm = 0
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
    sFilename_mesh=''
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    sFilename_basins=''     
    sFilename_hexwatershed_bin=''
    sWorkspace_model_region=''   

    sFilename_elevation=''
    sFilename_slope=''
    sFilename_drainage_area=''
    sFilename_flow_direction='' 
    sFilename_distance_to_outlet=   ''

    sFilename_variable_polyline=''
    sFilename_variable_polygon=''
  
    sRegion=''
    sModel=''
    iMesh_type ='mpas'
    sCase=''
    sDate=''    
    sFilename_spatial_reference=''
 
    sFilename_hexwatershed_json=''
    pPyFlowline = None #the pyflowline object
    
    sWorkspace_input=''
    sWorkspace_output_pyflowline=''
    sWorkspace_output_hexwatershed=''
    aBasin = list()
    
    
    iFlag_visual = importlib.util.find_spec("cartopy")
    if iFlag_visual is not None:
        from ._visual import plot
        from ._visual import _animate          
        from ._hpc import _create_hpc_job
        from ._hpc import _submit_hpc_job
    else:
        pass

    def __init__(self, aConfig_in):
        print('HexWatershed compset is being initialized')
        self.sFilename_model_configuration    = aConfig_in[ 'sFilename_model_configuration']

        if 'sWorkspace_data' in aConfig_in:
            self.sWorkspace_data = aConfig_in[ 'sWorkspace_data']
        
        if 'sWorkspace_input' in aConfig_in:
            self.sWorkspace_input = aConfig_in[ 'sWorkspace_input']
        
        if 'sWorkspace_output' in aConfig_in:
            self.sWorkspace_output    = aConfig_in[ 'sWorkspace_output']

        if 'sWorkspace_project' in aConfig_in:
            self.sWorkspace_project= aConfig_in[ 'sWorkspace_project']

        if 'sRegion' in aConfig_in:
            self.sRegion               = aConfig_in[ 'sRegion']

        if 'sModel' in aConfig_in:
            self.sModel                = aConfig_in[ 'sModel']
     
        if 'iFlag_resample_method' in aConfig_in:
            self.iFlag_resample_method       = int(aConfig_in[ 'iFlag_resample_method'])

        if 'iFlag_flowline' in aConfig_in:
            self.iFlag_flowline             = int(aConfig_in[ 'iFlag_flowline'])
        else: 
            self.iFlag_flowline =1 

        if 'iFlag_create_mesh' in aConfig_in:
            self.iFlag_create_mesh             = int(aConfig_in[ 'iFlag_create_mesh'])
        else: 
            self.iFlag_create_mesh =1 

        if 'iFlag_simplification' in aConfig_in:
            self.iFlag_simplification             = int(aConfig_in[ 'iFlag_simplification'])
        else: 
            self.iFlag_simplification = 1 
        if self.iFlag_simplification ==1:
            self.iFlag_flowline = 1

        if 'iFlag_intersect' in aConfig_in:
            self.iFlag_intersect             = int(aConfig_in[ 'iFlag_intersect'])
        else: 
            self.iFlag_intersect = 1 

        if 'iFlag_global' in aConfig_in:
            self.iFlag_global             = int(aConfig_in[ 'iFlag_global'])
        
        if 'iFlag_antarctic' in aConfig_in:
            self.iFlag_antarctic             = int(aConfig_in[ 'iFlag_antarctic'])   

        if 'iFlag_multiple_outlet' in aConfig_in:
            self.iFlag_multiple_outlet             = int(aConfig_in[ 'iFlag_multiple_outlet'])    

        if 'iFlag_use_mesh_dem' in aConfig_in:
            self.iFlag_use_mesh_dem             = int(aConfig_in[ 'iFlag_use_mesh_dem'])

        if 'iFlag_use_shapefile_extent' in aConfig_in:
            self.iFlag_use_shapefile_extent  = int(aConfig_in[ 'iFlag_use_shapefile_extent'])

            

        if 'iFlag_stream_burning_topology' in aConfig_in:
            self.iFlag_stream_burning_topology       = int(aConfig_in[ 'iFlag_stream_burning_topology'])

        if self.iFlag_flowline == 0:
            self.iFlag_stream_burning_topology = 0

        if 'iFlag_save_mesh' in aConfig_in:
            self.iFlag_save_mesh             = int(aConfig_in[ 'iFlag_save_mesh'])
        
        if 'iFlag_save_elevation' in aConfig_in:
            self.iFlag_save_elevation  = int(aConfig_in[ 'iFlag_save_elevation'])

        if 'iFlag_elevation_profile' in aConfig_in:
            self.iFlag_elevation_profile  = int(aConfig_in[ 'iFlag_elevation_profile'])
        
        if 'iFlag_user_provided_binary' in aConfig_in:
            self.iFlag_user_provided_binary  = int(aConfig_in[ 'iFlag_user_provided_binary'])
        else:
            self.iFlag_user_provided_binary = 0

        if 'nOutlet' in aConfig_in:
            self.nOutlet             = int(aConfig_in[ 'nOutlet'])
        else:
            self.nOutlet  = 1

        if 'dMissing_value_dem' in aConfig_in:
            self.dMissing_value_dem             = float(aConfig_in[ 'dMissing_value_dem'])

        if 'dBreach_threshold' in aConfig_in:
            self.dBreach_threshold             = float(aConfig_in[ 'dBreach_threshold'])

        if 'dAccumulation_threshold' in aConfig_in:
            self.dAccumulation_threshold             = float(aConfig_in[ 'dAccumulation_threshold'])
        
        if 'sFilename_spatial_reference' in aConfig_in:
            self.sFilename_spatial_reference = aConfig_in['sFilename_spatial_reference']

        if 'sFilename_dem' in aConfig_in:
            self.sFilename_dem = aConfig_in['sFilename_dem']

        if 'sFilename_mesh_netcdf' in aConfig_in:
            self.sFilename_mesh_netcdf = aConfig_in['sFilename_mesh_netcdf']

        if self.iFlag_user_provided_binary == 1:
            print('The model will use the user provided binary file')
            if 'sFilename_hexwatershed_bin' in aConfig_in:
                self.sFilename_hexwatershed_bin = aConfig_in['sFilename_hexwatershed_bin']
                #check file exist
                if not os.path.exists(self.sFilename_hexwatershed_bin):
                    print('The user provided binary file does not exist. The model will use the default binary file')
                    self.iFlag_user_provided_binary = 0
                    pass
                else:
                    print(self.sFilename_hexwatershed_bin)

            else:
                print('The binray file is not provided. The model will use the default binary file')
                self.iFlag_user_provided_binary = 0
                pass
        else:
            print('The model will use the default binary file')
            pass
            

        if 'iCase_index' in aConfig_in:
            iCase_index = int(aConfig_in['iCase_index'])
        else:
            iCase_index = 1
              
        sDate   = aConfig_in[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default

        sCase_index = "{:03d}".format( iCase_index )
        self.iCase_index =   iCase_index
        sCase = self.sModel  + self.sDate + sCase_index
        self.sCase = sCase

        sPath = str(Path(self.sWorkspace_output)  /  sCase)
        self.sWorkspace_output = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        
        if 'sMesh_type' in aConfig_in:
            self.sMesh_type =  aConfig_in['sMesh_type']
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
                            
        if 'dResolution_degree' in aConfig_in:
            self.dResolution_degree = float(aConfig_in['dResolution_degree']) 

        if 'dResolution_meter' in aConfig_in:
            self.dResolution_meter = float(aConfig_in['dResolution_meter']) 
        else:
            print('Please specify resolution.')

        if 'dLongitude_left' in aConfig_in:
            self.dLongitude_left = float(aConfig_in['dLongitude_left']) 

        if 'dLongitude_right' in aConfig_in:
            self.dLongitude_right = float(aConfig_in['dLongitude_right']) 

        if 'dLatitude_bot' in aConfig_in:
            self.dLatitude_bot = float(aConfig_in['dLatitude_bot']) 

        if 'dLatitude_top' in aConfig_in:
            self.dLatitude_top = float(aConfig_in['dLatitude_top']) 

        if 'sJob' in aConfig_in:
            self.sJob =  aConfig_in['sJob'] 
                
        if 'sFilename_basins' in aConfig_in:
            self.sFilename_basins = aConfig_in['sFilename_basins']
        else:
            self.sFilename_basins = ''              

        sPath = str(Path(self.sWorkspace_output)   / 'hexwatershed')
        self.sWorkspace_output_hexwatershed = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        sPath = str(Path(self.sWorkspace_output)   / 'pyflowline')
        self.sWorkspace_output_pyflowline = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)
        
        self.sFilename_mesh = os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + ".geojson" )
        self.sFilename_mesh_info  =  os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + "_mesh_info.json"  ) 
        self.sFilename_hexwatershed_json = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  "hexwatershed.json" )

        #individual output variables
        self.sFilename_elevation = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_elevation.geojson" )
        self.sFilename_slope = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_slope.geojson" )
        self.sFilename_drainage_area =  os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_drainage_area.geojson" )
        self.sFilename_flow_direction = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_flow_direction.geojson" )
        self.sFilename_distance_to_outlet = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_distance_to_outlet.geojson" )
        
        self.sFilename_variable_polyline = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_variable_polyline.geojson" )
        self.sFilename_variable_polygon = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_variable_polygon.geojson" )
        return    

    def tojson(self):
        aSkip = ['aBasin']     
        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
            pass

        sJson = json.dumps(obj,\
            sort_keys=True, \
            indent = 4, \
            ensure_ascii=True, \
            cls=CaseClassEncoder)

        return sJson

    def export_config_to_json(self, sFilename_out=None):  
        self.pPyFlowline.export_basin_config_to_json()
        self.sFilename_model_configuration = os.path.join(self.sWorkspace_output, 'configuration.json')
        self.sFilename_basins = self.pPyFlowline.sFilename_basins
        #save the configuration to a new file, which has the full path    
        if sFilename_out is not None:
            sFilename_configuration = sFilename_out
        else:
            sFilename_configuration = self.sFilename_model_configuration

        aSkip = [ 'aBasin', \
                'aFlowline_simplified','aFlowline_conceptual','aCellID_outlet',
                'aCell' ]

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
            pass
        with open(sFilename_configuration, 'w', encoding='utf-8') as f:
            json.dump(obj, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=CaseClassEncoder)     

        #make a copy  
        if sFilename_out is not None:
            copy2(sFilename_configuration, self.sFilename_model_configuration)      
        
        return
     
    def setup(self):
        #setup the pyflowline
        self.pPyFlowline.setup()
        #setup the hexwatershed
        system = platform.system()
        iFlag_found_binary = 0
        

        #if user provided the binary, then use the user provided binary
        if self.iFlag_user_provided_binary == 1:
            sFilename_executable = 'hexwatershed' 
            #copy the binary 
            iFlag_found_binary = 1
            sFilename_new = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  sFilename_executable )
            copy2(self.sFilename_hexwatershed_bin, sFilename_new)
            os.chmod(sFilename_new, stat.S_IRWXU )
            pass
        else:          
            # Get the distribution object for the package
            distribution = pkg_resources.get_distribution('hexwatershed')
            # Get the installation path for the package
            sPath_installation = distribution.location

            if system == 'Windows':
                sFilename_executable = 'hexwatershed.exe'
            else:
                sFilename_executable = 'hexwatershed'     
            
            #search for system wide binary in the system path
            for folder in os.environ['PATH'].split(os.pathsep):
                sFilename_hexwatershed_bin = os.path.join(folder, sFilename_executable)
                if os.path.isfile(sFilename_hexwatershed_bin):
                    print('Found binary at:', sFilename_hexwatershed_bin)
                    iFlag_found_binary = 1
                    break
            else:
                print('Binary not found in system path.')
            if iFlag_found_binary ==1:
                pass
            else:                
                sFilename_hexwatershed_bin = os.path.join(str(Path(sPath_installation + '/pyhexwatershed/_bin/') ) ,  sFilename_executable )
                if os.path.isfile(sFilename_hexwatershed_bin):
                    iFlag_found_binary=1
                    #copy the binary file
                    sFilename_new = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  sFilename_executable )
                    copy2(sFilename_hexwatershed_bin, sFilename_new)
                    os.chmod(sFilename_new, stat.S_IRWXU )
                else:
                    iFlag_found_binary = 0       
            

        return
    
    def run_pyflowline(self):
        """
        Run the pyflowline submodel

        Returns:
            _type_: _description_
        """

        aCell_out = self.pPyFlowline.run()

        return aCell_out
    
    def run_hexwatershed(self):
        """
        Run the hexwatershed model
        """
        system = platform.system()
        if platform.system() == 'Windows':
            print('Running on a Windows system')
            #run the model using bash
            self.generate_bash_script()
            os.chdir(self.sWorkspace_output_hexwatershed)            
            sCommand = "./run_hexwatershed.bat"
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()           
        elif system == 'Linux':
            print('Running on a Unix-based system')
            #run the model using bash
            self.generate_bash_script()
            os.chdir(self.sWorkspace_output_hexwatershed)            
            sCommand = "./run_hexwatershed.sh"
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()
        elif system == 'Darwin':     
            print('Running on a Unix-based system')
            #run the model using bash
            self.generate_bash_script()
            os.chdir(self.sWorkspace_output_hexwatershed)            
            sCommand = "./run_hexwatershed.sh"
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()        
        else:
            print('Unknown operating system')
            

        return
    
    def assign_elevation_to_cells(self):
        iMesh_type=self.iMesh_type
        iFlag_resample_method= self.iFlag_resample_method
        sFilename_dem_in = self.sFilename_dem
        aCell_in=self.pPyFlowline.aCell
        aCell_mid=list()
        ncell = len(aCell_in)        
        pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
        pDriver_json = ogr.GetDriverByName('GeoJSON')
        pDriver_memory = gdal.GetDriverByName('MEM')
        sFilename_shapefile_cut = "/vsimem/tmp_polygon.shp"
        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
        pDataset_elevation = gdal.Open(sFilename_dem_in, gdal.GA_ReadOnly)
        aDem_in, dPixelWidth, dOriginX, dOriginY, \
            nrow, ncolumn,dMissing_value, pSpatialRef_target, pProjection, pGeotransform = gdal_read_geotiff_file(sFilename_dem_in)

        #transform = osr.CoordinateTransformation(pSrs, pSpatialRef_target) 
        #get raster extent 
        dX_left=dOriginX
        dX_right = dOriginX + ncolumn * dPixelWidth
        dY_top = dOriginY
        dY_bot = dOriginY - nrow * dPixelWidth
        if iFlag_resample_method == 2: #zonal mean
            for i in range( ncell):
                pCell=  aCell_in[i]
                lCellID = pCell.lCellID
                dLongitude_center_degree = pCell.dLongitude_center_degree
                dLatitude_center_degree = pCell.dLatitude_center_degree
                nVertex = pCell.nVertex

                ring = ogr.Geometry(ogr.wkbLinearRing)
                aX= list()
                aY=list()
                for j in range(nVertex):
                    aX.append( pCell.aVertex[j].dLongitude_degree )
                    aY.append( pCell.aVertex[j].dLatitude_degree )                               
                    pass
                aX.append( pCell.aVertex[0].dLongitude_degree )
                aY.append( pCell.aVertex[0].dLatitude_degree )
                aX_out,aY_out = reproject_coordinates_batch(aX,aY,pSrs,pSpatialRef_target)   
                for j in range(nVertex + 1):
                    x1 = aX_out[j]
                    y1 = aY_out[j]                    
                    ring.AddPoint(x1, y1)                
                    pass                      
       
                pPolygon = ogr.Geometry(ogr.wkbPolygon)
                pPolygon.AddGeometry(ring)
                #pPolygon.AssignSpatialReference(pSpatialRef_target)
                if os.path.exists(sFilename_shapefile_cut):   
                    os.remove(sFilename_shapefile_cut)

                pDataset3 = pDriver_shapefile.CreateDataSource(sFilename_shapefile_cut)
                pLayerOut3 = pDataset3.CreateLayer('cell', pSpatialRef_target, ogr.wkbPolygon)    
                pLayerDefn3 = pLayerOut3.GetLayerDefn()
                pFeatureOut3 = ogr.Feature(pLayerDefn3)
                pFeatureOut3.SetGeometry(pPolygon)  
                pLayerOut3.CreateFeature(pFeatureOut3)    
                pDataset3.FlushCache()

                minX, maxX, minY, maxY = pPolygon.GetEnvelope()
                iNewWidth = int( (maxX - minX) / abs(dPixelWidth)  )
                iNewHeigh = int( (maxY - minY) / abs(dPixelWidth) )
                newGeoTransform = (minX, dPixelWidth, 0,    maxY, 0, -dPixelWidth)  

                if minX > dX_right or maxX < dX_left \
                    or minY > dY_top or maxY < dY_bot:        
                    #this polygon is out of bound            
                    continue
                else:         
                    pDataset_clip = pDriver_memory.Create('', iNewWidth, iNewHeigh, 1, gdalconst.GDT_Float32)
                    pDataset_clip.SetGeoTransform( newGeoTransform )
                    pDataset_clip.SetProjection( pProjection)   
                    pWrapOption = gdal.WarpOptions( cropToCutline=True,cutlineDSName = sFilename_shapefile_cut , \
                            width=iNewWidth,   \
                                height=iNewHeigh,      \
                                    dstSRS=pProjection , format = 'MEM' )
                    pDataset_clip = gdal.Warp('',pDataset_elevation, options=pWrapOption)
                    pBand = pDataset_clip.GetRasterBand( 1 )
                    dMissing_value = pBand.GetNoDataValue()
                    aData_out = pBand.ReadAsArray(0,0,iNewWidth, iNewHeigh)

                    aElevation = aData_out[np.where(aData_out !=dMissing_value)]                

                    if(len(aElevation) >0 and np.mean(aElevation)!=-9999):                        
                        dElevation =  float(np.mean(aElevation) )                          
                        pCell.dElevation_mean =    dElevation  
                        pCell.dz = dElevation  
                        aCell_mid.append(pCell)
                    else:                    
                        pCell.dElevation_mean=-9999.0
                        pass
        
        else:
            #the nearest resample method
            for i in range( ncell):
                pCell=  aCell_in[i]
                lCellID = pCell.lCellID
                dLongitude_center_degree = pCell.dLongitude_center_degree
                dLatitude_center_degree = pCell.dLatitude_center_degree
                x1 = dLongitude_center_degree
                y1 = dLatitude_center_degree
                dX_out,dY_out = reproject_coordinates(x1,y1,pSrs,pSpatialRef_target)   
                dDummy1 = (dX_out - dX_left) / dPixelWidth
                lColumn_index = int(dDummy1)
                dDummy2 = (dY_top - dY_out) / dPixelWidth
                lRow_index = int(dDummy2)

                if lColumn_index >= ncolumn or lColumn_index < 0 \
                    or lRow_index >= nrow or lRow_index < 0:        
                    #this pixel is out of bound            
                    continue
                else:         
                    dElevation = aDem_in[lRow_index, lColumn_index]     
                    if( dElevation!=-9999):     
                        pCell.dElevation_mean =    dElevation  
                        pCell.dz = dElevation  
                        aCell_mid.append(pCell)
                    else:                    
                        pCell.dElevation_mean=-9999.0
                        pass
            pass

        #update neighbor because not all cells have elevation now
        ncell = len(aCell_mid)
        aCellID  = list()
        for i in range(ncell):
            pCell = aCell_mid[i]
            lCellID = pCell.lCellID
            aCellID.append(lCellID)

        aCell_out=list()
        for i in range(ncell):
            pCell = aCell_mid[i]
            aNeighbor = pCell.aNeighbor
            aNeighbor_distance = pCell.aNeighbor_distance
            nNeighbor = pCell.nNeighbor
            aNeighbor_new = list()
            aNeighbor_distance_new = list()
            nNeighbor_new = 0 
            for j in range(nNeighbor):
                lNeighbor = int(aNeighbor[j])
                if lNeighbor in aCellID:
                    nNeighbor_new = nNeighbor_new +1 
                    aNeighbor_new.append(lNeighbor)
                    aNeighbor_distance_new.append(aNeighbor_distance[j])

            pCell.nNeighbor= len(aNeighbor_new)
            pCell.aNeighbor = aNeighbor_new
            pCell.nNeighbor_land= len(aNeighbor_new)
            pCell.aNeighbor_land = aNeighbor_new
            pCell.aNeighbor_distance = aNeighbor_distance_new
            aCell_out.append(pCell)

        #update the cell information
        self.pPyFlowline.aCell= aCell_out
        return aCell_out
        
    def update_outlet(self, aCell_elevation, aCell_origin):
        #after the elevation assignment, it is possible that the outlet has no elevation
        
        aCell_remove = list()
        def search_upstream(lCellID_in):
            for pCell_temp in aCell_origin:
                if pCell_temp.lCellID_downstream_burned == lCellID_in:
                    aCell_remove.append(lCellID_in)
                    return pCell_temp.lCellID
            
        for iBasin in range(len(self.pPyFlowline.aBasin)):
            pBasin = self.pPyFlowline.aBasin[iBasin]
            lCellID_outlet = pBasin.lCellID_outlet
            iFlag_error= 0
            for pCell_temp in aCell_origin:
                if pCell_temp.lCellID == lCellID_outlet:
                    if pCell_temp.dElevation_mean == -9999:
                        iFlag_error = 1
                        break
            if iFlag_error ==1:              
                iFlag_found = 0
                lCellID_current = lCellID_outlet
                while(iFlag_found ==0 ):

                    lOutletID_next  = search_upstream(lCellID_current)
                    for pCell_temp in self.pPyFlowline.aCell:
                        if pCell_temp.lCellID == lOutletID_next:
                            if pCell_temp.dElevation_mean !=-9999:
                                iFlag_found = 1
                                pCell_temp.lCellID_downstream_burned = -1
                                break
                            
                    lCellID_current = lOutletID_next

                self.pPyFlowline.aBasin[iBasin].lCellID_outlet = lOutletID_next
            else:
                #there is no issue with it
                pass

            pass

        for pCell in aCell_elevation:
            lCellID = pCell.lCellID
            if lCellID in aCell_remove:
                aCell_elevation.remove(pCell)

        self.pPyFlowline.aCell = aCell_elevation

        return

    def generate_bash_script(self):       
        sName  = 'configuration.json'
        sFilename_configuration  =  os.path.join( self.sWorkspace_output,  sName )
        os.chdir(self.sWorkspace_output_hexwatershed)    
        #detemine the system platform
        # Determine the appropriate executable name for the platform
        system = platform.system()
        if platform.system() == 'Windows':
            sFilename_executable = 'hexwatershed.exe'
            iFlag_unix = 0
        else:
            sFilename_executable = './hexwatershed'
            

        if system == 'Windows':
            # execute binary on Windows          
            iFlag_unix = 0
        elif system == 'Linux':
            # execute binary on Linux
            iFlag_unix = 1
        elif system == 'Darwin':
            # execute binary on macOS
            iFlag_unix = 1
        else:
            # unsupported operating system
            print('Unsupported operating system: ' + system)
            print('Please reach out to the developers for assistance.')

        #generate the bash/batch script    
        if iFlag_unix == 1 :
            sFilename_bash = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  "run_hexwatershed.sh" )
            ofs = open(sFilename_bash, 'w')
            sLine = '#!/bin/bash\n'
            ofs.write(sLine)   
            sLine = 'cd ' + self.sWorkspace_output_hexwatershed+ '\n'
            ofs.write(sLine)
            sLine = sFilename_executable + ' ' + sFilename_configuration + '\n'
            ofs.write(sLine)
            ofs.close()
            os.chmod(sFilename_bash, stat.S_IRWXU )      
        else:
            sFilename_bash = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  "run_hexwatershed.bat" )
            ofs = open(sFilename_bash, 'w')                               
            sLine = 'cd ' + self.sWorkspace_output_hexwatershed+ '\n'
            ofs.write(sLine)
            sLine = sFilename_executable + ' ' + sFilename_configuration + '\n'
            ofs.write(sLine)
            ofs.close()
            os.chmod(sFilename_bash, stat.S_IRWXU )     
        return
    
    def analyze(self):
        #a list of analysis was done within the C++ backend
        #additional analysis can be implemented here
        return

    def export(self):   
        """
        #https://hexwatershed.readthedocs.io/en/latest/application/application.html#simulation-results
        """        
        
        #polyline

        if self.iFlag_global==1: #we do not have the polyline information
            pass
        else:
            if self.iFlag_multiple_outlet == 1:
                pass
            else:

                self.pyhexwatershed_export_stream_segment()
                self.pyhexwatershed_export_flow_direction() 

                #polygon
                #self.pyhexwatershed_export_elevation()
                #self.pyhexwatershed_export_slope()
                #self.pyhexwatershed_export_drainage_area()                         
                self.pyhexwatershed_export_travel_distance()

                #we can also save a geojson that has all the information
                self.pyhexwatershed_export_all_polygon_variables()
                #self.pyhexwatershed_export_all_polyline_variables()
                pass

        return

    def pyhexwatershed_export_stream_segment(self):
        """
        https://hexwatershed.readthedocs.io/en/latest/application/application.html#simulation-results
        """       
               
        iFlag_flowline = self.iFlag_flowline
        nWatershed = self.nOutlet

        if self.iFlag_global==1: #we do not output global scale stream segment yet
            sFilename_json = self.sFilename_hexwatershed_json
            return

        else:
            if self.iFlag_multiple_outlet==1:                
                for iWatershed in range(1, nWatershed+1):                   
                    pBasin = self.aBasin[iWatershed-1]                    
                    sFilename_stream_edge  = pBasin.sFilename_stream_edge_json
                    sFilename_stream_edge_geojson = pBasin.sFilename_stream_edge
                    sFilename_stream_segment_geojson = pBasin.sFilename_stream_segment
                    point = dict()
                    point['dLongitude_degree'] = pBasin.dLongitude_outlet_degree
                    point['dLatitude_degree'] = pBasin.dLatitude_outlet_degree
                    pVertex_outlet=pyvertex(point)
                    export_json_to_geojson_polyline(sFilename_stream_edge, sFilename_stream_edge_geojson)
                    merge_stream_edge_to_stream_segment(sFilename_stream_edge_geojson, 
                                                        sFilename_stream_segment_geojson, 
                                                        pVertex_outlet)
                return
            else:
                #use the only one basin               
                if iFlag_flowline == 1: #we usually has one outlet        
                    #for iWatershed in range(1, nWatershed+1):
                    iWatershed = 1
                    pBasin = self.aBasin[iWatershed-1]  
                    pBasin_pyflowline = self.pPyFlowline.aBasin[iWatershed-1]                  
                    sFilename_stream_edge  = pBasin.sFilename_stream_edge_json
                    sFilename_stream_edge_geojson = pBasin.sFilename_stream_edge
                    sFilename_stream_segment_geojson = pBasin.sFilename_stream_segment

                    point = dict()
                    point['dLongitude_degree'] = pBasin_pyflowline.dLongitude_outlet_degree
                    point['dLatitude_degree'] = pBasin_pyflowline.dLatitude_outlet_degree
                    pVertex_outlet=pyvertex(point)
                    aVariable_json_in = ['iSegment']
                    aVariable_geojson_out = ['isegment']
                    aVariable_type_out= [1]
                    export_json_to_geojson_polyline(sFilename_stream_edge, 
                                                    sFilename_stream_edge_geojson, 
                                                    aVariable_json_in,
                                                    aVariable_geojson_out,
                                                 aVariable_type_out)
                    merge_stream_edge_to_stream_segment(sFilename_stream_edge_geojson, 
                                                        sFilename_stream_segment_geojson, 
                                                        pVertex_outlet)
 
           

        return

    def pyhexwatershed_export_flow_direction(self):
        """
        #https://hexwatershed.readthedocs.io/en/latest/application/application.html#simulation-results
        """

        if self.iFlag_global==1:
            sFilename_json = self.sFilename_hexwatershed_json
            sFilename_geojson = self.sFilename_flow_direction
            export_json_to_geojson_polyline(sFilename_json, sFilename_geojson)  

        else:
            if self.iFlag_multiple_outlet==1:
                sFilename_json = self.sFilename_hexwatershed_json
                sFilename_geojson = self.sFilename_flow_direction                  
                export_json_to_geojson_polyline(sFilename_json, sFilename_geojson)
            else:
                iWatershed = 1
                pBasin = self.aBasin[iWatershed-1]      
                #use the only one basin
                sFilename_json = pBasin.sFilename_watershed_json
                sFilename_geojson = pBasin.sFilename_flow_direction  
               
                aVariable_json = ['iSegment','DrainageArea']
                aVariable_geojson =    ['iSegment','drainage_area']
                aVariable_type_out = [1, 2]
                export_json_to_geojson_polyline(sFilename_json, sFilename_geojson,
                                                aVariable_json, aVariable_geojson, aVariable_type_out)
        
     
    def pyhexwatershed_export_elevation(self):
        """

        https://hexwatershed.readthedocs.io/en/latest/application/application.html#simulation-results
        """

        sFilename_json = self.sFilename_hexwatershed_json
        sFilename_geojson = self.sFilename_elevation
        aVariable_json  = ['Elevation']
        aVariable_geojson= ['elevation']
        export_json_to_geojson_polygon(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson)
    
    def pyhexwatershed_export_slope(self):

        sFilename_json = self.sFilename_hexwatershed_json
        sFilename_geojson = self.sFilename_slope
        aVariable_json  = ['dSlope_between']
        aVariable_geojson= ['slope']
        export_json_to_geojson_polygon(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson)
    
    def pyhexwatershed_export_drainage_area(self):
        sFilename_json = self.sFilename_hexwatershed_json
        sFilename_geojson = self.sFilename_drainage_area
        aVariable_json  = ['slp']
        aVariable_geojson= ['slp']
        export_json_to_geojson_polygon(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson)
  
    #starting from here, we will save watershed-level files    
       
    def pyhexwatershed_export_travel_distance(self):
     
        nWatershed = self.nOutlet
        if self.iFlag_flowline==1:    
            for iWatershed in range(1, nWatershed+1):
                pBasin = self.aBasin[iWatershed-1]     
                sFilename_json = pBasin.sFilename_watershed_json
                sFilename_geojson = pBasin.sFilename_distance_to_outlet
                aVariable_json  = ['dDistance_to_watershed_outlet']
                aVariable_geojson= ['travel_distance']
                aVariable_type= [2]
                export_json_to_geojson_polygon(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson,
                                        aVariable_type )
                pass  

    def pyhexwatershed_export_all_polyline_variables(self):
        sFilename_json = self.sFilename_hexwatershed_json
        sFilename_geojson = self.sFilename_variable_polyline
        #
        aVariable_json  = ['slp']
        aVariable_geojson= ['slp']
        export_json_to_geojson_polyline(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson)
        return

    def pyhexwatershed_export_all_polygon_variables(self):
        """
        Export all the polygon based variable into a single geojson file
        """
        if self.iFlag_global==1:
            sFilename_json = self.sFilename_hexwatershed_json
            sFilename_geojson = self.sFilename_variable_polygon
             

        else:
            if self.iFlag_multiple_outlet==1:
                sFilename_json = self.sFilename_hexwatershed_json
                sFilename_geojson = self.sFilename_variable_polygon                
            else:
                iWatershed = 1
                pBasin = self.aBasin[iWatershed-1]      
                #use the only one basin
                sFilename_json = pBasin.sFilename_watershed_json
                sFilename_geojson = pBasin.sFilename_variable_polygon  

        if self.iMesh_type == 4:
            aVariable_json  = ['iSubbasin','Elevation','dSlope_between', 'DrainageArea','dDistance_to_watershed_outlet']
            aVariable_geojson = ['isubbasin','elevation', 'slope', 'drainage_area','travel_distance']
        else:
            aVariable_json  = ['iSubbasin','Elevation','dSlope_profile','DrainageArea','dDistance_to_watershed_outlet']
            aVariable_geojson = ['isubbasin','elevation', 'slope', 'drainage_area','travel_distance']

        aVariable_type= [1, 2,2,2,2]
        export_json_to_geojson_polygon(sFilename_json,
                                        sFilename_geojson, 
                                        aVariable_json,
                                        aVariable_geojson,
                                        aVariable_type)
        return