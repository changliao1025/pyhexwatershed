import os
import sys
from os.path import realpath
from pathlib import Path

from pyhexwatershed.configuration import load_configuration

# ===========================
# setup workspace path
# ===========================
sPath_parent = str(Path(__file__).parents[2])  # data is located two dir's up
sPath_data = realpath(sPath_parent + "/data/susquehanna")
sWorkspace_input = str(Path(sPath_data) / "input")
sWorkspace_output = str(Path(sPath_data) / "output")

# ===================================
# YAML workflow configuration file (auto-resolves .yaml / .yml / .json)
# ===================================
sFilename_configuration_in = realpath(
    sPath_parent + "/examples/susquehanna/pyhexwatershed_susquehanna_mpas.yaml"
)

# ===========================
# setup case information
# ===========================
iCase_index = 1
dResolution_meter = 5000
sMesh_type = "mpas"
sDate = "20220801"

oPyhexwatershed = load_configuration(
    sFilename_configuration_in,
    case_index=iCase_index,
    resolution_meter=dResolution_meter,
    date=sDate,
    mesh_type=sMesh_type,
)

if oPyhexwatershed.iFlag_global == 1:
    # global simulation
    # we can only support MPAS/latlon mesh at global scale right now
    pass
else:
    # domain simulation
    if oPyhexwatershed.iFlag_multiple_outlet == 1:
        pass
    else:
        # single basin example
        # mpas mesh has elevation built-in
        oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree = 39.4620
        oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree = -76.0093
        oPyhexwatershed.setup()
        oPyhexwatershed.pPyFlowline.dLongitude_left = -79
        oPyhexwatershed.pPyFlowline.dLongitude_right = -74.5
        oPyhexwatershed.pPyFlowline.dLatitude_bot = 39.20
        oPyhexwatershed.pPyFlowline.dLatitude_top = 42.8
        oPyhexwatershed.run_pyflowline()
        oPyhexwatershed.pPyFlowline.export()
        oPyhexwatershed.export_config_to_json()
        oPyhexwatershed.run_hexwatershed()
        oPyhexwatershed.analyze()
        oPyhexwatershed.export()

print("Finished")
