import os, sys
import math
import numpy as np
from netCDF4 import Dataset


sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system.define_global_variables import *

sPath_hexcoastal_python = sWorkspace_code +  slash \
    + 'python' + slash \
    + 'hexcoastal' + slash + 'hexcoastal_python'
sys.path.append(sPath_hexcoastal_python)

from hexcoastal.shared.hexcoastal_global import *
from hexcoastal.shared.hexcoastal_read_configuration_file import hexcoastal_read_configuration_file

def hexcoastal_clip_mesh_by_rectangle(sFilename_configuration):


    hexcoastal_read_configuration_file(sFilename_configuration)

    
    dLatitude_top = jigsaw_mesh.dLatitude_top   
    dLatitude_bot = jigsaw_mesh.dLatitude_bot  
    dLongitude_left = jigsaw_mesh.dLongitude_left 
    dLongitude_right = jigsaw_mesh.dLongitude_right 
    sFilename_mesh = jigsaw_mesh.sFilename_mesh
    sFilename_clip = jigsaw_mesh.sFilename_clip
    

    #read netcdf
    if (os.path.isfile(sFilename_mesh)):
        pass
    else:
        print('Mesh file does not exist!')
        exit
    pDatasets_in = Dataset(sFilename_mesh)


    netcdf_format = pDatasets_in.file_format

    
        

    #write new netcdf
    for sKey, aValue in pDatasets_in.variables.items():        
        print(aValue.datatype)
        print(aValue.dimensions)

        #we need to filter out unused grids based on mpas specs
        if sKey == 'latCell':
            aLatiude = aValue
        else:
            pass
        if sKey == 'lonCell':
            aLongtitude = aValue 
        else:
            pass

    
    #conver unit 
    aLatitude = aLatiude[:] / math.pi * 180
    aLongitude = aLongtitude[:] / math.pi * 180

    aIndex = np.where( ( dLatitude_bot<aLatitude ) \
        & (  aLatitude<dLatitude_top) \
        & (  dLongitude_left<aLongitude) \
        & (  aLongitude<dLongitude_right) )

    #save the result
    pDatasets_out = Dataset(sFilename_clip, "w", format=netcdf_format)
    for sKey, iValue in pDatasets_in.dimensions.items():
        dummy = len(iValue)
        if not iValue.isunlimited():            
            pDatasets_out.createDimension(sKey, dummy)            
        else:
            pDatasets_out.createDimension(sKey, dummy )
    pDatasets_out.close()

    pass
