import os, stat
from pathlib import Path
def _create_hpc_job(self, sSlurm_in=None):
    """create a HPC job for this simulation
    """
    os.chdir(self.sWorkspace_output)
    
    #part 1 python script         
    
    sFilename_pyhexwatershed = os.path.join(str(Path(self.sWorkspace_output)) , "run_pyhexwatershed.py" )
    ofs_pyhexwatershed = open(sFilename_pyhexwatershed, 'w')
       
    sLine = '#!/qfs/people/liao313/.conda/envs/hexwatershed/bin/' + 'python3' + '\n' 
    ofs_pyhexwatershed.write(sLine) 
    sLine = 'from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file' + '\n'
    ofs_pyhexwatershed.write(sLine)         
    sLine = 'sFilename_configuration_in = ' + '"' + self.sFilename_model_configuration + '"\n'
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,'  \
        + 'iCase_index_in='+ str(self.iCase_index) + ',' \
        + 'iFlag_stream_burning_topology_in='+ str(self.iFlag_stream_burning_topology) + ',' \
        + 'iFlag_elevation_profile_in='+ str(self.iFlag_elevation_profile) + ',' \
        + 'iFlag_use_mesh_dem_in='+ str(self.iFlag_use_mesh_dem) + ',' \
        + 'iResolution_index_in='+ str(self.iResolution_index) + ',' \
        + 'dResolution_meter_in=' + "{:0f}".format(self.dResolution_meter)+ ',' \
        + 'sDggrid_type_in="'+ str(self.sDggrid_type) + '",' \
        +  'sDate_in="'+ str(self.sDate) + '",' \
        +  'sMesh_type_in="'+ str(self.sMesh_type) +'"' \
        + ')'  +   '\n'   
    ofs_pyhexwatershed.write(sLine)
    if self.iFlag_global == 1:
        pass
    else:
        if self.iFlag_multiple_outlet ==1:
            pass
        else:
            if self.pPyFlowline.iFlag_flowline==1:
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=' \
                    +  "{:0f}".format(self.pPyFlowline.aBasin[0].dLatitude_outlet_degree)+ '\n'   
                ofs_pyhexwatershed.write(sLine)
                sLine = 'oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=' \
                    + "{:0f}".format(self.pPyFlowline.aBasin[0].dLongitude_outlet_degree)+ '\n'   
                ofs_pyhexwatershed.write(sLine)        
    sLine = 'oPyhexwatershed.setup()' + '\n'   
    ofs_pyhexwatershed.write(sLine)
    sLine = 'aCell_origin = oPyhexwatershed.run_pyflowline()' + '\n'   
    ofs_pyhexwatershed.write(sLine) 
    if self.iMesh_type !=4:            
        sLine = 'aCell_out = oPyhexwatershed.assign_elevation_to_cells()' + '\n'   
        ofs_pyhexwatershed.write(sLine)      
        sLine = 'aCell_new = oPyhexwatershed.update_outlet(aCell_out, aCell_origin)' + '\n'   
        ofs_pyhexwatershed.write(sLine)       
    else:
        #possible has issue too
        
        pass    
    sLine = 'oPyhexwatershed.pPyFlowline.export()' + '\n'   
    ofs_pyhexwatershed.write(sLine)      
    sLine = 'oPyhexwatershed.export_config_to_json()' + '\n'   
    ofs_pyhexwatershed.write(sLine)   
    sLine = 'oPyhexwatershed.run_hexwatershed()' + '\n'   
    ofs_pyhexwatershed.write(sLine)
    sLine = 'oPyhexwatershed.analyze()' + '\n'   
    ofs_pyhexwatershed.write(sLine)      
    sLine = 'oPyhexwatershed.export()' + '\n'   
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
    sLine = '#SBATCH -t 90:00:00' + '\n'
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
    sLine = 'module load gcc/8.1.0' + '\n'
    ofs.write(sLine)
    sLine = 'module load anaconda3/2019.03' + '\n'
    ofs.write(sLine)
    sLine = 'source /share/apps/anaconda3/2019.03/etc/profile.d/conda.sh' + '\n'
    ofs.write(sLine)    
    sLine = 'conda activate hexwatershed' + '\n'
    ofs.write(sLine)
    sLine = 'cd $SLURM_SUBMIT_DIR\n'
    ofs.write(sLine)
    sLine = 'JOB_DIRECTORY='+ self.sWorkspace_output +  '\n'
    ofs.write(sLine)
    sLine = 'cd $JOB_DIRECTORY' +  '\n'
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

def _submit_hpc_job(self):
    #this is not fully recommended as it may affect the environment variable
    return