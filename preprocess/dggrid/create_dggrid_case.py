
import sys, os, stat
import numpy as np
from pathlib import Path
from shutil import copy2

import subprocess
import datetime
sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from pyes.system.define_global_variables import *

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)
sDate = '20201015'
def create_dggrid_case( iCase_index, \
    iResolution_index ,\
        sGrid_type,\
        sFilename_crop_shapefile_in =None ):

    sCase = "{:03d}".format( iCase_index )
    sResolution = "{:02d}".format( iResolution_index )
    if sFilename_crop_shapefile_in is not None:
        if os.path.isfile(sFilename_crop_shapefile_in):
            iFlag_crop =1
            sFilename_crop_shapefile = sFilename_crop_shapefile_in
        else:
            iFlag_crop = 0
    else:
        iFlag_crop = 0




    sCase_folder = sWorkspace_job + slash + sGrid_type + sResolution + slash + 'case'  +  sDate + sCase
    sFolder_out = sWorkspace_out  + slash + sGrid_type + sResolution + slash + 'case'  +  sDate + sCase
    sFilename_out = sFolder_out + slash + sGrid_type + sResolution 

    if (os.path.exists(sFolder_out)):
        sCommand = 'rm -rf '  + sFolder_out
        print(sCommand)
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()
    Path(sFolder_out).mkdir(parents=True, exist_ok=True)

    if (os.path.exists(sCase_folder)):
        sCommand = 'rm -rf '  + sCase_folder
        print(sCommand)
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

    Path(sCase_folder).mkdir(parents=True, exist_ok=True)
    os.chdir(sCase_folder)
     #write configuration
    sFilename_config= sCase_folder + slash + sRegion +'.ini'
    ofs = open(sFilename_config, 'w')
    sLine = 'dggrid_operation GENERATE_GRID' + '\n'
    ofs.write(sLine)
    sLine = 'dggs_type ' + sGrid_type.upper() + '\n'
    ofs.write(sLine)
    sLine = 'dggs_res_spec ' + sResolution + '\n'
    ofs.write(sLine)

    if iFlag_crop ==1:
        sLine = 'clip_region_files ' + sFilename_crop_shapefile + '\n'
        ofs.write(sLine)
        sLine = 'clip_subset_type SHAPEFILE'  + '\n'
        ofs.write(sLine)

    else:
        pass

    sLine = 'update_frequency 10000000'+ '\n'
    ofs.write(sLine)
    sLine = 'cell_output_type SHAPEFILE' + '\n'
    ofs.write(sLine)
    sLine = 'cell_output_file_name ' + sFilename_out + '\n'
    ofs.write(sLine)
    sLine = 'densification 3' + '\n'
    ofs.write(sLine)
    sLine = 'max_cells_per_output_file 0'  + '\n'
    ofs.write(sLine)
    
    ofs.close()


    #writen normal run script
    sFilename_bash = sCase_folder + slash + 'run.sh'
    ofs = open(sFilename_bash, 'w')
    sLine = '#!/bin/bash\n'
    ofs.write(sLine)
    sLine = 'module load gcc/5.2.0\n'
    ofs.write(sLine)
    
    sLine = './dggrid ' + sRegion + '.ini' + '\n'
    ofs.write(sLine)
    ofs.close()
    os.chmod(sFilename_bash, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

    #write job file
    sFilename_job = sCase_folder + slash + 'submit.job'
    ofs = open(sFilename_job, 'w')
    sLine = '#!/bin/bash\n'
    ofs.write(sLine)
    sLine = '#SBATCH -A br21_liao313\n'
    ofs.write(sLine)
    sLine = '#SBATCH  --job-name=dggrid' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH -t '+ sWalltime +':00:00' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH  --nodes=1' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH  --ntasks-per-node=1' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH  --partition=slurm' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH -o stdout.out\n'
    ofs.write(sLine)
    sLine = '#SBATCH -e stderr.err\n'
    ofs.write(sLine)
    sLine = '#SBATCH --mail-type=ALL\n'
    #ofs.write(sLine)
    sLine = '#SBATCH --mail-user=chang.liao@pnnl.gov\n'
    ofs.write(sLine)
    sLine = 'cd $SLURM_SUBMIT_DIR\n'
    ofs.write(sLine)
    sLine = 'module purge\n'
    ofs.write(sLine)
    sLine = 'module load gcc/5.2.0\n'
    ofs.write(sLine)
    
    sLine = './dggrid ' + sRegion + '.ini' + '\n'
    ofs.write(sLine)
    ofs.close()
   
    #copy execulate
    sFilename_new = sCase_folder + slash + 'dggrid'
    copy2(sFilename_dggrid, sFilename_new)
    os.chmod(sFilename_new, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)
    sCommand =  'sbatch submit.job' + '\n'
    sCommand = sCommand.lstrip()
    os.chdir(sCase_folder)
    
    p = subprocess.Popen(sCommand, shell= True)
    p.wait()
    return

if __name__ == '__main__':


    sRegion = 'conus'

    

    sWorkspace_job = '/qfs/people/liao313/jobs/' + 'dggrid' + slash + sRegion + slash + 'simulation'
    sWorkspace_out = '/pic/scratch/liao313/04model/dggrid/' + slash + sRegion + slash + 'simulation'
    sFilename_dggrid = '/qfs/people/liao313/bin/dggrid'

    sFilename_boundary = '/qfs/people/liao313/data/dggrid/conus/vector/conus.shp'
    iCase_index = 1
    sGrid_type='isea3h'
    for i  in np.arange(1, 15):
        sWalltime =  "{:02d}".format( iCase_index )
        iResolution_index = i 
        create_dggrid_case( iCase_index, \
                    iResolution_index ,  \
                        sGrid_type,
                       sFilename_crop_shapefile_in=  sFilename_boundary)
        

       



    pass