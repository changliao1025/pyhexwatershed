import os, sys
import numpy as np

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system.define_global_variables import *

sPath_hexcoastal_python = sWorkspace_code +  slash + 'python' + slash \
    + 'hexcoastal' + slash + 'hexcoastal_python'
sys.path.append(sPath_hexcoastal_python)

from hexcoastal.mesh.hexcoastal_clip_mesh_by_rectangle import hexcoastal_clip_mesh_by_rectangle

def hexcoastal(sFilename_configuration):
    hexcoastal_clip_mesh_by_rectangle(sFilename_configuration)

    pass

if __name__ == '__main__':
    sModel = 'hexcoastal'
    sRegion = 'delaware'
    sFilename_configuration = sWorkspace_configuration + slash \
        + sModel + slash \
        + sRegion + slash + 'coastal_configuration.txt'
    hexcoastal(sFilename_configuration)
