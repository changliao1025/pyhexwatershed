import os
import stat
import platform
import pkg_resources
import datetime
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
from pyflowline.algorithms.split.find_flowline_confluence import find_flowline_confluence
from pyflowline.algorithms.merge.merge_flowline import merge_flowline
from pyflowline.formats.export_flowline import export_flowline_to_geojson

from pyflowline.algorithms.simplification.remove_duplicate_edge import remove_duplicate_edge
from pyhexwatershed.algorithm.auxiliary.gdal_function import gdal_read_geotiff_file, reproject_coordinates, reproject_coordinates_batch

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
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    sFilename_basins=''     
    sWorkspace_model_region=''    
  
    sRegion=''
    sModel=''
    iMesh_type ='mpas'
    sCase=''
    sDate=''    
    sFilename_spatial_reference=''
 
    sFilename_hexwatershed_json=''
    pPyFlowline = None
    sWorkspace_input=''
    sWorkspace_output_pyflowline=''
    sWorkspace_output_hexwatershed=''
    aBasin = list()
    
    from ._visual import _plot
    from ._visual import _animate
    from ._visual import _plot_flow_direction
    from ._visual import _plot_mesh_with_variable
    from ._visual import _plot_mesh_with_flow_direction
    from ._visual import _plot_mesh_with_flow_direction_and_river_network
    from ._hpc import _create_hpc_job
    from ._hpc import _submit_hpc_job

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

        if 'iFlag_multiple_outlet' in aConfig_in:
            self.iFlag_multiple_outlet             = int(aConfig_in[ 'iFlag_multiple_outlet'])    

        if 'iFlag_use_mesh_dem' in aConfig_in:
            self.iFlag_use_mesh_dem             = int(aConfig_in[ 'iFlag_use_mesh_dem'])

        if 'iFlag_use_shapefile_extent' in aConfig_in:
            self.iFlag_use_shapefile_extent             = int(aConfig_in[ 'iFlag_use_shapefile_extent'])

            

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

        self.sFilename_elevation = os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + "_elevation.geojson" )
        self.sFilename_mesh = os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + ".geojson" )
        self.sFilename_mesh_info  =  os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + "_mesh_info.json"  ) 
        self.sFilename_hexwatershed_json = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  "hexwatershed.json" )
        
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
        # Get the distribution object for the package
        distribution = pkg_resources.get_distribution('hexwatershed')
        # Get the installation path for the package
        sPath_installation = distribution.location
        if platform.system() == 'Windows':
            sFilename_executable = 'hexwatershed.exe'
            sFilename_hexwatershed_bin = os.path.join(str(Path(sPath_installation + '/pyhexwatershed/_bin/') ) ,  sFilename_executable )
            #copy the binary file
            sFilename_new = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  sFilename_executable )
            copy2(sFilename_hexwatershed_bin, sFilename_new)
            os.chmod(sFilename_new, stat.S_IRWXU )
            
        else:
            sFilename_executable = 'hexwatershed'            
            sFilename_hexwatershed_bin = os.path.join(str(Path(sPath_installation + '/pyhexwatershed/_bin/') ) ,  sFilename_executable )
            #copy the binary file
            sFilename_new = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sFilename_executable )
            copy2(sFilename_hexwatershed_bin, sFilename_new)
            os.chmod(sFilename_new, stat.S_IRWXU )

        return
    
    def run_pyflowline(self):

        aCell_out = self.pPyFlowline.run()

        return aCell_out
    
    def run_hexwatershed(self):
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
        self.pyhexwatershed_save_elevation()
        self.pyhexwatershed_save_slope()
        self.pyhexwatershed_save_drainage_area()        
        self.pyhexwatershed_save_flow_direction()    
        self.pyhexwatershed_save_stream_segment()
        self.pyhexwatershed_save_travel_distance()

        return

    def pyhexwatershed_save_flow_direction(self):
        sFilename_json = os.path.join(self.sWorkspace_output_hexwatershed ,   'hexwatershed.json')
        sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed ,   'flow_direction.geojson')
        if os.path.exists(sFilename_geojson):
            os.remove(sFilename_geojson)
        pDriver_geojson = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson)    

        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)  #WGS84 lat/lon

        pLayer = pDataset.CreateLayer('flowdir', pSrs, ogr.wkbLineString)
        # Add one attribute
        pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
        pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
        pFac_field.SetWidth(20)
        pFac_field.SetPrecision(2)
        pLayer.CreateField(pFac_field) #long type for high resolution

        pLayerDefn = pLayer.GetLayerDefn()
        pFeature = ogr.Feature(pLayerDefn)

        with open(sFilename_json) as json_file:
            data = json.load(json_file)  
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]
                lCellID = int(pcell['lCellID'])
                lCellID_downslope = int(pcell['lCellID_downslope'])
                x_start=float(pcell['dLongitude_center_degree'])
                y_start=float(pcell['dLatitude_center_degree'])
                dfac = float(pcell['DrainageArea'])
                for j in range(ncell):
                    pcell2 = data[j]
                    lCellID2 = int(pcell2['lCellID'])
                    if lCellID2 == lCellID_downslope:
                        x_end=float(pcell2['dLongitude_center_degree'])
                        y_end=float(pcell2['dLatitude_center_degree'])

                        pLine = ogr.Geometry(ogr.wkbLineString)
                        pLine.AddPoint(x_start, y_start)
                        pLine.AddPoint(x_end, y_end)
                        pFeature.SetGeometry(pLine)
                        pFeature.SetField("id", lID)
                        pFeature.SetField("fac", dfac)
                        pLayer.CreateFeature(pFeature)
                        lID = lID +1
                        break

            pDataset = pLayer = pFeature  = None      
        pass
     
    def pyhexwatershed_save_slope(self):

        sFilename_json = os.path.join(self.sWorkspace_output_hexwatershed ,   'hexwatershed.json')

        sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed ,   'slope.geojson')
        if os.path.exists(sFilename_geojson):
            os.remove(sFilename_geojson)

        pDriver_geojson = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson)
        
    
        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

        pLayer = pDataset.CreateLayer('slp', pSrs, geom_type=ogr.wkbPolygon)
        # Add one attribute
        pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution       
        pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
        pFac_field.SetWidth(20)
        pFac_field.SetPrecision(2)
        pLayer.CreateField(pFac_field) #long type for high resolution

        pSlp_field = ogr.FieldDefn('slpb', ogr.OFTReal)
        pSlp_field.SetWidth(20)
        pSlp_field.SetPrecision(8)
        pLayer.CreateField(pSlp_field) #long type for high resolution

        pSlp_field = ogr.FieldDefn('slpp', ogr.OFTReal)
        pSlp_field.SetWidth(20)
        pSlp_field.SetPrecision(8)
        pLayer.CreateField(pSlp_field) #long type for high resolution

        pLayerDefn = pLayer.GetLayerDefn()
        pFeature = ogr.Feature(pLayerDefn)

        with open(sFilename_json) as json_file:
            data = json.load(json_file)  
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]
                lCellID = int(pcell['lCellID'])
                lCellID_downslope = int(pcell['lCellID_downslope'])
                x_start=float(pcell['dLongitude_center_degree'])
                y_start=float(pcell['dLatitude_center_degree'])
                dfac = float(pcell['DrainageArea'])
                dslpb = float(pcell['dSlope_between'])
                dslpp = float(pcell['dSlope_profile'])
                vVertex = pcell['vVertex']
                nvertex = len(vVertex)
                pPolygon = ogr.Geometry(ogr.wkbPolygon)
                ring = ogr.Geometry(ogr.wkbLinearRing)

                for j in range(nvertex):
                    x = vVertex[j]['dLongitude_degree']
                    y = vVertex[j]['dLatitude_degree']
                    ring.AddPoint(x, y)

                x = vVertex[0]['dLongitude_degree']
                y = vVertex[0]['dLatitude_degree']
                ring.AddPoint(x, y)
                pPolygon.AddGeometry(ring)
                pFeature.SetGeometry(pPolygon)
                pFeature.SetField("id", lCellID)                
                pFeature.SetField("fac", dfac)
                pFeature.SetField("slpb", dslpb)
                pFeature.SetField("slpp", dslpp)
                pLayer.CreateFeature(pFeature)

            pDataset = pLayer = pFeature  = None      
        pass        
    
    def pyhexwatershed_save_elevation(self):
        sFilename_json = os.path.join(self.sWorkspace_output_hexwatershed ,   'hexwatershed.json')

        sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed ,   'elevation.geojson')
        if os.path.exists(sFilename_geojson):
            os.remove(sFilename_geojson)

        pDriver_geojson = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson)           
        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
        pLayer = pDataset.CreateLayer('ele', pSrs, geom_type=ogr.wkbPolygon)
        # Add one attribute
        pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution       
        pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
        pFac_field.SetWidth(20)
        pFac_field.SetPrecision(2)
        pLayer.CreateField(pFac_field) #long type for high resolution

        pSlp_field = ogr.FieldDefn('elev', ogr.OFTReal)
        pSlp_field.SetWidth(20)
        pSlp_field.SetPrecision(8)
        pLayer.CreateField(pSlp_field) #long type for high resolution

        pSlp_field = ogr.FieldDefn('elep', ogr.OFTReal)
        pSlp_field.SetWidth(20)
        pSlp_field.SetPrecision(8)
        pLayer.CreateField(pSlp_field) #long type for high resolution

        pLayerDefn = pLayer.GetLayerDefn()
        pFeature = ogr.Feature(pLayerDefn)

        with open(sFilename_json) as json_file:
            data = json.load(json_file)  
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]
                lCellID = int(pcell['lCellID'])
                lCellID_downslope = int(pcell['lCellID_downslope'])
                x_start=float(pcell['dLongitude_center_degree'])
                y_start=float(pcell['dLatitude_center_degree'])
                dfac = float(pcell['DrainageArea'])
                dElev = float(pcell['Elevation'])
                dElep = float(pcell['Elevation_profile'])
                vVertex = pcell['vVertex']
                nvertex = len(vVertex)
                pPolygon = ogr.Geometry(ogr.wkbPolygon)
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for j in range(nvertex):
                    x = vVertex[j]['dLongitude_degree']
                    y = vVertex[j]['dLatitude_degree']
                    ring.AddPoint(x, y)

                x = vVertex[0]['dLongitude_degree']
                y = vVertex[0]['dLatitude_degree']
                ring.AddPoint(x, y)
                pPolygon.AddGeometry(ring)
                pFeature.SetGeometry(pPolygon)
                pFeature.SetField("id", lCellID)                
                pFeature.SetField("fac", dfac)
                pFeature.SetField("elev", dElev)
                pFeature.SetField("elep", dElep)
                pLayer.CreateFeature(pFeature)
            pDataset = pLayer = pFeature  = None      
        pass   

    def pyhexwatershed_save_drainage_area(self):
        sFilename_json = os.path.join(self.sWorkspace_output_hexwatershed ,   'hexwatershed.json')

        sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed ,   'drainage_area.geojson')
        if os.path.exists(sFilename_geojson):
            os.remove(sFilename_geojson)

        pDriver_geojson = ogr.GetDriverByName('GeoJSON')
        pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson)           
        pSrs = osr.SpatialReference()  
        pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
        pLayer = pDataset.CreateLayer('drai', pSrs, geom_type=ogr.wkbPolygon)
        # Add one attribute
        pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution       
        pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
        pFac_field.SetWidth(20)
        pFac_field.SetPrecision(2)
        pLayer.CreateField(pFac_field) #long type for high resolution
        

        pLayerDefn = pLayer.GetLayerDefn()
        pFeature = ogr.Feature(pLayerDefn)

        with open(sFilename_json) as json_file:
            data = json.load(json_file)  
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]
                lCellID = int(pcell['lCellID'])
                lCellID_downslope = int(pcell['lCellID_downslope'])
                x_start=float(pcell['dLongitude_center_degree'])
                y_start=float(pcell['dLatitude_center_degree'])
                dfac = float(pcell['DrainageArea'])               
                vVertex = pcell['vVertex']
                nvertex = len(vVertex)
                pPolygon = ogr.Geometry(ogr.wkbPolygon)
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for j in range(nvertex):
                    x = vVertex[j]['dLongitude_degree']
                    y = vVertex[j]['dLatitude_degree']
                    ring.AddPoint(x, y)

                x = vVertex[0]['dLongitude_degree']
                y = vVertex[0]['dLatitude_degree']
                ring.AddPoint(x, y)
                pPolygon.AddGeometry(ring)
                pFeature.SetGeometry(pPolygon)
                pFeature.SetField("id", lCellID)                
                pFeature.SetField("fac", dfac)                
                
                pLayer.CreateFeature(pFeature)
            pDataset = pLayer = pFeature  = None      
        pass  

    #starting from here, we will save watershed-level files    
    
    def pyhexwatershed_save_stream_segment(self):
        nWatershed = self.nOutlet
        
        for iWatershed in range(1, nWatershed+1):
            pBasin=   self.pPyFlowline.aBasin[iWatershed-1]
            sWatershed = "{:08d}".format(iWatershed) 

            sWorkspace_watershed =  os.path.join( self.sWorkspace_output_hexwatershed,  sWatershed )

            sFilename_watershed_stream_edge  = os.path.join( sWorkspace_watershed,  'stream_edge.json' )
            sFilename_stream_edge_geojson = os.path.join(sWorkspace_watershed ,   'stream_edge.geojson')
            if os.path.exists(sFilename_stream_edge_geojson):
                os.remove(sFilename_stream_edge_geojson)
            pDriver_geojson = ogr.GetDriverByName('GeoJSON')
            pDataset = pDriver_geojson.CreateDataSource(sFilename_stream_edge_geojson)    

            pSrs = osr.SpatialReference()  
            pSrs.ImportFromEPSG(4326)  #WGS84 lat/lon

            pLayer = pDataset.CreateLayer('flowdir', pSrs, ogr.wkbLineString)
            # Add one attribute
            pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
            pLayer.CreateField(ogr.FieldDefn('iseg', ogr.OFTInteger)) #long type for high resolution
            pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
            pFac_field.SetWidth(20)
            pFac_field.SetPrecision(2)
            pLayer.CreateField(pFac_field) #long type for high resolution

            pLayerDefn = pLayer.GetLayerDefn()
            pFeature = ogr.Feature(pLayerDefn)
            
            with open(sFilename_watershed_stream_edge) as json_file:
                data = json.load(json_file)  
                ncell = len(data)
                lID =0 
                for i in range(ncell):
                    pcell = data[i]
                    lCellID = int(pcell['lCellID'])
                    lCellID_downslope = int(pcell['lCellID_downslope'])
                    x_start=float(pcell['dLongitude_center_degree'])
                    y_start=float(pcell['dLatitude_center_degree'])
                    iSegment = int(pcell['iSegment'])
                    #iStream_order = int(pcell['lCellID_downslope'])
                    dfac = float(pcell['DrainageArea'])
                    for j in range(ncell):
                        pcell2 = data[j]
                        lCellID2 = int(pcell2['lCellID'])
                        if lCellID2 == lCellID_downslope:
                            x_end=float(pcell2['dLongitude_center_degree'])
                            y_end=float(pcell2['dLatitude_center_degree'])

                            pLine = ogr.Geometry(ogr.wkbLineString)
                            pLine.AddPoint(x_start, y_start)
                            pLine.AddPoint(x_end, y_end)
                            pFeature.SetGeometry(pLine)
                            pFeature.SetField("id", lID)
                            pFeature.SetField("fac", dfac)
                            pFeature.SetField("iseg", iSegment)
                            pLayer.CreateFeature(pFeature)
                            lID = lID +1
                            break           
        
            #delete and write to dick                    
            pFac_field =None
            pLine=None
            pLayer = None 
            pFeature = None 
            pDataset  = None 
        
        #now convert edge to segment
        for iWatershed in range(1, nWatershed+1):
            pBasin=   self.pPyFlowline.aBasin[iWatershed-1]
            sWatershed = "{:08d}".format(iWatershed) 
            sWorkspace_watershed =  os.path.join( self.sWorkspace_output_hexwatershed,  sWatershed )       
            sFilename_stream_edge_geojson = os.path.join(sWorkspace_watershed ,   'stream_edge.geojson')        
            aFlowline_edge_basin_conceptual, pSpatialRef_geojson = read_flowline_geojson(sFilename_stream_edge_geojson)

            #connect using 
            point = dict()
            point['dLongitude_degree'] = pBasin.dLongitude_outlet_degree
            point['dLatitude_degree'] = pBasin.dLatitude_outlet_degree
            pVertex_outlet=pyvertex(point)


            #remember there that it is possible that there is only one segment, no confluence
            aVertex, lIndex_outlet, aIndex_headwater,aIndex_middle, aIndex_confluence, aConnectivity, pVertex_outlet\
            = find_flowline_confluence(aFlowline_edge_basin_conceptual,  pVertex_outlet)
            #segment based
            aFlowline_basin_conceptual = merge_flowline( aFlowline_edge_basin_conceptual,\
                aVertex, pVertex_outlet, \
                aIndex_headwater,aIndex_middle, aIndex_confluence  )
            sFilename_stream_segment_geojson = os.path.join(sWorkspace_watershed , 'stream_segment.geojson')
            if os.path.exists(sFilename_stream_segment_geojson):
                os.remove(sFilename_stream_segment_geojson)

            aStream_segment = list()
            for pFlowline in aFlowline_basin_conceptual:
                aStream_segment.append( pFlowline.iStream_segment  )
            export_flowline_to_geojson(aFlowline_basin_conceptual, sFilename_stream_segment_geojson,
            aAttribute_data=[aStream_segment], aAttribute_field=['iseg'], aAttribute_dtype=['int'])
           

        return
    
    def pyhexwatershed_save_travel_distance(self):
        
        nWatershed = self.nOutlet
        
        for iWatershed in range(1, nWatershed+1):
            pBasin=   self.pPyFlowline.aBasin[iWatershed-1]
            sWatershed = "{:08d}".format(iWatershed) 
            sWorkspace_watershed =  os.path.join( self.sWorkspace_output_hexwatershed,  sWatershed )
            sFilename_json = os.path.join(sWorkspace_watershed ,   'watershed.json')
            sFilename_geojson = os.path.join(sWorkspace_watershed ,   'travel_distance.geojson')

            if os.path.exists(sFilename_geojson):
                os.remove(sFilename_geojson)

            pDriver_geojson = ogr.GetDriverByName('GeoJSON')
            pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson)           
            pSrs = osr.SpatialReference()  
            pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
            pLayer = pDataset.CreateLayer('dist', pSrs, geom_type=ogr.wkbPolygon)
            # Add one attribute
            pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution       
            pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
            pFac_field.SetWidth(20)
            pFac_field.SetPrecision(2)
            pLayer.CreateField(pFac_field) #long type for high resolution

            pSlp_field = ogr.FieldDefn('dist', ogr.OFTReal)
            pSlp_field.SetWidth(20)
            pSlp_field.SetPrecision(8)
            pLayer.CreateField(pSlp_field) #long type for high resolution

            pLayerDefn = pLayer.GetLayerDefn()
            pFeature = ogr.Feature(pLayerDefn)

            with open(sFilename_json) as json_file:
                data = json.load(json_file)  
                ncell = len(data)
                lID =0 
                for i in range(ncell):
                    pcell = data[i]
                    lCellID = int(pcell['lCellID'])
                    lCellID_downslope = int(pcell['lCellID_downslope'])
                    x_start=float(pcell['dLongitude_center_degree'])
                    y_start=float(pcell['dLatitude_center_degree'])
                    dfac = float(pcell['DrainageArea'])
                    dElev = float(pcell['dDistance_to_watershed_outlet'])

                    vVertex = pcell['vVertex']
                    nvertex = len(vVertex)
                    pPolygon = ogr.Geometry(ogr.wkbPolygon)
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    for j in range(nvertex):
                        x = vVertex[j]['dLongitude_degree']
                        y = vVertex[j]['dLatitude_degree']
                        ring.AddPoint(x, y)

                    x = vVertex[0]['dLongitude_degree']
                    y = vVertex[0]['dLatitude_degree']
                    ring.AddPoint(x, y)
                    pPolygon.AddGeometry(ring)
                    pFeature.SetGeometry(pPolygon)
                    pFeature.SetField("id", lCellID)                
                    pFeature.SetField("fac", dfac)
                    pFeature.SetField("dist", dElev)

                    pLayer.CreateFeature(pFeature)
                pDataset = pLayer = pFeature  = None      
            pass  