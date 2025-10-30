
import sys
import os, stat
from pathlib import Path
from pyearth.system.python.get_python_environment import get_python_environment
def _pyhexwatershed_create_hpc_job(self, sSlurm_in=None, hours_in = 24):
    """create a HPC job for this simulation
    """
    os.chdir(self.sWorkspace_output)

    sConda_env_path , sConda_env_name,_ = get_python_environment()

    #part 1 python script

    sFilename_pyhexwatershed = os.path.join(str(Path(self.sWorkspace_output)) , "run_pyhexwatershed.py" )
    ofs_pyhexwatershed = open(sFilename_pyhexwatershed, 'w')

    sLine = '#!/qfs/people/liao313/.conda/envs/' +  sConda_env_name + '/bin/' + 'python3' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'import os' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = "os.environ['PROJ_LIB']=" + '"'+ sConda_env_path  + '/share/proj' +'"'+ '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = "os.environ['LD_LIBRARY_PATH']=" + '"' + sConda_env_path + '/lib:${LD_LIBRARY_PATH}"' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'from pyhexwatershed.configuration.read_configuration_file import pyhexwatershed_read_configuration_file' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'sFilename_configuration_in = ' + '"' + self.sFilename_model_configuration + '"\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration_in,'  \
        + 'iCase_index_in='+ str(self.iCase_index) + ',' \
        + 'iFlag_stream_burning_topology_in='+ str(self.iFlag_stream_burning_topology) + ',' \
        + 'iFlag_elevation_profile_in='+ str(self.iFlag_elevation_profile) + ',' \
        + 'iFlag_use_mesh_dem_in='+ str(self.iFlag_use_mesh_dem) + ',' \
        + 'iResolution_index_in='+ str(self.iResolution_index) + ',' \
        + 'dResolution_meter_in=' + "{:0f}".format(self.dResolution_meter)+ ',' \
        + 'sDggrid_type_in="'+ str(self.sDggrid_type) + '",' \
        + 'sDate_in="'+ str(self.sDate) + '",' \
        + 'sMesh_type_in="'+ str(self.sMesh_type) +'"' \
        + ')'  +   '\n'
    ofs_pyhexwatershed.write(sLine)
    if self.iFlag_global == 1:
        pass
    else:
        if self.iFlag_multiple_outlet ==1:
            if self.pPyFlowline.iFlag_flowline==1:
                for iBasin in range(self.pPyFlowline.nOutlet):
                    sLine = 'oPyhexwatershed.pPyFlowline.aBasin[' + str(iBasin) + '].dLatitude_outlet_degree=' \
                        +  "{:0f}".format(self.pPyFlowline.aBasin[iBasin].dLatitude_outlet_degree)+ '\n'
                    ofs_pyhexwatershed.write(sLine)
                    sLine = 'oPyhexwatershed.pPyFlowline.aBasin[' + str(iBasin) + '].dLongitude_outlet_degree=' \
                        +  "{:0f}".format(self.pPyFlowline.aBasin[iBasin].dLongitude_outlet_degree)+ '\n'
                    ofs_pyhexwatershed.write(sLine)
                    sLine = 'oPyhexwatershed.pPyFlowline.aBasin[' + str(iBasin) + '].dThreshold_small_river=' \
                        +  "{:0f}".format(self.pPyFlowline.aBasin[iBasin].dThreshold_small_river)+ '\n'
                    ofs_pyhexwatershed.write(sLine)
                    sLine = 'oPyhexwatershed.pPyFlowline.aBasin[' + str(iBasin) + '].sFilename_flowline_filter=' \
                        + "'" + self.pPyFlowline.aBasin[iBasin].sFilename_flowline_filter + "'" +'\n'
                    ofs_pyhexwatershed.write(sLine)

            pass
        else:
            if self.pPyFlowline.iFlag_flowline==1:
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=' \
                    +  "{:0f}".format(self.pPyFlowline.aBasin[0].dLatitude_outlet_degree)+ '\n'
                ofs_pyhexwatershed.write(sLine)
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=' \
                    + "{:0f}".format(self.pPyFlowline.aBasin[0].dLongitude_outlet_degree)+ '\n'
                ofs_pyhexwatershed.write(sLine)
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].dThreshold_small_river=' \
                    + "{:0f}".format(self.pPyFlowline.aBasin[0].dThreshold_small_river)+ '\n'
                ofs_pyhexwatershed.write(sLine)
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].sFilename_flowline_filter=' \
                    + "'"+ self.pPyFlowline.aBasin[0].sFilename_flowline_filter + "'" +'\n'
                ofs_pyhexwatershed.write(sLine)

    sLine = 'oPyhexwatershed.pyhexwatershed_setup()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'aCell_origin = oPyhexwatershed.pyhexwatershed_run_pyflowline()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    if self.iMesh_type !=4:
        sLine = 'oPyhexwatershed.pyhexwatershed_assign_elevation_to_cells()' + '\n'
        ofs_pyhexwatershed.write(sLine)
        sLine = 'aCell_new = oPyhexwatershed.pyhexwatershed_update_outlet(aCell_origin)' + '\n'
        ofs_pyhexwatershed.write(sLine)
    else:
        #possible has issue too
        if self.iFlag_use_mesh_dem == 1: #dem is within the mesh already
            pass
        else: #mpas mesh has no dem information
            sLine = 'oPyhexwatershed.pyhexwatershed_assign_elevation_to_cells()' + '\n'
            ofs_pyhexwatershed.write(sLine)
            sLine = 'aCell_new = oPyhexwatershed.pyhexwatershed_update_outlet(aCell_origin)' + '\n'
            ofs_pyhexwatershed.write(sLine)
        pass

    sLine = 'oPyhexwatershed.pPyFlowline.pyflowline_export()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pPyFlowline.pyflowline_analyze()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pPyFlowline.pyflowline_evaluate()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pyhexwatershed_export_config_to_json()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pyhexwatershed_run_hexwatershed()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pyhexwatershed_postrun()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pyhexwatershed_analyze()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.pyhexwatershed_export()' + '\n'
    ofs_pyhexwatershed.write(sLine)
    ofs_pyhexwatershed.close()
    os.chmod(sFilename_pyhexwatershed, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

    #part 2 bash script
    sFilename_job = os.path.join(str(Path(self.sWorkspace_output)  ) ,  "submit.job" )
    ofs = open(sFilename_job, 'w')
    sLine = '#!/bin/bash\n'
    ofs.write(sLine)
    sLine = '#SBATCH -A ESMD\n'
    ofs.write(sLine)
    sLine = '#SBATCH --job-name=' + self.sCase + '\n'
    ofs.write(sLine)

    sHour = "{:02d}".format(hours_in)
    sLine = '#SBATCH -t ' + sHour + ':00:00' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH --nodes=1' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH --ntasks-per-node=1' + '\n'
    ofs.write(sLine)
    if sSlurm_in is not None:
        sSlurm = sSlurm_in
    else:
        sSlurm = 'slurm'
    sLine = '#SBATCH --partition='+ sSlurm + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH -o stdout.out\n'
    ofs.write(sLine)
    sLine = '#SBATCH -e stderr.err\n'
    ofs.write(sLine)
    sLine = 'module purge\n'
    ofs.write(sLine)
    #sLine = 'module load gcc/10.2.0' + '\n' #this is only for the C++ component
    #ofs.write(sLine)
    sLine = 'module load python/miniconda2024May29 ' + '\n'
    ofs.write(sLine)
    sLine = 'source /share/apps/python/miniconda2024May29/etc/profile.d/conda.sh' + '\n'
    ofs.write(sLine)
    sLine = 'conda activate ' + sConda_env_name + '\n'
    ofs.write(sLine)
    sLine = 'cd $SLURM_SUBMIT_DIR\n'
    ofs.write(sLine)
    sLine = 'JOB_DIRECTORY='+ self.sWorkspace_output +  '\n'
    ofs.write(sLine)
    sLine = 'cd $JOB_DIRECTORY' +  '\n'
    ofs.write(sLine)

    #set system environment variable using the conda enviroment
    sLine = 'export PROJ_LIB='  + sConda_env_path  + '/share/proj' + '\n'
    ofs.write(sLine)
    #sLine = 'export LD_LIBRARY_PATH='  + sConda_env_path  + '/lib64' + '\n'
    sLine = 'export LD_LIBRARY_PATH=' + sConda_env_path + '/lib:$LD_LIBRARY_PATH' + '\n'
    ofs.write(sLine)

    if self.iFlag_profile == 0:
        sLine = 'python3 run_pyhexwatershed.py' +  '\n'
    else:
        #use cProfile tp run the code
        sLine = 'python3 -m cProfile -o cprofile.txt run_pyhexwatershed.py' +  '\n'

    ofs.write(sLine)
    sLine = 'conda deactivate' + '\n'
    ofs.write(sLine)
    ofs.close()
    return

def _pyhexwatershed_submit_hpc_job(self):
    #this is not fully recommended as it may affect the environment variable
    return