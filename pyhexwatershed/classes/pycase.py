import os, stat
from abc import ABCMeta, abstractmethod
import datetime
import json
from shutil import copy2
import subprocess

from json import JSONEncoder

from pathlib import Path
import numpy as np
from pyflowline.classes.pycase import flowlinecase
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)


class CaseClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, list):
            pass  
        if isinstance(obj, flowlinecase):
            return obj.sWorkspace_output 
            
        return JSONEncoder.default(self, obj)

class hexwatershedcase(object):
    __metaclass__ = ABCMeta  
    iFlag_resample_method=2 
    iFlag_flowline=1
    iFlag_global = 0
    iFlag_multiple_outlet = 0
    iFlag_elevation_profile = 0
    iFlag_stream_burning_topology=1
    iFlag_create_mesh= 1
    iFlag_simplification= 0
    iFlag_intersect= 0
    iFlag_merge_reach=1
    iMesh_type=4   
    iFlag_save_mesh = 0 

    iFlag_use_mesh_dem=0
    nOutlet=1  
    dResolution_degree=0.0
    dResolution_meter=0.0
    dThreshold_small_river=0.0
    dLongitude_left = -180
    dLongitude_right = 180
    dLatitude_bot = -90
    dLatitude_top = 90
    sFilename_dem=''  
    sFilename_model_configuration=''
    sFilename_mesh_info=''
    sFilename_flowline_info=''
    sFilename_basins=''
    
 
    sWorkspace_model_region=''    
    sWorkspace_bin=''
    
    sRegion=''
    sModel=''
    iMesh_type ='hexagon'

    sCase=''
    sDate=''    

    sFilename_spatial_reference=''
    sFilename_hexwatershed=''
    pPyFlowline = None
    sWorkspace_output_pyflowline=''
    sWorkspace_output_hexwatershed=''
    aBasin = list()


    def __init__(self, aConfig_in):
        print('HexWatershed compset is being initialized')
        self.sFilename_model_configuration    = aConfig_in[ 'sFilename_model_configuration']

        if 'sWorkspace_data' in aConfig_in:
            self.sWorkspace_data = aConfig_in[ 'sWorkspace_data']
        
        if 'sWorkspace_output' in aConfig_in:
            self.sWorkspace_output    = aConfig_in[ 'sWorkspace_output']

        if 'sWorkspace_project' in aConfig_in:
            self.sWorkspace_project= aConfig_in[ 'sWorkspace_project']

        if 'sWorkspace_bin' in aConfig_in:
            self.sWorkspace_bin= aConfig_in[ 'sWorkspace_bin']

        if 'sRegion' in aConfig_in:
            self.sRegion               = aConfig_in[ 'sRegion']

        if 'sModel' in aConfig_in:
            self.sModel                = aConfig_in[ 'sModel']
        
        #required with default variables

        if 'iFlag_resample_method' in aConfig_in:
            self.iFlag_resample_method       = int(aConfig_in[ 'iFlag_resample_method'])

        if 'iFlag_flowline' in aConfig_in:
            self.iFlag_flowline             = int(aConfig_in[ 'iFlag_flowline'])

        if 'iFlag_create_mesh' in aConfig_in:
            self.iFlag_create_mesh             = int(aConfig_in[ 'iFlag_create_mesh'])

        if 'iFlag_simplification' in aConfig_in:
            self.iFlag_simplification             = int(aConfig_in[ 'iFlag_simplification'])

        if 'iFlag_intersect' in aConfig_in:
            self.iFlag_intersect             = int(aConfig_in[ 'iFlag_intersect'])

        if 'iFlag_global' in aConfig_in:
            self.iFlag_global             = int(aConfig_in[ 'iFlag_global'])

        if 'iFlag_multiple_outlet' in aConfig_in:
            self.iFlag_multiple_outlet             = int(aConfig_in[ 'iFlag_multiple_outlet'])    

        if 'iFlag_use_mesh_dem' in aConfig_in:
            self.iFlag_use_mesh_dem             = int(aConfig_in[ 'iFlag_use_mesh_dem'])

        if 'iFlag_stream_burning_topology' in aConfig_in:
            self.iFlag_stream_burning_topology       = int(aConfig_in[ 'iFlag_stream_burning_topology'])

        if 'iFlag_save_mesh' in aConfig_in:
            self.iFlag_save_mesh             = int(aConfig_in[ 'iFlag_save_mesh'])

        #optional
        if 'iFlag_save_elevation' in aConfig_in:
            self.iFlag_save_elevation  = int(aConfig_in[ 'iFlag_save_elevation'])

        if 'iFlag_elevation_profile' in aConfig_in:
            self.iFlag_elevation_profile  = int(aConfig_in[ 'iFlag_elevation_profile'])

        if 'nOutlet' in aConfig_in:
            self.nOutlet             = int(aConfig_in[ 'nOutlet'])

        if 'dMissing_value_dem' in aConfig_in:
            self.dMissing_value_dem             = float(aConfig_in[ 'dMissing_value_dem'])

        if 'dBreach_threshold' in aConfig_in:
            self.dBreach_threshold             = float(aConfig_in[ 'dBreach_threshold'])

        if 'dAccumulation_threshold' in aConfig_in:
            self.dAccumulation_threshold             = float(aConfig_in[ 'dAccumulation_threshold'])
        
        if 'sFilename_spatial_reference' in aConfig_in:
            self.sFilename_spatial_reference = aConfig_in['sFilename_spatial_reference']

        if 'sFilename_dem' in aConfig_in:
            self.sFilename_dem = aConfig_in['sFilename_dem']

        if 'sFilename_mesh_netcdf' in aConfig_in:
            self.sFilename_mesh_netcdf = aConfig_in['sFilename_mesh_netcdf']

        if 'iCase_index' in aConfig_in:
            iCase_index = int(aConfig_in['iCase_index'])
        else:
            iCase_index = 1
        
       
        
        sDate   = aConfig_in[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default

        sCase_index = "{:03d}".format( iCase_index )
        self.iCase_index =   iCase_index
        sCase = self.sModel  + self.sDate + sCase_index
        self.sCase = sCase

        sPath = str(Path(self.sWorkspace_output)  /  sCase)
        self.sWorkspace_output = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        
        if 'sMesh_type' in aConfig_in:
            self.sMesh_type =  aConfig_in['sMesh_type']
        else:
            self.sMesh_type = 'hexagon'
        
        sMesh_type = self.sMesh_type
        if sMesh_type =='hexagon': #hexagon
            self.iMesh_type = 1
        else:
            if sMesh_type =='square': #sqaure
                self.iMesh_type = 2
            else:
                if sMesh_type =='latlon': #latlon
                    self.iMesh_type = 3
                else:
                    if sMesh_type =='mpas': #mpas
                        self.iMesh_type = 4
                    else:
                        if sMesh_type =='tin': #tin
                            self.iMesh_type = 5
                        else:
                            print('Unsupported mesh type?')
                            
        if 'dResolution_degree' in aConfig_in:
            self.dResolution_degree = float(aConfig_in['dResolution_degree']) 

        if 'dResolution_meter' in aConfig_in:
            self.dResolution_meter = float(aConfig_in['dResolution_meter']) 
        else:
            print('Please specify resolution.')

        if 'dLongitude_left' in aConfig_in:
            self.dLongitude_left = float(aConfig_in['dLongitude_left']) 

        if 'dLongitude_right' in aConfig_in:
            self.dLongitude_right = float(aConfig_in['dLongitude_right']) 

        if 'dLatitude_bot' in aConfig_in:
            self.dLatitude_bot = float(aConfig_in['dLatitude_bot']) 

        if 'dLatitude_top' in aConfig_in:
            self.dLatitude_top = float(aConfig_in['dLatitude_top']) 

        if 'sJob' in aConfig_in:
            self.sJob =  aConfig_in['sJob'] 

        if 'sFilename_hexwatershed' in aConfig_in:
            self.sFilename_hexwatershed= aConfig_in['sFilename_hexwatershed'] 

        if 'sWorkspace_bin' in aConfig_in:
            self.sWorkspace_bin = aConfig_in['sWorkspace_bin']
        else:
            print('The path to the hexwatershed binary is not specified.')
        
                
        if 'sFilename_basins' in aConfig_in:
            self.sFilename_basins = aConfig_in['sFilename_basins']
        else:
            self.sFilename_basins = ''              

        sPath = str(Path(self.sWorkspace_output)   / 'hexwatershed')
        self.sWorkspace_output_hexwatershed = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        sPath = str(Path(self.sWorkspace_output)   / 'pyflowline')
        self.sWorkspace_output_pyflowline = sPath
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sFilename_elevation = os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + "_elevation.json" )
        self.sFilename_mesh = os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + ".json" )
        self.sFilename_mesh_info  =  os.path.join(str(Path(self.sWorkspace_output_pyflowline)  ) , sMesh_type + "_mesh_info.json"  ) 
        
        
        return    

    def tojson(self):
        aSkip = ['aBasin']      

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
            pass

        sJson = json.dumps(obj,\
            sort_keys=True, \
            indent = 4, \
            ensure_ascii=True, \
            cls=CaseClassEncoder)
        return sJson

    def export_config_to_json(self):        

        sPath = os.path.dirname(self.sFilename_model_configuration)
        sName  = Path(self.sFilename_model_configuration).stem + '.json'
        sFilename_configuration  =  os.path.join( self.sWorkspace_output_hexwatershed,  sName )

        aSkip = ['aBasin', \
                'aFlowline_simplified','aFlowline_conceptual','aCellID_outlet',
                'aCell']
        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
            pass

        with open(sFilename_configuration, 'w', encoding='utf-8') as f:
            json.dump(obj, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=CaseClassEncoder)
        
   
        return
     
    def setup(self):
        self.pPyFlowline.setup()

        sFilename_hexwatershed = os.path.join(str(Path(self.sWorkspace_bin)  ) ,  self.sFilename_hexwatershed )
        #copy the binary file
        sFilename_new = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) ,  "hexwatershed" )
        copy2(sFilename_hexwatershed, sFilename_new)


        return
    
    def run_pyflowline(self):

        self.pPyFlowline.run()

        return
    
    def run_hexwatershed(self):
        #call hexwatershed binary

        sFilename_hexwatershed = os.path.join(self.sWorkspace_output_hexwatershed, "hexwatershed" )

        sFilename_configuration = self.sFilename_model_configuration
        sCommand = sFilename_hexwatershed + " "  + sFilename_configuration
        print(sCommand)
        p = subprocess.Popen(sCommand, shell= True)


        

        return
    
    def analyze(self):
        return

    def export(self):
        
        
        return

    def create_hpc_job(self):
        """create a HPC job for this simulation
        """

        os.chdir(self.sWorkspace_output)
        #writen normal run script
        sFilename_job = os.path.join(str(Path(self.sWorkspace_output)  ) ,  "submit.job" )
        ofs = open(sFilename_job, 'w')
        sLine = '#!/bin/bash\n'
        ofs.write(sLine)
        sLine = '#SBATCH -A ESMD\n'
        ofs.write(sLine)
        sLine = '#SBATCH --job-name=hex' + self.sCase + '\n'
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
        sLine = 'module load gcc/8.1.0' + '\n'
        ofs.write(sLine)
        sLine = 'module load anaconda3/2019.03' + '\n'
        ofs.write(sLine)
        sLine = 'source /share/apps/anaconda3/2019.03/etc/profile.d/conda.sh' + '\n'
        ofs.write(sLine)
        sLine = './hexwatershed ' + '.ini' + '\n'
        ofs.write(sLine)
        ofs.close()

        #run pyflowline script
        sFilename_pyflowline = os.path.join(str(Path(self.sWorkspace_output_pyflowline)) , "run_pyflowline.sh" )
        ofs_pyflowline = open(sFilename_pyflowline, 'w')

        sLine = '#!/bin/bash\n'
        ofs_pyflowline.write(sLine)

        sLine = 'echo "Started to prepare python scripts"\n'
        ofs_pyflowline.write(sLine)
        sLine = 'module load anaconda3/2019.03' + '\n'
        ofs_pyflowline.write(sLine)
        sLine = 'source /share/apps/anaconda3/2019.03/etc/profile.d/conda.sh' + '\n'
        ofs_pyflowline.write(sLine)
        sLine = 'conda activate pyflowlineenv' + '\n'
        ofs_pyflowline.write(sLine)

        sLine = 'cat << EOF > run_pyflowline.py' + '\n' 
        ofs_pyflowline.write(sLine)    
        sLine = '#!/qfs/people/liao313/.conda/envs/hexwatershedenv/bin/' + 'python3' + '\n' 
        ofs_pyflowline.write(sLine) 

        sLine = 'from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file' + '\n'
        ofs_pyflowline.write(sLine)
         
        sLine = 'sFilename_configuration_in = ' + '"' + self.sFilename_model_configuration + '"\n'
        ofs_pyflowline.write(sLine)
        sLine = 'oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,' + \
            'iCase_index_in='+ str(self.iCase_index) + ',' +  'sMesh_type_in="'+ str(self.sMesh_type) +'"' \
           + ')'  +   '\n'   
        ofs_pyflowline.write(sLine)
        
        sLine = 'oPyhexwatershed.pPyflowline.setup()' + '\n'   
        ofs_pyflowline.write(sLine)
        sLine = 'oPyhexwatershed.pPyflowline.run()' + '\n'   
        ofs_pyflowline.write(sLine)
        sLine = 'oPyhexwatershed.pPyflowline.analyze()' + '\n'   
        ofs_pyflowline.write(sLine)
        sLine = 'oPyhexwatershed.pPyflowline.export()' + '\n'   
        ofs_pyflowline.write(sLine)
        sLine = 'EOF\n'
        ofs_pyflowline.write(sLine)
        sLine = 'chmod 755 ' + 'run_pyflowline.py' + '\n'   
        ofs_pyflowline.write(sLine)


        sLine = './run_pyflowline.py'
        ofs_pyflowline.write(sLine)
        ofs_pyflowline.close()
        os.chmod(sFilename_pyflowline, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)

        
        
        #os.chmod(sFilename_new, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)
        
     
        return

    def submit_hpc_job(self):
        #this is not fully recommended as it may affect the environment variable

        return