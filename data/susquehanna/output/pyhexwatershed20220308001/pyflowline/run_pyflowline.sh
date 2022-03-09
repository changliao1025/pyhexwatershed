#!/bin/bash
echo "Started to prepare python scripts"
module load anaconda3/2019.03
source /share/apps/anaconda3/2019.03/etc/profile.d/conda.sh
conda activate pyflowlineenv
cat << EOF > run_pyflowline.py
#!/qfs/people/liao313/.conda/envs/hexwatershedenv/bin/python3
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
sFilename_configuration_in = "/qfs/people/liao313/workspace/python/pyhexwatershed/tests/configurations/template.json"
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,iCase_index_in=1,sMesh_type_in="mpas")
oPyhexwatershed.pPyflowline.setup()
oPyhexwatershed.pPyflowline.run()
oPyhexwatershed.pPyflowline.analyze()
oPyhexwatershed.pPyflowline.export()
EOF
chmod 755 run_pyflowline.py
./run_pyflowline.py