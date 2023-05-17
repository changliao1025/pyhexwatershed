import os, stat
import json
from shutil import copy2
from pathlib import Path
from osgeo import gdal, ogr, osr, gdalconst
import numpy as np
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.animation as animation 
from matplotlib.animation import FuncAnimation

mpl.use("Agg")
from shapely.wkt import loads
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

from pyhexwatershed.algorithm.auxiliary.statistics import remap

pProjection_map_deafult = ccrs.Orthographic(central_longitude=  0.0, \
        central_latitude= 0.0, globe=None)
#pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
        
iFigwidth_default = 12
iFigheight_default = 12

def _animate(self, sFilename_in, \
        iFlag_type_in = None, \
        iFigwidth_in=None, iFigheight_in=None,\
            aExtent_in = None,\
        pProjection_map_in = None):

    if iFigwidth_in is None:
        iFigwidth_in = iFigwidth_default

    if iFigheight_in is None:
        iFigheight_in = iFigheight_default 

    if pProjection_map_in is None:
        pProjection_map = pProjection_map_deafult
    else:
        pProjection_map = pProjection_map_in

    #read domain json 
    sFilename_pyflowline =  self.sFilename_mesh_info
    #read result json
    sFilename_domain_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'domain.json' )

    #read animation json
    sFilename_animation_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'animation.json' )
    
    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180 
    aCellID = list() 
    aData = list()
    aCell_raw = list()
    aCell_new = list()
    aCell_animation = list()
    with open(sFilename_pyflowline) as json_file:
        aCell_raw = json.load(json_file)     
        ncell_raw = len(aCell_raw)
        lID =0         
        for i in range(ncell_raw):
            pcell = aCell_raw[i]     
            lCellID = int(pcell['lCellID'])  
            dummy = float(pcell["dElevation_mean"])
            aData.append(dummy)
            aCellID.append(lCellID)  
            avertex = pcell['aVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )
            #this is the cell
            #get the vertex
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude_degree']
                aLocation[k,1] = avertex[k]['dLatitude_degree']
                if aLocation[k,0] > dLon_max:
                    dLon_max = aLocation[k,0]
                if aLocation[k,0] < dLon_min:
                    dLon_min = aLocation[k,0]
                if aLocation[k,1] > dLat_max:
                    dLat_max = aLocation[k,1]
                if aLocation[k,1] < dLat_min:
                    dLat_min = aLocation[k,1]

    pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
    fig = plt.figure( dpi=100 )
    fig.set_figwidth( iFigwidth_in )
    fig.set_figheight( iFigheight_in )
    ax = fig.add_axes([0.1, 0.1, 0.65, 0.8] , projection=pProjection_map )    
    ax.set_global()   

    aData = np.array(aData)        
    dData_max = np.max(aData)   
    dData_min = np.min(aData) 
    marginx  = (dLon_max - dLon_min) / 20
    marginy  = (dLat_max - dLat_min) / 20
    if aExtent_in is None:        
        aExtent = [dLon_min - marginx , dLon_max + marginx , dLat_min -marginy , dLat_max + marginy]
    else:
        aExtent = aExtent_in  

    ax.set_extent(aExtent)
    ax.coastlines()#resolution='110m') 
    if iFlag_type_in ==1: #full
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.3, linestyle='--')
        gl.xlabel_style = {'size': 8, 'color': 'k', 'rotation':0, 'ha':'right'}
        gl.ylabel_style = {'size': 8, 'color': 'k', 'rotation':90,'weight': 'normal'}
    else: #track mode

        pass
    cmap = cm.get_cmap('Spectral')
    # setting a title for the plot 
    sText = 'Priority flood in HexWatershed'
    ax.text(0.5, 1.05, sText, \
    verticalalignment='center', horizontalalignment='center',\
        transform=ax.transAxes, \
        color='black', fontsize=9)
    cmap_reversed = cmap.reversed() 
    
    with open(sFilename_domain_json) as json_file:
        aCell_new = json.load(json_file) 
        ncell_new = len(aCell_new)

    with open(sFilename_animation_json) as json_file:
        aCell_animation = json.load(json_file) 
        ncell_animation = len(aCell_animation)

    #initialization function 
    #aPolygon=list() 
    #for i in range(ncell_raw):
    #    pcell = aCell_raw[i]              
    #    dummy = float(pcell['dElevation_mean'])
    #    avertex = pcell['aVertex']
    #    nvertex = len(avertex)
    #    aLocation= np.full( (nvertex, 2), 0.0, dtype=float )             
    #    for k in range(nvertex):
    #        aLocation[k,0] = avertex[k]['dLongitude_degree']
    #        aLocation[k,1] = avertex[k]['dLatitude_degree']
    #      
    #    color_index = (dummy-dData_min ) /(dData_max - dData_min )
    #    rgb = cmap_reversed(color_index)
    #    polygon = mpatches.Polygon(aLocation, closed=True, facecolor=rgb,\
    #        edgecolor='none',transform=ccrs.PlateCarree() )
      
        #aPolygon.append(ax.add_patch(polygon) )  

    sText = ''
    x1 = 0.0
    y1 = 0.0
    pArtist1 = ax.text(x1, y1, sText, \
    verticalalignment='center', horizontalalignment='right',\
        transform=ax.transAxes, \
        color='black', fontsize=12)
    
    x2 = 0.0
    y2 = 0.0
    pArtist2 = ax.text(x2, y2, sText, \
    verticalalignment='center', horizontalalignment='left',\
        transform=ax.transAxes, \
        color='black', fontsize=12) 

    #trasform elevation
    norm=plt.Normalize(dData_min,dData_max)
    sm = plt.cm.ScalarMappable(cmap=cmap_reversed, norm=norm)
    sm.set_array(aData)
    ax_cb= fig.add_axes([0.85, 0.12, 0.04, 0.75])
    cb = fig.colorbar(sm, cax=ax_cb)       
    sUnit = r'Unit: m'     
    cb.ax.get_yaxis().set_ticks_position('right')
    cb.ax.get_yaxis().labelpad = 5
    cb.ax.set_ylabel(sUnit, rotation=90)
    cb.ax.get_yaxis().set_label_position('left')
    cb.ax.tick_params(labelsize=6)  
    
    def animate(i):
        aArtist=list()
    	#get the time step global id and updated elevation
        pcell_animation = aCell_animation[i]
        lCellID = int(pcell_animation['lCellID'])
        lCellIndex = aCellID.index(lCellID)
        
        pcell_new  = aCell_new[lCellIndex]
        dlon= float(pcell_new['dLongitude_center_degree'])
        dlat = float(pcell_new['dLatitude_center_degree'])
        dummy0= float(pcell_new['Elevation_raw'])
        dummy = float(pcell_new['Elevation'])
        avertex = pcell_new['vVertex']
        nvertex = len(avertex)
        aLocation= np.full( (nvertex, 2), 0.0, dtype=float )
        for k in range(nvertex):
            aLocation[k,0] = avertex[k]['dLongitude_degree']
            aLocation[k,1] = avertex[k]['dLatitude_degree']
        
        color_index = (dummy-dData_min ) /(dData_max - dData_min )
        rgb = cmap_reversed(color_index)
        polygon = mpatches.Polygon(aLocation, closed=True, facecolor=rgb,\
            edgecolor='none',transform=ccrs.PlateCarree() )
        pArtist0 = ax.add_patch(polygon)

        if iFlag_type_in ==1:
            dLon_min_zoom = dLon_min
            dLon_max_zoom = dLon_max
            dLat_min_zoom = dLat_min
            dLat_max_zoom = dLat_max
        else:
            dLon_min_zoom = dlon - marginx * 2
            dLon_max_zoom = dlon + marginx * 2
            dLat_min_zoom = dlat - marginy * 2 
            dLat_max_zoom = dlat + marginy * 2

        if dummy0 > dummy:
            x1 = (dlon - dLon_min_zoom)/(dLon_max_zoom-dLon_min_zoom)
            y1 = (dlat - dLat_min_zoom)/(dLat_max_zoom-dLat_min_zoom) + 0.05
            x2 = (dlon - dLon_min_zoom)/(dLon_max_zoom-dLon_min_zoom)
            y2 = (dlat - dLat_min_zoom)/(dLat_max_zoom-dLat_min_zoom) - 0.05
        else:
            x1 = (dlon - dLon_min_zoom)/(dLon_max_zoom-dLon_min_zoom)
            y1 = (dlat - dLat_min_zoom)/(dLat_max_zoom-dLat_min_zoom) - 0.05
            x2 = (dlon - dLon_min_zoom)/(dLon_max_zoom-dLon_min_zoom)
            y2 = (dlat - dLat_min_zoom)/(dLat_max_zoom-dLat_min_zoom) + 0.05

        sText1 = 'Before: ' + "{:0.2f}".format( dummy0 ) + 'm'
        
        pArtist1.set_x(x1)
        pArtist1.set_y(y1)
        pArtist1.set_text(sText1)
        sText2 = 'After: ' + "{:0.2f}".format( dummy ) + 'm'
        
        pArtist2.set_x(x2)
        pArtist2.set_y(y2)
        pArtist2.set_text(sText2)  

        if iFlag_type_in ==2:
            aExtent_zoom = [dlon - marginx * 2 , dlon + marginx * 2, dlat -marginy * 2, dlat + marginy* 2]
            ax.set_extent(aExtent_zoom)       

        return pArtist0 , pArtist1, pArtist2
  
    plt.rcParams["animation.convert_path"] = "/share/apps/ImageMagick/7.1.0-52/bin/convert"   
    #init_func=init,\
    anim = FuncAnimation(fig, animate, \
                                   frames=ncell_animation, interval=400, blit=False)
    anim.save(sFilename_in,writer="imagemagick") 

    return

def _plot(self, sFilename_in, \
        iFlag_type_in = None, \
        sVariable_in=None, \
        aExtent_in = None, \
        iFigwidth_in=None, iFigheight_in=None,\
        pProjection_map_in = None):

     
    
    if iFlag_type_in == 1: #polygon based          
        self._plot_mesh_with_variable(sFilename_in,sVariable_in, aExtent_in= aExtent_in,  iFigwidth_in=iFigwidth_in, iFigheight_in=iFigheight_in, pProjection_map_in= pProjection_map_in)            
    else:
        if iFlag_type_in == 2: #polyline based
            self._plot_flow_direction(sFilename_in,aExtent_in= aExtent_in, iFigwidth_in=iFigwidth_in, iFigheight_in=iFigheight_in, pProjection_map_in= pProjection_map_in)
            pass
        else: #mesh + line
            if iFlag_type_in == 3:
                self._plot_mesh_with_flow_direction(sFilename_in,aExtent_in= aExtent_in,iFigwidth_in=iFigwidth_in, iFigheight_in=iFigheight_in,  pProjection_map_in= pProjection_map_in)
                pass
            else:
                self._plot_mesh_with_flow_direction_and_river_network(sFilename_in,aExtent_in= aExtent_in, iFigwidth_in=iFigwidth_in, iFigheight_in=iFigheight_in, pProjection_map_in= pProjection_map_in)
                pass
    
    return
    
def _plot_mesh_with_variable(self, sFilename_in, sVariable_in, aExtent_in=None,  iFigwidth_in=None, iFigheight_in=None, pProjection_map_in = None, \
    dData_min_in = None, dData_max_in = None):

    if self.iMesh_type !=4:
        if sVariable_in == 'elevation':
            sVariable='Elevation'
            sTitle = 'Surface elevation'
            sUnit = r'Unit: m'
            dData_min = dData_min_in
            dData_max = dData_max_in
        else:
            if sVariable_in == 'drainagearea': 
                sVariable='DrainageArea'
                sTitle = 'Drainage area'
                sUnit = r'Unit: $m^{2}$'
                dData_min = dData_min_in
                dData_max = dData_max_in
            else:
                if sVariable_in == 'distance_to_outlet': 
                    sVariable='dDistance_to_watershed_outlet'
                    sTitle = 'Travel distance'
                    sUnit = r'Unit: m'
                    dData_min = 0.0
                    dData_max = dData_max_in
                else:    
                    sVariable='dSlope_between'
                    sTitle = 'Surface slope'
                    sUnit = r'Unit: percent'
                    dData_min = dData_min_in
                    dData_max = dData_max_in
    else:
        if sVariable_in == 'elevation':
            sVariable='Elevation' #Elevation_profile'
            sTitle = 'Surface elevation'
            sUnit = 'Unit: m'
            dData_min = dData_min_in
            dData_max = dData_max_in
        else:
            if sVariable_in == 'drainagearea': 
                sVariable='DrainageArea'
                sTitle = 'Drainage area'
                sUnit = r'Unit: $m^{2}$'
                dData_min = dData_min_in
                dData_max = dData_max_in
            else:
                if sVariable_in == 'distance_to_outlet': 
                    sVariable='dDistance_to_watershed_outlet'
                    sTitle = 'Distance to outlet'
                    sUnit = r'Unit: m'
                    dData_min = 0.0
                    dData_max = dData_max_in
                else:
                    sVariable='dSlope_between'
                    sTitle = 'Surface slope'
                    sUnit = 'Unit: percent'
                    dData_min = 0.0
                    dData_max = dData_max_in
    
    if iFigwidth_in is None:
        iFigwidth = iFigwidth_default

    if iFigheight_in is None:
        iFigheight = iFigheight_default 

    if pProjection_map_in is None:
        pProjection_map = pProjection_map_deafult
    else:
        pProjection_map = pProjection_map_in
     
    sFilename_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'hexwatershed.json' )
    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180
    with open(sFilename_json) as json_file:
        data = json.load(json_file)     
        ncell = len(data)       
        for i in range(ncell):
            pcell = data[i]         
            avertex = pcell['vVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )         
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude_degree']
                aLocation[k,1] = avertex[k]['dLatitude_degree']
                if aLocation[k,0] > dLon_max:
                    dLon_max = aLocation[k,0]
                if aLocation[k,0] < dLon_min:
                    dLon_min = aLocation[k,0]
                if aLocation[k,1] > dLat_max:
                    dLat_max = aLocation[k,1]
                if aLocation[k,1] < dLat_min:
                    dLat_min = aLocation[k,1]

    pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
    fig = plt.figure( dpi=300 )
    fig.set_figwidth( iFigwidth )
    fig.set_figheight( iFigheight )
    ax = fig.add_axes([0.1, 0.15, 0.75, 0.8] , projection=pProjection_map )    
    ax.set_global()     
    aData=[]
    with open(sFilename_json) as json_file:
        data = json.load(json_file)      
        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]
            dummy = float(pcell[sVariable])
            aData.append(dummy)

    aData = np.array(aData)  
    cmap = cm.get_cmap('Spectral')
    cmap_reversed = cmap.reversed()

    if dData_max is None:
        dData_max = np.max(aData)
    if dData_min is None:
        dData_min = np.min(aData)

    norm=plt.Normalize(dData_min,dData_max)
    with open(sFilename_json) as json_file:
        data = json.load(json_file)     
        ncell = len(data)       
        for i in range(ncell):
            pcell = data[i]            
            dummy = float(pcell[sVariable])
            avertex = pcell['vVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )  
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude_degree']
                aLocation[k,1] = avertex[k]['dLatitude_degree']
            color_index = (dummy-dData_min ) /(dData_max - dData_min )
            rgba = cmap_reversed(color_index)
            polygon = mpatches.Polygon(aLocation, closed=True, facecolor=rgba,\
                edgecolor='none',transform=ccrs.PlateCarree() )            
            ax.add_patch(polygon)    
 
    #trasform elevation
    sm = plt.cm.ScalarMappable(cmap=cmap_reversed, norm=norm)
    sm.set_array(aData)
    cb = fig.colorbar(sm, ax=ax)        
    
    cb.ax.get_yaxis().set_ticks_position('right')
    cb.ax.get_yaxis().labelpad = 5
    cb.ax.set_ylabel(sUnit, rotation=90)
    cb.ax.get_yaxis().set_label_position('left')
    cb.ax.tick_params(labelsize=6)     
   
    if aExtent_in is None:
        marginx  = (dLon_max - dLon_min) / 20
        marginy  = (dLat_max - dLat_min) / 20
        aExtent = [dLon_min - marginx , dLon_max + marginx , dLat_min -marginy , dLat_max + marginy]
    else:
        aExtent = aExtent_in

    ax.set_extent(aExtent)
    ax.coastlines()#resolution='110m')        
    ax.set_title(sTitle , loc='center')        
        
    #sText = 'Case index: ' + "{:0d}".format( self.iCase_index  )
    #ax.text(0.05, 0.95, sText, \
    #verticalalignment='top', horizontalalignment='left',\
    #        transform=ax.transAxes, \
    #        color='black', fontsize=12)
    sText = 'Mesh type: ' + self.sMesh_type.title()
    ax.text(0.05, 0.90, sText, \
    verticalalignment='top', horizontalalignment='left',\
            transform=ax.transAxes, \
            color='black', fontsize=12)
    sResolution =  'Resolution: ' + "{:0d}".format( int(self.dResolution_meter) ) + 'm'
    if self.sMesh_type != 'mpas':
        ax.text(0.05, 0.85, sResolution, \
            verticalalignment='top', horizontalalignment='left',\
            transform=ax.transAxes, \
            color='black', fontsize=12)
    else:
        pass
    if self.iFlag_stream_burning_topology ==1:
        sText = 'Stream topology: on'  
    else:
        sText = 'Stream topology: off'  
    ax.text(0.05, 0.80, sText, \
    verticalalignment='top', horizontalalignment='left',\
            transform=ax.transAxes, \
            color='black', fontsize=12)
 
    # Extract first layer of features from shapefile using OGR
    #sFilename_boundary = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_wgs.geojson'
    #pDriver = ogr.GetDriverByName('GeoJSON')
    #pDataset = pDriver.Open(sFilename_boundary, gdal.GA_ReadOnly)
    #pLayer = pDataset.GetLayer(0)
    #
    #paths = []
    #
    ## Read all features in layer and store as paths
    #for pFeature in pLayer:
    #    geom = pFeature.geometry()
    #    codes = []
    #    all_x = []
    #    all_y = []
    #    ng = geom.GetGeometryCount()
    #    for i in range(ng):
    #        # Read ring geometry and create path
    #        r = geom.GetGeometryRef(i)
    #        sGeometry_type = geom.GetGeometryName()                
    #        if(sGeometry_type == 'MULTIPOLYGON'):
    #            for geom_part in geom:
    #                ng2 = geom_part.GetGeometryCount()
    #                for k in range(ng2):
    #                    dummy= geom_part.GetGeometryRef(k)                        
    #                    lpoint =  dummy.GetPointCount()
    #                    if lpoint>0:
    #                        x = [dummy.GetX(j) for j in range(lpoint)]
    #                        y = [dummy.GetY(j) for j in range(lpoint)]
    #                        # skip boundary between individual rings
    #                        codes += [mpath.Path.MOVETO] + \
    #                                     (len(x)-1)*[mpath.Path.LINETO]
    #                        all_x += x
    #                        all_y += y
    #                        path = mpath.Path(np.column_stack((all_x,all_y)), codes)
    #                        paths.append(path)
    #                    else:
    #                        pass
    #        else:
    #            print('single')
        
    # Add paths as patches to axes
    #for path in paths:
    #    patch = mpatches.PathPatch(path, \
    #            facecolor='none', edgecolor='red' , linewidth=0.3)
    #    ax.add_patch(patch)
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.3, linestyle='--')
    gl.xlabel_style = {'size': 8, 'color': 'k', 'rotation':0, 'ha':'right'}
    gl.ylabel_style = {'size': 8, 'color': 'k', 'rotation':90,'weight': 'normal'}
    
    
    plt.savefig(sFilename_in, bbox_inches='tight')
    pDataset = pLayer = pFeature  = None      
     
    return
 
def _plot_flow_direction(self, sFilename_in, aExtent_in=None,  iFigwidth_in=None, iFigheight_in=None,pProjection_map_in = None):   
    if iFigwidth_in is None:
        iFigwidth = iFigwidth_default

    if iFigheight_in is None:
        iFigheight = iFigheight_default 

    if pProjection_map_in is None:
        pProjection_map = pProjection_map_deafult
    else:
        pProjection_map = pProjection_map_in     
    sTitle = 'Flow direction'
    
    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180 

    pDriver = ogr.GetDriverByName('GeoJSON')
    sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed, 'flow_direction.geojson')
    pDataset = pDriver.Open(sFilename_geojson, gdal.GA_ReadOnly)
    pLayer = pDataset.GetLayer(0)
    for pFeature in pLayer:
        pGeometry_in = pFeature.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        dFlow_accumulation = pFeature.GetField("fac")
        if sGeometry_type =='LINESTRING':
            dummy0 = loads( pGeometry_in.ExportToWkt() )
            aCoords_gcs = dummy0.coords
            aCoords_gcs= np.array(aCoords_gcs)
            aCoords_gcs = aCoords_gcs[:,0:2]
            dLon_max = np.max( [dLon_max, np.max(aCoords_gcs[:,0])] )
            dLon_min = np.min( [dLon_min, np.min(aCoords_gcs[:,0])] )
            dLat_max = np.max( [dLat_max, np.max(aCoords_gcs[:,1])] )
            dLat_min = np.min( [dLat_min, np.min(aCoords_gcs[:,1])] )
            
    pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
    fig = plt.figure( dpi=300)
    fig.set_figwidth( iFigwidth )
    fig.set_figheight( iFigheight )
    ax = fig.add_axes([0.1, 0.15, 0.85, 0.8] , projection=pProjection_map ) #request.crs
    ax.set_global()
    
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon    
    lID = 0     
    
    n_colors = pLayer.GetFeatureCount()        
    colours = cm.rainbow(np.linspace(0, 1, n_colors))
    aFlow_accumulation =list()
    for pFeature in pLayer:        
        dFlow_accumulation = pFeature.GetField("fac")
        aFlow_accumulation.append(dFlow_accumulation)
    
    aFlow_accumulation = np.array(aFlow_accumulation)
    dFlow_accumulation_max = np.max(aFlow_accumulation)
    print(dFlow_accumulation_max/1.0E6)
    dFlow_accumulation_min = np.min(aFlow_accumulation)
    iThickness_max = 2.5
    iThickness_min = 0.3
    for pFeature in pLayer:
        pGeometry_in = pFeature.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        dFlow_accumulation = pFeature.GetField("fac")
        if sGeometry_type =='LINESTRING':
            dummy0 = loads( pGeometry_in.ExportToWkt() )
            aCoords_gcs = dummy0.coords
            aCoords_gcs= np.array(aCoords_gcs)
            nvertex = len(aCoords_gcs)       
            
            codes = np.full(nvertex, mpath.Path.LINETO, dtype=int )
            codes[0] = mpath.Path.MOVETO
            path = mpath.Path(aCoords_gcs[:,0:2], codes)            
            x, y = zip(*path.vertices)
            #caluculate line thickess
            iThickness = remap( dFlow_accumulation, dFlow_accumulation_min, dFlow_accumulation_max, iThickness_min, iThickness_max )               
            line, = ax.plot(x, y, color= 'black',linewidth=iThickness, transform=ccrs.PlateCarree())            
            lID = lID + 1
        else:
            print('multiple')
            pass                  
    

    if aExtent_in is None:
        marginx  = (dLon_max - dLon_min) / 20
        marginy  = (dLat_max - dLat_min) / 20
        aExtent = [dLon_min - marginx , dLon_max + marginx , dLat_min -marginy , dLat_max + marginy]
    else:
        aExtent = aExtent_in
             
    sFilename  = Path(sFilename_geojson).stem + self.sCase + '.png'
    
    ax.set_extent(aExtent)  
    ax.coastlines()#resolution='110m')       
    gl = ax.gridlines( draw_labels=True,\
                  linewidth=0.2, color='gray', alpha=0.3, linestyle='--')
    gl.xlocator = mticker.MaxNLocator(5)
    gl.ylocator = mticker.MaxNLocator(5)
    gl.xlabel_style = {'size': 8, 'color': 'k', 'rotation':0, 'ha':'right'}
    gl.ylabel_style = {'size': 8, 'color': 'k', 'rotation':90,'weight': 'normal'}
    ax.set_title( sTitle.capitalize()) #, fontsize =  8*4)    
    plt.savefig(sFilename_in, bbox_inches='tight')  
    pDataset = pLayer = pFeature  = None  
    return

def _plot_mesh_with_flow_direction(self,sFilename_in, aExtent_in = None,  iFigwidth_in=None, iFigheight_in=None,pProjection_map_in = None):
    if iFigwidth_in is None:
        iFigwidth = iFigwidth_default

    if iFigheight_in is None:
        iFigheight = iFigheight_default 

    if pProjection_map_in is None:
        pProjection_map = pProjection_map_deafult
    else:
        pProjection_map = pProjection_map_in
    sTitle = 'Flow direction'
    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180 
    sFilename_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'hexwatershed.json' )
    with open(sFilename_json) as json_file:
        data = json.load(json_file)     
        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]    
            avertex = pcell['vVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )         
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude_degree']
                aLocation[k,1] = avertex[k]['dLatitude_degree']
                if aLocation[k,0] > dLon_max:
                    dLon_max = aLocation[k,0]
                if aLocation[k,0] < dLon_min:
                    dLon_min = aLocation[k,0]
                if aLocation[k,1] > dLat_max:
                    dLat_max = aLocation[k,1]
                if aLocation[k,1] < dLat_min:
                    dLat_min = aLocation[k,1]
    pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
    fig = plt.figure( dpi=300)
    fig.set_figwidth( iFigwidth )
    fig.set_figheight( iFigheight )
    ax = fig.add_axes([0.1, 0.15, 0.85, 0.8] , projection=pProjection_map ) #request.crs
    ax.set_global()
    
    with open(sFilename_json) as json_file:
        data = json.load(json_file)     
        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]           
            avertex = pcell['vVertex']
            nvertex = len(avertex)
            aLocation= np.full( (nvertex, 2), 0.0, dtype=float )   
            for k in range(nvertex):
                aLocation[k,0] = avertex[k]['dLongitude_degree']
                aLocation[k,1] = avertex[k]['dLatitude_degree']     
            polygon = mpatches.Polygon(aLocation, closed=True, facecolor='none', alpha=0.8, linewidth=0.1,\
                edgecolor='black',transform=ccrs.PlateCarree() )
            ax.add_patch(polygon)     

    pDriver = ogr.GetDriverByName('GeoJSON')
    sFilename_geojson = os.path.join(self.sWorkspace_output_hexwatershed, 'flow_direction.geojson')
    pDataset = pDriver.Open(sFilename_geojson, gdal.GA_ReadOnly)
    pLayer = pDataset.GetLayer(0)

    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    lID = 0            

    #ax.add_image(request, 6)    # 5 = zoom level
    n_colors = pLayer.GetFeatureCount()
    
    colours = cm.rainbow(np.linspace(0, 1, n_colors))
    aFlow_accumulation =list()
    for pFeature in pLayer:        
        dFlow_accumulation = pFeature.GetField("fac")
        aFlow_accumulation.append(dFlow_accumulation)
    
    aFlow_accumulation = np.array(aFlow_accumulation)
    dFlow_accumulation_max = np.max(aFlow_accumulation)
    dFlow_accumulation_min = np.min(aFlow_accumulation)
    iThickness_max = 2.5
    iThickness_min = 0.3
    for pFeature in pLayer:
        pGeometry_in = pFeature.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        dFlow_accumulation = pFeature.GetField("fac")
        if sGeometry_type =='LINESTRING':
            dummy0 = loads( pGeometry_in.ExportToWkt() )
            aCoords_gcs = dummy0.coords
            aCoords_gcs= np.array(aCoords_gcs)
            nvertex = len(aCoords_gcs)
                            
            if nvertex == 2 :
                dLon_label = 0.5 * (aCoords_gcs[0][0] + aCoords_gcs[1][0] ) 
                dLat_label = 0.5 * (aCoords_gcs[0][1] + aCoords_gcs[1][1] ) 
            else:
                lIndex_mid = int(nvertex/2)    
                dLon_label = aCoords_gcs[lIndex_mid][0]
                dLat_label = aCoords_gcs[lIndex_mid][1]

            codes = np.full(nvertex, mpath.Path.LINETO, dtype=int )
            codes[0] = mpath.Path.MOVETO
            path = mpath.Path(aCoords_gcs[:,0:2], codes)            
            x, y = zip(*path.vertices)
            #caluculate line thickess
            iThickness = remap( dFlow_accumulation, dFlow_accumulation_min, dFlow_accumulation_max, iThickness_min, iThickness_max )
            if n_colors < 10:
                line, = ax.plot(x, y, color= colours[lID],linewidth=iThickness, transform=ccrs.PlateCarree())
            else:
                line, = ax.plot(x, y, color= 'black',linewidth=iThickness, transform=ccrs.PlateCarree())
            lID = lID + 1
            #add label 

    pDataset = pLayer = pFeature  = None    
   
    if aExtent_in is None:
        marginx  = (dLon_max - dLon_min) / 20
        marginy  = (dLat_max - dLat_min) / 20
        aExtent = [dLon_min - marginx , dLon_max + marginx , dLat_min -marginy , dLat_max + marginy]
    else:
        aExtent = aExtent_in
   
    ax.set_extent(aExtent)       
    gl = ax.gridlines( draw_labels=True,\
                  linewidth=0.2, color='gray', alpha=0.3, linestyle='--')
    gl.xlocator = mticker.MaxNLocator(5)
    gl.ylocator = mticker.MaxNLocator(5)
    gl.xlabel_style = {'size': 8, 'color': 'k', 'rotation':0, 'ha':'right'}
    gl.ylabel_style = {'size': 8, 'color': 'k', 'rotation':90,'weight': 'normal'}
    ax.set_title( sTitle.capitalize()) #, fontsize =  8*4)       
     
    
    #plot wbd
    #iFlag_plot_wbd =0 
    #if iFlag_plot_wbd ==1:
    #    # Extract first layer of features from shapefile using OGR
    #    sFilename_boundary = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_wgs.geojson'    
    #    pDataset = pDriver.Open(sFilename_boundary, gdal.GA_ReadOnly)
    #    pLayer = pDataset.GetLayer(0)   
    #    paths = []
    #
    #    for pFeature in pLayer:
    #        geom = pFeature.geometry()
    #        codes = []
    #        all_x = []
    #        all_y = []
    #        ng = geom.GetGeometryCount()
    #        for i in range(ng):
    #            # Read ring geometry and create path
    #            r = geom.GetGeometryRef(i)
    #            sGeometry_type = geom.GetGeometryName()                
    #            if(sGeometry_type == 'MULTIPOLYGON'):
    #                for geom_part in geom:
    #                    ng2 = geom_part.GetGeometryCount()
    #                    for k in range(ng2):
    #                        dummy= geom_part.GetGeometryRef(k)                        
    #                        lpoint =  dummy.GetPointCount()
    #                        if lpoint>0:
    #                            x = [dummy.GetX(j) for j in range(lpoint)]
    #                            y = [dummy.GetY(j) for j in range(lpoint)]
    #                            # skip boundary between individual rings
    #                            codes += [mpath.Path.MOVETO] + \
    #                                         (len(x)-1)*[mpath.Path.LINETO]
    #                            all_x += x
    #                            all_y += y
    #                            path = mpath.Path(np.column_stack((all_x,all_y)), codes)
    #                            paths.append(path)
    #                        else:
    #                            pass
    #            else:
    #                print('single')
    #    # Add paths as patches to axes
    #    for path in paths:
    #        patch = mpatches.PathPatch(path, \
    #                facecolor='none', edgecolor='red')
    #        ax.add_patch(patch)
    
    plt.savefig(sFilename_in, bbox_inches='tight')
    return
    
def _plot_mesh_with_flow_direction_and_river_network(self, sFilename_in, aExtent_in = None,  iFigwidth_in=None, iFigheight_in=None, pProjection_map_in = None):
    from matplotlib.backends.backend_pdf import PdfPages
    pPdf = PdfPages(sFilename_in)
    if iFigwidth_in is None:
        iFigwidth = iFigwidth_default

    if iFigheight_in is None:
        iFigheight = iFigheight_default 

    if pProjection_map_in is None:
        pProjection_map = pProjection_map_deafult
    else:
        pProjection_map = pProjection_map_in
    sTitle = 'Flow direction and river networks'
    dLat_min = 90
    dLat_max = -90
    dLon_min = 180
    dLon_max = -180  
    sFilename_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'hexwatershed.json' )
    iFlag_plot_mesh =1 
    if iFlag_plot_mesh ==1:
        with open(sFilename_json) as json_file:
            data = json.load(json_file)     
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]               
                avertex = pcell['vVertex']
                nvertex = len(avertex)
                aLocation= np.full( (nvertex, 2), 0.0, dtype=float )             
                for k in range(nvertex):
                    aLocation[k,0] = avertex[k]['dLongitude_degree']
                    aLocation[k,1] = avertex[k]['dLatitude_degree']
                    if aLocation[k,0] > dLon_max:
                        dLon_max = aLocation[k,0]
                    if aLocation[k,0] < dLon_min:
                        dLon_min = aLocation[k,0]
                    if aLocation[k,1] > dLat_max:
                        dLat_max = aLocation[k,1]
                    if aLocation[k,1] < dLat_min:
                        dLat_min = aLocation[k,1]

    pProjection_map = ccrs.Orthographic(central_longitude =  0.50*(dLon_max+dLon_min),  central_latitude = 0.50*(dLat_max+dLat_min), globe=None)
    fig = plt.figure( dpi=600)
    fig.set_figwidth( iFigwidth )
    fig.set_figheight( iFigheight )
    ax = fig.add_axes([0.1, 0.15, 0.75, 0.8] , projection=pProjection_map ) #request.crs
    ax.set_global()  

   
    sFilename_json = os.path.join(  self.sWorkspace_output_hexwatershed, 'hexwatershed.json' )
    iFlag_plot_mesh =1 
    if iFlag_plot_mesh ==1:
        with open(sFilename_json) as json_file:
            data = json.load(json_file)     
            ncell = len(data)
            lID =0 
            for i in range(ncell):
                pcell = data[i]               
                avertex = pcell['vVertex']
                nvertex = len(avertex)
                aLocation= np.full( (nvertex, 2), 0.0, dtype=float )     
                for k in range(nvertex):
                    aLocation[k,0] = avertex[k]['dLongitude_degree']
                    aLocation[k,1] = avertex[k]['dLatitude_degree'] 
                polygon = mpatches.Polygon(aLocation, closed=True, facecolor='none', alpha=0.8, linewidth=0.1,\
                    edgecolor='black',transform=ccrs.PlateCarree() )
                ax.add_patch(polygon)     
    pDriver = ogr.GetDriverByName('GeoJSON')
    sFilename_json = os.path.join(self.sWorkspace_output_hexwatershed, 'flow_direction.geojson')
    pDataset = pDriver.Open(sFilename_json, gdal.GA_ReadOnly)
    pLayer = pDataset.GetLayer(0)

    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    lID = 0
    n_colors = pLayer.GetFeatureCount()    
    colours = cm.rainbow(np.linspace(0, 1, n_colors))
    aFlow_accumulation =list()
    for pFeature in pLayer:       
        dFlow_accumulation = pFeature.GetField("fac")
        aFlow_accumulation.append(dFlow_accumulation)
    
    aFlow_accumulation = np.array(aFlow_accumulation)
    dFlow_accumulation_max = np.max(aFlow_accumulation)
    dFlow_accumulation_min = np.min(aFlow_accumulation)
    iThickness_max = 2.5
    iThickness_min = 0.3
    for pFeature in pLayer:
        pGeometry_in = pFeature.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        dFlow_accumulation = pFeature.GetField("fac")
        if sGeometry_type =='LINESTRING':
            dummy0 = loads( pGeometry_in.ExportToWkt() )
            aCoords_gcs = dummy0.coords
            aCoords_gcs= np.array(aCoords_gcs)
            nvertex = len(aCoords_gcs)
            
            for i in range(nvertex):
                dLon = aCoords_gcs[i][0]
                dLat = aCoords_gcs[i][1]              
                
            if nvertex == 2 :
                dLon_label = 0.5 * (aCoords_gcs[0][0] + aCoords_gcs[1][0] ) 
                dLat_label = 0.5 * (aCoords_gcs[0][1] + aCoords_gcs[1][1] ) 
            else:
                lIndex_mid = int(nvertex/2)    
                dLon_label = aCoords_gcs[lIndex_mid][0]
                dLat_label = aCoords_gcs[lIndex_mid][1]

            codes = np.full(nvertex, mpath.Path.LINETO, dtype=int )
            codes[0] = mpath.Path.MOVETO
            path = mpath.Path(aCoords_gcs[:,0:2], codes)            
            x, y = zip(*path.vertices)
            #caluculate line thickess
            iThickness = remap( dFlow_accumulation, dFlow_accumulation_min, dFlow_accumulation_max, iThickness_min, iThickness_max )
            if n_colors < 10:
                line, = ax.plot(x, y, color= colours[lID],linewidth=iThickness, transform=ccrs.PlateCarree())
            else:
                line, = ax.plot(x, y, color= 'black',linewidth=iThickness, transform=ccrs.PlateCarree())
            lID = lID + 1
            #add label 
                     
    pDataset = pLayer = pFeature  = None    
   
    #plot wbd
    #iFlag_plot_wbd =0 
    #if iFlag_plot_wbd ==1:
    #    # Extract first layer of features from shapefile using OGR
    #    sFilename_boundary = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_wgs.geojson'
    #    #pDriver = ogr.GetDriverByName('GeoJSON')
    #    pDataset = pDriver.Open(sFilename_boundary, gdal.GA_ReadOnly)
    #    pLayer = pDataset.GetLayer(0)
    #
    #    paths = []
    #    #pLayer.ResetReading()
    #    # Read all features in layer and store as paths
    #    for pFeature in pLayer:
    #        geom = pFeature.geometry()
    #        codes = []
    #        all_x = []
    #        all_y = []
    #        ng = geom.GetGeometryCount()
    #        for i in range(ng):
    #            # Read ring geometry and create path
    #            r = geom.GetGeometryRef(i)
    #            sGeometry_type = geom.GetGeometryName()                
    #            if(sGeometry_type == 'MULTIPOLYGON'):
    #                for geom_part in geom:
    #                    ng2 = geom_part.GetGeometryCount()
    #                    for k in range(ng2):
    #                        dummy= geom_part.GetGeometryRef(k)                        
    #                        lpoint =  dummy.GetPointCount()
    #                        if lpoint>0:
    #                            x = [dummy.GetX(j) for j in range(lpoint)]
    #                            y = [dummy.GetY(j) for j in range(lpoint)]
    #                            # skip boundary between individual rings
    #                            codes += [mpath.Path.MOVETO] + \
    #                                         (len(x)-1)*[mpath.Path.LINETO]
    #                            all_x += x
    #                            all_y += y
    #                            path = mpath.Path(np.column_stack((all_x,all_y)), codes)
    #                            paths.append(path)
    #                        else:
    #                            pass
    #            else:
    #                print('single')
#
    #    # Add paths as patches to axes
    #    for path in paths:
    #        patch = mpatches.PathPatch(path, \
    #                facecolor='none', edgecolor='red',linewidth=0.3,alpha=0.5)
    #        ax.add_patch(patch)
    
    #plot conceptual river network
    iFlag_plot_conceptual_flowline =1 
    if iFlag_plot_conceptual_flowline ==1:
        lID = 0 
        for iBasin in range(len(self.pPyFlowline.aBasin)):
            pBasin = self.pPyFlowline.aBasin[iBasin]
            sWorkspace_output_basin = pBasin.sWorkspace_output_basin
            #sFilename_json = os.path.join(self.sWorkspace_output_pyflowline, 'flowline_conceptual.geojson')
            sFilename_dummy = pBasin.sFilename_flowline_conceptual           
            sFilename_json = os.path.join(sWorkspace_output_basin, sFilename_dummy)
            pDriver = ogr.GetDriverByName('GeoJSON')
            pDataset = pDriver.Open(sFilename_json, gdal.GA_ReadOnly)
            pLayer = pDataset.GetLayer(0)
            n_colors = pLayer.GetFeatureCount()
            lID = 0 
            colours = cm.rainbow(np.linspace(0, 1, n_colors))
            for pFeature in pLayer:
                pGeometry_in = pFeature.GetGeometryRef()
                sGeometry_type = pGeometry_in.GetGeometryName()
                if sGeometry_type =='LINESTRING':
                    dummy0 = loads( pGeometry_in.ExportToWkt() )
                    aCoords_gcs = dummy0.coords
                    aCoords_gcs= np.array(aCoords_gcs)
                    nvertex = len(aCoords_gcs)   
                    codes = np.full(nvertex, mpath.Path.LINETO, dtype=int )
                    codes[0] = mpath.Path.MOVETO
                    path = mpath.Path(aCoords_gcs, codes)            
                    x, y = zip(*path.vertices)
                    line, = ax.plot(x, y, color= colours[lID], linewidth=0.5,alpha=0.8, transform=ccrs.PlateCarree())
                    lID = lID + 1
                pass
            pass

    if aExtent_in is None:
        marginx  = (dLon_max - dLon_min) / 20
        marginy  = (dLat_max - dLat_min) / 20
        aExtent = [dLon_min - marginx , dLon_max + marginx , dLat_min -marginy , dLat_max + marginy]
    else:
        aExtent = aExtent_in
        
    ax.set_extent(aExtent)   

    #sText = 'Case index: ' + "{:0d}".format( self.iCase_index  )
    #ax.text(0.05, 0.95, sText, \
    #verticalalignment='top', horizontalalignment='left',\
    #        transform=ax.transAxes, \
    #        color='black', fontsize=12)
    
    if self.sMesh_type != 'mpas':        
        sText = 'Mesh type: ' + self.sMesh_type.title()
        ax.text(0.05, 0.95, sText, \
        verticalalignment='top', horizontalalignment='left',\
            transform=ax.transAxes, \
            color='black', fontsize=12)
        sResolution =  'Resolution: ' + "{:0d}".format( int(self.dResolution_meter) ) + 'm'
        ax.text(0.05, 0.90, sResolution, \
            verticalalignment='top', horizontalalignment='left',\
            transform=ax.transAxes, \
            color='black', fontsize=12)
        if self.iFlag_stream_burning_topology ==1:
            sText = 'Stream topology: on'  
        else:
            sText = 'Stream topology: off'  

        ax.text(0.05, 0.85, sText, \
        verticalalignment='top', horizontalalignment='left',\
                transform=ax.transAxes, \
                color='black', fontsize=12)  

    else:
        sText = 'Mesh type: MPAS'
        ax.text(0.05, 0.95, sText, \
        verticalalignment='top', horizontalalignment='left',\
                transform=ax.transAxes, \
                color='black', fontsize=12)
        
        if self.iFlag_stream_burning_topology ==1:
            sText = 'Stream topology: on'  
        else:
            sText = 'Stream topology: off'  

        ax.text(0.05, 0.90, sText, \
        verticalalignment='top', horizontalalignment='left',\
                transform=ax.transAxes, \
                color='black', fontsize=12)  
        
        pass
    
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.3, linestyle='--')
    
    gl.xlocator = mticker.MaxNLocator(5)
    gl.ylocator = mticker.MaxNLocator(5)
    gl.xlabel_style = {'size': 10, 'color': 'k', 'rotation':0, 'ha':'right'}
    gl.ylabel_style = {'size': 10, 'color': 'k', 'rotation':90,'weight': 'normal'}
    ax.set_title( sTitle.capitalize()) #, fontsize =  8*4)       
    #plt.savefig(sFilename_in, bbox_inches='tight')
    #plt.savefig()
    pPdf.savefig()
    pPdf.close()


    return

