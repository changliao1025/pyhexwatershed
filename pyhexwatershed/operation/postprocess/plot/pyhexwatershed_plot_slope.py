import sys, os, stat
import numpy as np
from pathlib import Path
import json
import subprocess

from pyearth.system.define_global_variables import *
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


import cartopy.crs as ccrs

#desired_proj = ccrs.NearsidePerspective(
#                        central_latitude=42.0,
 #                       central_longitude=-75.0,
  #                      satellite_height=10000.0)

desired_proj = ccrs.Orthographic(central_longitude=-75, central_latitude=42, globe=None)

#desired_proj = ccrs.PlateCarree()

def pyhexwatershed_plot_slope(oHexwatershed_in):

    sWorkspace_output_case = oHexwatershed_in.sWorkspace_output_case

    sFilename_json = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'hexwatershed.json'
    sFilename_out = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'slope_between.png'
    #sFilename_mesh = sWorkspace_output_case + slash +  'mpas_mesh_info.json'

    #ax = plt.subplot( 1, projection=desired_proj)
    fig = plt.figure( dpi=300 )
    fig.set_figwidth( 12 )
    fig.set_figheight( 12 )
    ax = fig.add_axes([0.1, 0.5, 0.8, 0.4] , projection=desired_proj )
    #ax = plt.subplot(2, 1,  1, projection=desired_proj)
    ax.set_global()
    
    #with open(sFilename_mesh) as mesh_file:
    #    mesh_data = json.load(mesh_file)        
    #    ncell0 = len(mesh_data)
    
    aPatch=[]
    aSlope_between=[]
    with open(sFilename_json) as json_file:
        data = json.load(json_file)        

        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]
           
            delev = float(pcell['dSlope_between'])
            aSlope_between.append(delev)

    aSlope_between = np.array(aSlope_between)
    dElev_min = np.min(aSlope_between)
    dElev_max = np.max(aSlope_between)

    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180

    cmap = matplotlib.cm.get_cmap('Spectral')
    norm=plt.Normalize(dElev_min,dElev_max)

    with open(sFilename_json) as json_file:
        data = json.load(json_file)        

        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start=float(pcell['dLongitude_center_degree'])
            y_start=float(pcell['dLatitude_center_degree'])
            dfac = float(pcell['DrainageArea'])
            delev = float(pcell['dSlope_between'])

            avertex = pcell['vVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )
            #this is the cell
            #get the vertex
            
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude']
                aLocation[k,1] = avertex[k]['dLatitude']

                if aLocation[k,0] > dLon_max:
                    dLon_max = aLocation[k,0]
                
                if aLocation[k,0] < dLon_min:
                    dLon_min = aLocation[k,0]
                
                if aLocation[k,1] > dLat_max:
                    dLat_max = aLocation[k,1]

                if aLocation[k,1] < dLat_min:
                    dLat_min = aLocation[k,1]

            color_index = (delev-dElev_min ) /(dElev_max - dElev_min )
            rgba = cmap(color_index)
            polygon = mpatches.Polygon(aLocation, closed=True, facecolor=rgba, alpha=0.8, edgecolor=rgba,transform=ccrs.PlateCarree() )
            #aPatch.append(polygon)
            ax.add_patch(polygon)                   
                    
    #trasform elevation
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(aSlope_between)
    fig.colorbar(sm, ax=ax)
    
    dDiff_lon = dLon_max - dLon_min
    dDiff_lat = dLat_max - dLat_min
   
    ax.set_extent([dLon_min + 0.5 * dDiff_lon , dLon_max - 0.2 * dDiff_lon, dLat_min- 0.1 * dDiff_lat , dLat_max -  0.75 * dDiff_lat])
    ax.coastlines()#resolution='110m')
    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.3, linestyle='--')

    
    #plt.show()
    plt.savefig(sFilename_out, bbox_inches='tight')
    
    pDataset = pLayer = pFeature  = None      
    return


