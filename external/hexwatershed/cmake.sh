#!/bin/bash
module load cmake/3.11.4
module load gcc/8.1.0
module load gdal/2.3.1
module load anaconda3/2019.03
source /share/apps/anaconda3/2019.03/etc/profile.d/conda.sh
conda activate sphinx
cmake ..
