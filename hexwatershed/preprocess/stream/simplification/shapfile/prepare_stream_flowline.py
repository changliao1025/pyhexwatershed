
import sys, os
import numpy as np
from osgeo import gdal, osr,ogr, gdalconst

from pyearth.system.define_global_variables import *

gdal.UseExceptions()



def check_stream_order(aDic, aPt_pair):
    iFlag = 0
    npair= len(aDic)
    iCount = 0
    x0=-2136505.847
    y0=2901799.686
    
    #normally, a point has to appear twice, so it is 2+2=4
    #on the edge, it showup only 1 + 2 =3
    for i in np.arange(0,2):
        x1 = aPt_pair[i][0]
        y1 = aPt_pair[i][1]
        #check outlet
        d = np.power(  (x1-x0), 2 ) + np.power(  (y1-y0), 2 )
        if(d < 0.0001):
            iCount = 10
            break

        for j in np.arange(0, npair):
            aPt_pair2 = aDic[j]
            for k in np.arange(0,2):
                x2 = aPt_pair2[k][0]
                y2 = aPt_pair2[k][1]

                a = np.power(  (x1-x2), 2 ) + np.power(  (y1-y2), 2 )

                if(a < 0.0001):
                    iCount = iCount + 1
                    pass


    if iCount < 6:
        iFlag = 1
    else:
        print(iCount)
        iFlag = 0

    return iFlag

def define_stream_segment_index(sFilename_in, sFilename_out):

    return


def define_stream_order():

    return

def remove_small_stream(sFilename_in, sFilename_out):

    sDriverName = "ESRI Shapefile"
    pDriver = ogr.GetDriverByName( sDriverName )


    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)

    pDataSource = pDriver.Open(sFilename_in, 0) # 0 means      read-only. 1 means writeable.

    

    # Check to see if shapefile is found.
    if pDataSource is None:
        print ('Could not open %s' % (sFilename_in))
    else:
        print ('Opened %s' % (sFilename_in))
        pLayer = pDataSource.GetLayer()
        pSpatailRef = pLayer.GetSpatialRef() 

        #output
        pSrs = pSpatailRef
        pDatasetOut = pDriver.CreateDataSource(sFilename_out)
        pLayerOut = pDatasetOut.CreateLayer('flowline2', pSrs, ogr.wkbLineString)
        # Add one attribute
        pLayerOut.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        pLayerDefn = pLayerOut.GetLayerDefn()
        pFeatureOut = ogr.Feature(pLayerDefn)
        lFeatureCount = pLayer.GetFeatureCount()
        print ( "Number of features in %s: %d" %  (os.path.basename(sFilename_in),lFeatureCount) )        
        pSpatailRef = pLayer.GetSpatialRef() 
        #aFeature=[]
        
        j = 0
        aDic =[]
        #first build the loop up table
        for pFeature in pLayer:            
            pGeometry = pFeature.GetGeometryRef()
            #print(pGeometry)
            npt = pGeometry.GetPointCount()
            #print(npt)           
            
            aPt_pair = [ pGeometry.GetPoint(0), pGeometry.GetPoint(npt-1)]
            aDic.append(aPt_pair)          
            pass

        #now check small
        i=1
        j =1
        for pFeature in pLayer:            
            pGeometry = pFeature.GetGeometryRef()
            #print(pGeometry)
            npt = pGeometry.GetPointCount()
            print(i, npt)           
            i=i+1
            
            #get length as well
            dLength = pGeometry.Length()
            aPt_pair = [ pGeometry.GetPoint(0), pGeometry.GetPoint(npt-1)]
            iFlag = check_stream_order(aDic, aPt_pair)
            if iFlag ==1 and dLength < 100000:
                
                    #remove this line
                print('removed')
                pass
            else:
                #save this geomery
                pFeatureOut.SetGeometry(pGeometry)
                pFeatureOut.SetField("id", j)
                pLayerOut.CreateFeature(pFeatureOut)
                j=j+1
                pass

                pass

            pass


     
        pDatasetOut = pLayerOut = pFeatureOut  = None      
    print("finished")
    return

def save_as_shapefile():
    return

if __name__ == '__main__':

    sWorkspace_data = '/people/liao313/data'

    sFilename_in = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_noloop_split.shp'
    sFilename_out = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_nonloop2.shp'

    #remove_stream_network_loops(sFilename_in, sFilename_out)

    #merge again

    #feature to line

    #remove small edge line

    sFilename_in = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_nonloop2_split_single.shp'
    sFilename_out = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_remove_small_line8.shp'
    #remove_small_stream(sFilename_in, sFilename_out)


    #merge and multiple part
    sFilename_in = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_remove_small_line_split.shp'
    sFilename_out = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_segment.shp'
    define_stream_segment_index(sFilename_in, sFilename_out)







    




