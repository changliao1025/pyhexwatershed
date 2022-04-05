import matplotlib.pyplot as plt
import numpy as np

import cartopy
import cartopy.crs as ccrs
import matplotlib.ticker as mticker


from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
def main():

    x1 = -70
    y1 = 4
    x2 = -150
    y2 = 68
    
    plt.figure(figsize=(6,20))
    ax2 = plt.subplot(3, 1, 2, projection=ccrs.Orthographic(-110, 25))
    ax2.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax2.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')

    ax2.set_global()

    gl = ax2.gridlines( 
                  linewidth=0.5, color='gray', alpha=1, linestyle='--')
  
    #gl.xlines = True

    aLongitude = np.arange(-180,180, 2.0)
    aLatitude = np.arange(-90, 90, 2.0)
    gl.xlocator = mticker.FixedLocator(aLongitude)
    gl.ylocator = mticker.FixedLocator(aLatitude)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    #plt.show()

#1
    ax1 = plt.subplot(3, 1, 3, projection=ccrs.Orthographic(x1,y1))
    ax1.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax1.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
    ax1.set_global() 
    gl = ax1.gridlines(color='red', xlocs= aLongitude,\
        ylocs=aLatitude, linewidth = 1.5)
    gl.xlocator = mticker.FixedLocator(aLongitude)
    gl.ylocator = mticker.FixedLocator(aLatitude)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
    ax1.set_extent([x1-2.5, x1+2.5, y1-2.5, y1+2.5], crs=ccrs.PlateCarree())


#3
    ax3 = plt.subplot(3, 1, 1, projection=ccrs.Orthographic(x2,y2))
    ax3.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax3.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
    ax3.set_global() 
    gl = ax3.gridlines(color='red', xlocs= aLongitude,\
        ylocs=aLatitude, linewidth = 1.5)
    gl.xlocator = mticker.FixedLocator(aLongitude)
    gl.ylocator = mticker.FixedLocator(aLatitude)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
   
    gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
    ax3.set_extent([x2-2.5, x2+2.5, y2-2.5, y2+2.5], crs=ccrs.PlateCarree())


    #plt.show()
    sFilename_png = 'spatial_distortion.png'
    plt.savefig(sFilename_png)#, bbox_inches = 'tight')

    print('finished')


if __name__ == '__main__':
    main()