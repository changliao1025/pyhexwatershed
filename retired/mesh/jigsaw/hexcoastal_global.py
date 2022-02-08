import os, sys
import datetime
sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *
from eslib.toolbox.reader.read_configuration_file import read_configuration_file

sPath_hexcoastal_python = sWorkspace_code +  slash + 'python' + slash \
    + 'hexcoastal' + slash + 'hexcoastal_python'
sys.path.append(sPath_hexcoastal_python)

from hexcoastal.mesh.jigsaw_mesh import jigsaw_mesh


aParameter = {}
jMesh = jigsaw_mesh(aParameter)