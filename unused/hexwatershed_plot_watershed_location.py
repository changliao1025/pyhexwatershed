import platform
import os
import sys
from copy import copy
from pathlib import Path
import cartopy.crs as ccrs
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import numpy as np
from numpy  import array
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from shutil import copyfile
from osgeo import gdal, osr
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.geoaxes import GeoAxes
import matplotlib.ticker as mtick
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader
from cartopy.feature  import ShapelyFeature
from shapely.geometry import LineString
import matplotlib.patches as mpatches
import shapely.geometry as sgeom
import geoplot as gplt

sPlatform_os = platform.system()
sRegion = 'tinpan'

if sPlatform_os == 'Windows':  #windows
    slash = '\\'
    sWorkspace_code = 'C:' + slash + 'workspace'
    sWorkspace_scratch = 'D:'
    sFilename_config = sRegion + '_windows.txt'
else:  #linux or unix
    slash = '/'
    home = str(Path.home())
    sWorkspace_code = home + slash + 'workspace'
    if (sPlatform_os == 'Linux'):
        sWorkspace_scratch = slash + 'pic' + slash + 'scratch' + slash + 'liao313'
        sFilename_config = sRegion + '_linux.txt'
    else:
        if (sPlatform_os == 'Darwin'):
            sWorkspace_scratch = slash + 'Volumes' + slash + 'mac'
            sFilename_config = sRegion + '_mac.txt'
        else:
            exit
sExtension_envi = '.dat'
sExtension_header = '.hdr'
sExtension_txt = '.txt'
missing_value = -9999.0

sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string
from gis.gdal.gdal_read_tiff import gdal_read_tiff
from gis.gdal.gdal_read_envi import gdal_read_envi
from gis.gdal.gdal_read_shapefile import gdal_read_shapefile
from gis.cartopy.cartopy_define_projection import cartopy_define_projection
from toolbox.color.choose_n_color import choose_n_color

sWorkspace_data = '/Users/liao313/data/'
sWorkspace_project = sWorkspace_data + slash + 'hexwatershed'
sWorkspace_out = '/Users/liao313/tmp/03model/hexwatershed'

sFilename_dem = sWorkspace_project + slash + 'tinpan' + slash + 'raster' + slash \
    + 'dem.tif'
#sWorkspace_project = sWorkspace_data + slash + 'eco3d'
#sFilename_dem = sWorkspace_project + slash + 'raster' + slash + 'dem' + slash + 'huc819040507' + slash     + 'dem.dat'

sFilename_shapefile = sWorkspace_project + slash + 'tinpan' + slash + 'vector' + slash + 'hexgrid100.shp'
sFilename_shapefile ='/Users/liao313/tmp/03model/hexwatershed/tinpan/output/case5/stream_segment_merge_polyline.shp'

sFilename_png  = sWorkspace_project + slash + 'tinpan' + slash + 'vector' + slash + 'stream.png'

if not os.path.isfile(sFilename_dem): 
    print("File is missing")
    exit()

dummy = gdal_read_tiff(sFilename_dem)
aDem= dummy[0] #np.flip(dummy[0],0)
ncolumn = dummy[4]
nrow = dummy[5]
aDem.shape = (nrow, ncolumn)
pSpatialRef = dummy[6]
print(pSpatialRef)

x1 = dummy[2]
x2= dummy[2] + dummy[1] * ncolumn
y1 = dummy[3]
y2 = dummy[3] - dummy[1] * nrow
aImage_extent = [x1,x2, y2, y1]
pProjection_dem = cartopy_define_projection(pSpatialRef)

#plot matrix using matplotlib
aMask = np.where(  aDem == missing_value )
aMask2 = np.where(  aDem != missing_value )
aDem[aMask] = np.nan
max_value = np.nanmax(aDem[aMask2])
min_value = np.nanmin(aDem[aMask2])
#plot
fig = plt.figure(figsize=(12,9),  dpi=150 )
pColormap_dem = plt.get_cmap('rainbow') 
pColormap_stream  = plt.get_cmap('viridis') 
pProjection_gcs = ccrs.PlateCarree()

iBase_projection = 1
if iBase_projection == 1: # use data projection

    [lon_left ,lat_top] = pProjection_gcs.transform_point( x1, y1 , src_crs=pProjection_dem)
    [lon_right,lat_bot] = pProjection_gcs.transform_point( x2, y2 , src_crs=pProjection_dem)
else:
    
    lon_left = x1 
    lon_right = x2 
    lat_bot = y1 
    lat_top = y2 

pProjection_map = pProjection_dem

axes_class = (GeoAxes,
          dict(map_projection=pProjection_map))
axgr = AxesGrid(fig, 111, axes_class=axes_class,
      nrows_ncols=(1,1),
      axes_pad=0.6,
      cbar_location='right',
      cbar_mode='single',
      cbar_pad=0.2,
      cbar_size='1.5%',
      label_mode='')  # note the empty label_mode

aMap_extent=(lon_left,lon_right, lat_bot, lat_top)


pShapeReader = shpreader.Reader(sFilename_shapefile)
dummy= gdal_read_shapefile(sFilename_shapefile)

pProjection_stream = cartopy_define_projection(dummy[1])
nsegment = dummy[2]

aColor = choose_n_color(nsegment, pColormap_stream)
 
pGeometry = pShapeReader.geometries()
aShapeFeature = ShapelyFeature(pGeometry, pProjection_stream, facecolor='none', edgecolor=aColor, linewidth=0.5 , label = 'sLabel')
        
for i, ax in enumerate(axgr):
    #ax.coastlines()
    ax.axis('on')
    ax.set_extent(aMap_extent, crs=pProjection_gcs)
    #ax.set_extent(aImage_extent, crs=pProjection_dem)
    
    ax.tick_params(labeltop=True, labelright=True) 
    
    #ax.add_feature(cfeature.OCEAN, zorder=0)
    #ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    #ax.add_feature(cfeature.COASTLINE)
    #ax.set_global()
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.10)
    ax.set_xlim(x1,x2)
    ax.set_ylim(y2,y1)

    #convert project to longitude/latitude
    dummy1 = (lon_right - lon_left) / 5
    dummy2 = (lat_top - lat_bot) / 5 
    a = np.linspace(lon_left - dummy1, lon_right+ dummy1, 7)
    b = np.linspace(lat_bot - dummy2, lat_top+ dummy2, 7)
    
    gl = ax.gridlines(xlocs=a, ylocs=b, linestyle='--')
    
    lon_formatter = LongitudeFormatter(zero_direction_label=True,number_format = '.1f')
    lat_formatter = LatitudeFormatter(number_format = '.1f')
    
    #ax.xaxis.set_major_formatter(lon_formatter)
    #ax.yaxis.set_major_formatter(lat_formatter)

    gl.xlocator = mticker.FixedLocator(a)
    gl.ylocator = mticker.FixedLocator(b)
    gl.xformatter = lon_formatter
    gl.yformatter = lat_formatter
    #gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
    #ax.set_xticks(a, crs=pProjection_gcs)
    #ax.set_yticks(b ,crs=pProjection_gcs)
    #gl.xlabels_top = True
   
    #gl.ylabels_left = True
    #gl.ylabels_right=True
    #gl.xlines = True
    # Customize the grid    
    #plt.show()    
    
    #ax.set_xlabel('Longitude')
    #ax.set_ylabel('Latitude')
    
    ax.set_title('Tin Pan', loc='center')
    
    implot = ax.imshow(aDem, extent = aImage_extent, origin='upper',cmap=pColormap_dem , \
       vmax = max_value, vmin = min_value , transform = pProjection_dem) 

    
    ax.add_feature(aShapeFeature)
    #i = 0
    #aLabel = np.full(nsegment, None, dtype= object)
    #for pLineString in pShapeReader.records():
    #    sLabel = pLineString.attributes['segm']
    #    aLabel[i] = sLabel
    #    ax.add_geometries(pLineString.geometry, pProjection_stream , facecolor='none' 
    #            , edgecolor= aColor[i],linewidth=0.2, zorder = 4) 
    #    i = i+1
        
    #ax.legend(aLabel)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=lon_left, borderaxespad=0.)
    #handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles, labels)
    #plot shapefile
    #cb_label_loc = np.arange( min_value , (max_value+1) , ((max_value-min_value)/5) , dtype= float)
    #cb_label = cb_label_loc
    #cb = plt.colorbar(implot, cax = axgr.cbar_axes[0], extend = 'both')        
    #tick_locs  = cb_label_loc
    #tick_labels = ['{:.0f}'.format(x) for x in cb_label]
    #cb.locator     = ticker.FixedLocator(tick_locs)
    #cb.formatter   = ticker.FixedFormatter(tick_labels)       
    #cb.update_ticks()
    plt.show()
    plt.savefig(sFilename_png, bbox_inches = 'tight')
    print(sFilename_png)
    print('ok')

                        