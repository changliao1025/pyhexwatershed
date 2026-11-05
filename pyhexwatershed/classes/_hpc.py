import os
from pathlib import Path
import stat
import sys

from pyearth.system.python.get_python_environment import get_python_environment


def _pyhexwatershed_create_hpc_job(self, sSlurm_in=None, hours_in=24):
    """create a HPC job for this simulation"""
    os.chdir(self.sWorkspace_output)

    sConda_env_path, sConda_env_name, _ = get_python_environment()

    # part 1 python script
    sFilename_pyhexwatershed = os.path.join(str(Path(self.sWorkspace_output)), "run_pyhexwatershed.py")
    ofs_pyhexwatershed = open(sFilename_pyhexwatershed, "w")

    sLine = f"#!/qfs/people/liao313/.conda/envs/{sConda_env_name}/bin/python3\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = "import os\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = f'os.environ["PROJ_LIB"] = "{sConda_env_path}/share/proj"\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = f'os.environ["LD_LIBRARY_PATH"] = "{sConda_env_path}/lib:${{LD_LIBRARY_PATH}}"\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = "from pyhexwatershed.configuration.read_configuration_file import pyhexwatershed_read_configuration_file\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = f'sFilename_configuration_in = "{self.sFilename_model_configuration}"\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = (
        f"oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration_in,"
        f"iCase_index_in={self.iCase_index},"
        f"iFlag_stream_burning_topology_in={self.iFlag_stream_burning_topology},"
        f"iFlag_elevation_profile_in={self.iFlag_elevation_profile},"
        f"iFlag_use_mesh_dem_in={self.iFlag_use_mesh_dem},"
        f"iResolution_index_in={self.iResolution_index},"
        f"dResolution_meter_in={self.dResolution_meter:0f},"
        f'sDggrid_type_in="{self.sDggrid_type}",'
        f'sDate_in="{self.sDate}",'
        f'sMesh_type_in="{self.sMesh_type}")\n'
    )
    ofs_pyhexwatershed.write(sLine)
    if self.iFlag_global == 1:
        pass
    else:
        if self.iFlag_multiple_outlet == 1:
            if self.pPyFlowline.iFlag_flowline == 1:
                for iBasin in range(self.pPyFlowline.nOutlet):
                    sLine = (
                        f"oPyhexwatershed.pPyFlowline.aBasin[{iBasin}].dLatitude_outlet_degree="
                        f"{self.pPyFlowline.aBasin[iBasin].dLatitude_outlet_degree:0f}\n"
                    )
                    ofs_pyhexwatershed.write(sLine)
                    sLine = (
                        f"oPyhexwatershed.pPyFlowline.aBasin[{iBasin}].dLongitude_outlet_degree="
                        f"{self.pPyFlowline.aBasin[iBasin].dLongitude_outlet_degree:0f}\n"
                    )
                    ofs_pyhexwatershed.write(sLine)
        else:
            if self.pPyFlowline.iFlag_flowline == 1:
                sLine = (
                    f"oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree="
                    f"{self.pPyFlowline.aBasin[0].dLatitude_outlet_degree:0f}\n"
                )
                ofs_pyhexwatershed.write(sLine)
                sLine = (
                    f"oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree="
                    f"{self.pPyFlowline.aBasin[0].dLongitude_outlet_degree:0f}\n"
                )
                ofs_pyhexwatershed.write(sLine)

    sLine = "oPyhexwatershed.pyhexwatershed_setup()\n"
    ofs_pyhexwatershed.write(sLine)

    if self.iFlag_flowline == 1:
        sLine = "oPyhexwatershed.pyhexwatershed_run_pyflowline()\n"
        ofs_pyhexwatershed.write(sLine)

    sLine = "aCell_origin = oPyhexwatershed.pPyFlowline.aCell\n"
    ofs_pyhexwatershed.write(sLine)
    if self.iMesh_type != 4:
        sLine = "oPyhexwatershed.pyhexwatershed_assign_elevation_to_cells()\n"
        ofs_pyhexwatershed.write(sLine)
        sLine = "aCell_new = oPyhexwatershed.pyhexwatershed_update_outlet(aCell_origin)\n"
        ofs_pyhexwatershed.write(sLine)
    else:
        pass
    sLine = "oPyhexwatershed.pPyFlowline.pyflowline_export()\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = "oPyhexwatershed.pyhexwatershed_export_config_to_json()\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = "oPyhexwatershed.pyhexwatershed_run_hexwatershed()\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = "oPyhexwatershed.pyhexwatershed_analyze()\n"
    ofs_pyhexwatershed.write(sLine)
    sLine = "oPyhexwatershed.pyhexwatershed_export()\n"
    ofs_pyhexwatershed.write(sLine)
    ofs_pyhexwatershed.close()
    os.chmod(sFilename_pyhexwatershed, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

    # part 2 bash script
    sFilename_job = os.path.join(str(Path(self.sWorkspace_output)), "submit.job")
    ofs = open(sFilename_job, "w")
    sLine = "#!/bin/bash\n"
    ofs.write(sLine)
    sLine = "#SBATCH -A ESMD\n"
    ofs.write(sLine)
    sLine = f"#SBATCH --job-name={self.sCase}\n"
    ofs.write(sLine)

    sHour = f"{hours_in:02d}"
    sLine = f"#SBATCH -t {sHour}:00:00\n"
    ofs.write(sLine)
    sLine = "#SBATCH --nodes=1\n"
    ofs.write(sLine)
    sLine = "#SBATCH --ntasks-per-node=1\n"
    ofs.write(sLine)
    if sSlurm_in is not None:
        sSlurm = sSlurm_in
    else:
        sSlurm = "slurm"
    sLine = f"#SBATCH --partition={sSlurm}\n"
    ofs.write(sLine)
    sLine = "#SBATCH -o stdout.out\n"
    ofs.write(sLine)
    sLine = "#SBATCH -e stderr.err\n"
    ofs.write(sLine)
    sLine = "module purge\n"
    ofs.write(sLine)
    sLine = "module load python/miniconda2024May29\n"
    ofs.write(sLine)
    sLine = "source /share/apps/python/miniconda2024May29/etc/profile.d/conda.sh\n"
    ofs.write(sLine)
    sLine = f"conda activate {sConda_env_name}\n"
    ofs.write(sLine)
    sLine = "cd $SLURM_SUBMIT_DIR\n"
    ofs.write(sLine)
    sLine = f"JOB_DIRECTORY={self.sWorkspace_output}\n"
    ofs.write(sLine)
    sLine = "cd $JOB_DIRECTORY\n"
    ofs.write(sLine)

    sLine = f"export PROJ_LIB={sConda_env_path}/share/proj\n"
    ofs.write(sLine)
    sLine = f"export LD_LIBRARY_PATH={sConda_env_path}/lib:$LD_LIBRARY_PATH\n"
    ofs.write(sLine)

    if self.iFlag_profile == 0:
        sLine = "python3 run_pyhexwatershed.py\n"
    else:
        sLine = "python3 -m cProfile -o cprofile.txt run_pyhexwatershed.py\n"

    ofs.write(sLine)
    sLine = "conda deactivate\n"
    ofs.write(sLine)
    ofs.close()
    return


def _pyhexwatershed_submit_hpc_job(self):
    return
