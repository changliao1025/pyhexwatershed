
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
sDate = '20210308'
def create_hexwatershed_compset(iFlag_resample_method, iFlag_stream_burning, iFlag_stream_burning_topology,\
    iCase_index,\
     lMeshID_outlet,\
    dAccumulation_threshold , \
        sResolution, \
            sFilename_dem, \
                sMissing_value_dem):

    if (sResolution == '20k' ):
        if(iFlag_resample_method ==1):
            lMeshID_outlet = 1166
            pass
           
        

    sCase = "{:03d}".format( iCase_index )

    sCase_folder = sWorkspace_job + slash + 'case' + sDate + sCase

    if (os.path.exists(sCase_folder)):
        sCommand = 'rm -rf '  + sCase_folder
        print(sCommand)
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()
    else:
        print(sCase_folder)

    Path(sCase_folder).mkdir(parents=True, exist_ok=True)
    

    os.chdir(sCase_folder)
    #writen normal run script
    sFilename_bash = sCase_folder + slash + 'run.sh'
    ofs = open(sFilename_bash, 'w')
    sLine = '#!/bin/bash\n'
    ofs.write(sLine)
    sLine = 'module load gcc/8.1.0\n'
    ofs.write(sLine)
    sLine = 'module load gdal/2.3.1' + '\n'
    ofs.write(sLine)
    sLine = 'module load netcdf/4.6.3' + '\n'
    ofs.write(sLine)
    sLine = './hexwatershed ' +sRegion+'.ini' + '\n'
    ofs.write(sLine)
    ofs.close()
    os.chmod(sFilename_bash, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)
    #write job file
    sFilename_job = sCase_folder + slash + 'submit.job'
    ofs = open(sFilename_job, 'w')
    sLine = '#!/bin/bash\n'
    ofs.write(sLine)
    sLine = '#SBATCH -A ESMD\n'
    ofs.write(sLine)
    sLine = '#SBATCH --job-name=hexwatershed' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH -t 1:00:00' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH --nodes=1' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH --ntasks-per-node=1' + '\n'
    ofs.write(sLine)
    sLine = '#SBATCH --partition=short' + '\n'
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
    sLine = 'module load gcc/8.1.0\n'
    ofs.write(sLine)
    sLine = 'module load gdal/2.3.1' + '\n'
    ofs.write(sLine)
    sLine = 'module load netcdf/4.6.3' + '\n'
    ofs.write(sLine)
    sLine = './hexwatershed ' + sRegion + '.ini' + '\n'
    ofs.write(sLine)
    ofs.close()
    #write configuration
    sFilename_config= sCase_folder + slash +  sRegion +'.ini'
    ofs = open(sFilename_config, 'w')
    sLine = 'sDate, '+ sDate + '\n'
    ofs.write(sLine)
    sLine = 'sWorkspace_data, /people/liao313/data/hexwatershed/' + sRegion + '\n'
    ofs.write(sLine)
    sLine = 'sWorkspace_output, /compyfs/liao313/04model/hexwatershed/'+ sRegion+'/output'+ '\n'
    ofs.write(sLine)
    sLine = 'sFilename_hexagon_polygon_shapefile, grid' + sResolution + '.shp'+ '\n'
    ofs.write(sLine)
    sLine = 'sFilename_nhd_flowline_shapefile, grid' + sResolution + '_str.shp' + '\n'
    ofs.write(sLine)
    sLine = 'sFilename_elevation_raster, ' + sFilename_dem + '\n'
    ofs.write(sLine)
    #sLine = 'dMissing_value_dem, -32768' + '\n'
    sLine = 'dMissing_value_dem, ' + sMissing_value_dem + '\n'
    ofs.write(sLine)
    sLine = 'iFlag_nhd_flowline, ' +   "{:0d}".format( iFlag_stream_burning )  + '\n'
    ofs.write(sLine)
    sLine = 'iFlag_stream_burning_topology, ' +   "{:0d}".format( iFlag_stream_burning_topology )  + '\n'
    ofs.write(sLine)
    
    sLine = 'iFlag_resample_method, ' +   "{:0d}".format( iFlag_resample_method )  + '\n'
    ofs.write(sLine)
    if (iFlag_stream_burning ==1):
        sLine = 'lMeshID_outlet, ' + "{:0d}".format( lMeshID_outlet )   + '\n'
        ofs.write(sLine)
    else:
        pass
    sLine = 'iCase, '  + sCase + '\n'
    ofs.write(sLine)
    sLine = 'dAccumulation_threshold, ' + "{:0d}".format( dAccumulation_threshold ) + '\n'
    ofs.write(sLine)
    ofs.close()
    #copy execulate
    sFilename_new = sCase_folder + slash + 'hexwatershed'
    copy2(sFilename_hexwatershed, sFilename_new)
    os.chmod(sFilename_new, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

    sCommand =  'sbatch ./submit.job' + '\n'
    sCommand = sCommand.lstrip()
    os.chdir(sCase_folder)
    #p = subprocess.Popen(['/bin/bash', '-i', '-c', sCommand])
    p = subprocess.Popen(sCommand, shell= True)
    p.wait()
    return

if __name__ == '__main__':


    sRegion = 'columbia_river_basin'
    #sRegion = 'susquehanna'

    
    
    #crb
    if sRegion == 'columbia_river_basin':
        aResolution = ['5k', '10k', '20k', '40k']
        aAccumulation_threshold =[1000, 250, 60, 15]
        aMeshID_outlet =[19595, 4848, 1240, 324]
        sFilename_dem='crbdem.tif'
        sMissing_value_dem='-32768'
    else: 
        #susquehanna
        if sRegion == 'susquehanna':
            aResolution = ['5k', '10k', '20k']
            aAccumulation_threshold =[100, 50, 10]
            aMeshID_outlet =[4664, 1162, 297]
            sFilename_dem='dem1.tif'
            sMissing_value_dem='-9999'
        else:

            #aAccumulation_threshold =[1000, 250, 60, 15]
            pass

    nResolution  = len(aResolution)

    sWorkspace_job = '/qfs/people/liao313/jobs/hexwatershed/' +sRegion +'/simulation'
    sFilename_hexwatershed = '/qfs/people/liao313/workspace/cplus/hexwatershed_dev/hexwatershed_dev/bin/hexwatershed'
    iCase_index = 1

    iFlag_resample_method = 2
    for i  in np.arange(nResolution):
        
        if i !=3 :
            continue

        iCase_index = i* nResolution + 1
        dAccumulation_threshold = aAccumulation_threshold[i]
        sResolution = aResolution[i]
        
        lMeshID_outlet = aMeshID_outlet[i]
        iFlag_stream_burning_topology = 0
        iFlag_stream_burning = 1
        create_hexwatershed_case(iFlag_resample_method, iFlag_stream_burning, iFlag_stream_burning_topology, \
            iCase_index, \
                    lMeshID_outlet,dAccumulation_threshold ,  sResolution, sFilename_dem, sMissing_value_dem)
        iCase_index = iCase_index + 1

        iFlag_stream_burning_topology = 1 
        iFlag_stream_burning = 1
        create_hexwatershed_case(iFlag_resample_method, iFlag_stream_burning, iFlag_stream_burning_topology, \
            iCase_index, \
                     lMeshID_outlet,dAccumulation_threshold , sResolution, sFilename_dem, sMissing_value_dem)
        

        continue

        iFlag_resample_method = 2
        iFlag_stream_burning = 0
        create_hexwatershed_case(iFlag_resample_method, iFlag_stream_burning, iFlag_stream_burning_topology,iCase_index, \
                     lMeshID_outlet,dAccumulation_threshold , sResolution, sFilename_dem, sMissing_value_dem)
        iCase_index = iCase_index + 1

        iFlag_resample_method = 2 
        iFlag_stream_burning = 1
        create_hexwatershed_case(iFlag_resample_method, iFlag_stream_burning, iFlag_stream_burning_topology,iCase_index, \
                     lMeshID_outlet ,dAccumulation_threshold, sResolution, sFilename_dem, sMissing_value_dem)
        iCase_index = iCase_index + 1



    pass