import sys, os, stat
import numpy as np
from pathlib import Path
import json
import subprocess

from pyearth.system.define_global_variables import *
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

#import cartopy.crs as ccrs

#desired_proj = ccrs.NearsidePerspective(
#                        central_latitude=50.72,
#                        central_longitude=-3.53,
#                        satellite_height=10000000.0)

def pyhexwatershed_plot_elevation(oHexwatershed_in):

    sWorkspace_output_case = oHexwatershed_in.sWorkspace_output_case

    sFilename_json = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'hexwatershed.json'
    sFilename_mesh = sWorkspace_output_case + slash +  'mpas_mesh_info.json'

    #ax = plt.subplot( 1, projection=desired_proj)
    fig = plt.figure( dpi=100 )
    fig.set_figwidth( 12 )
    fig.set_figheight( 10 )
    ax = fig.add_axes([0.1, 0.5, 0.8, 0.4] )
    #ax.set_global()
    patches = []
    with open(sFilename_mesh) as mesh_file:
        mesh_data = json.load(mesh_file)        
        ncell0 = len(mesh_data)

    with open(sFilename_json) as json_file:
        data = json.load(json_file)        

        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start=float(pcell['dLon_center'])
            y_start=float(pcell['dLat_center'])
            dfac = float(pcell['DrainageArea'])
            delev = float(pcell['Elevation'])

            #read vertex
            for j in range(ncell0):
                pcell0 = mesh_data[j]
                lCellID0 =  int(pcell0['lCellID'])
                if(lCellID == lCellID0):
                    nvertex =  int(pcell0['nVertex'])
                    aLocation= np.full( (nvertex, 2), 0.0, dtype=float )
                    #this is the cell
                    #get the vertex
                    avertex = pcell0['aVertex']
                    for k in range(nvertex):
                        aLocation[k,0] = avertex[k]['dLongitude']
                        aLocation[k,1] = avertex[k]['dLatitude']


                    polygon = Polygon(aLocation, True)
                    patches.append(polygon)
         
    #trasform elevation
   

    ax.coastlines(resolution='110m')
    ax.gridlines()
    plt.show()
    pDataset = pLayer = pFeature  = None      
    return


