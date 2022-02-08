import os, sys
import datetime
sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *
from eslib.toolbox.reader.read_configuration_file import read_configuration_file

sPath_hexcoastal_python = sWorkspace_code +  slash \
    + 'python' + slash \
    + 'hexcoastal' + slash + 'hexcoastal_python'
sys.path.append(sPath_hexcoastal_python)

from hexcoastal.shared.hexcoastal_global import *

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)



def hexcoastal_read_configuration_file(sFilename_configuration_in,\
                                    iCase_index_in = None, \
                                 iFlag_debug_in = None, \
                                 sDate_in = None):

    config = read_configuration_file(sFilename_configuration_in)
    sModel = config['sModel']
    sRegion = config['sRegion']
    sVariable = config['sVariable']
    sFilename_mesh = config['sFilename_mesh']

    dLatitude_top = float( config['dLatitude_top'] )
    dLatitude_bot = float( config['dLatitude_bot'] )
    dLongitude_left = float( config['dLongitude_left'] )
    dLongitude_right = float( config['dLongitude_right'] )
   
    
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = sDate_default
        pass
    if iCase_index_in is not None:
        iCase_index = iCase_index_in
    else:
        iCase_index = 0
    sCase_index = "{:03d}".format(iCase_index)
        #important change here

    sCase = sModel + sDate + sCase_index
 
    jigsaw_mesh.dLatitude_top = dLatitude_top
    jigsaw_mesh.dLatitude_bot = dLatitude_bot
    jigsaw_mesh.dLongitude_left = dLongitude_left
    jigsaw_mesh.dLongitude_right = dLongitude_right
    jigsaw_mesh.sFilename_mesh = sFilename_mesh
    jigsaw_mesh.sFilename_clip = sFilename_mesh + '.clip'
    return
