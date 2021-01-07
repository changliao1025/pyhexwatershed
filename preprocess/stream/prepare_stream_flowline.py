
import sys, os
import numpy as np
from osgeo import gdal, osr,ogr, gdalconst


sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from pyes.system.define_global_variables import *

from pyes.gis.gdal.read.gdal_read_shapefile import gdal_read_shapefile

gdal.UseExceptions()

def search_duplicate_pair(aDic, aPt_pair):

    nPair = len(aDic)
    iFlag = 0 # not in the dic
    for i in np.arange(0, nPair):
        start = aDic[i][0]
        end = aDic[i][1]
        start_x = start[0]
        start_y = start[1]
        end_x = end[0]
        end_y = end[1]
        x1 = aPt_pair[0][0]
        y1 = aPt_pair[0][1]
        x2 = aPt_pair[1][0]
        y2 = aPt_pair[1][1]

        a = np.power(  (start_x - x1 ) ,2)  + np.power(  (start_y - y1 ) ,2) + np.power(  (end_x - x2 ) ,2)  + np.power(  (end_y - y2 ) ,2)
        #reverse
        b = np.power(  (start_x - x2 ) ,2)  + np.power(  (start_y - y2 ) ,2) + np.power(  (end_x - x1 ) ,2)  + np.power(  (end_y - y1 ) ,2)
        if a < 0.0001 or b < 0.0001:
            #we found one
            iFlag = 1
            break
        else:
            pass

    if iFlag == 0:
        #add it into the dic
        aDic.append(aPt_pair)

    return iFlag, aDic

def remove_stream_network_loops(sFilename_in, sFilename_out):

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
        pLayerOut = pDatasetOut.CreateLayer('flowline', pSrs, ogr.wkbLineString)
        # Add one attribute
        pLayerOut.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))

        pLayerDefn = pLayerOut.GetLayerDefn()
        pFeatureOut = ogr.Feature(pLayerDefn)


        lFeatureCount = pLayer.GetFeatureCount()
        print ( "Number of features in %s: %d" %  (os.path.basename(sFilename_in),lFeatureCount) )
        
        pSpatailRef = pLayer.GetSpatialRef() 

        #aFeature=[]

        aPt = np.full( (lFeatureCount,2) , None, dtype = object)
        j = 0
        aDic =[]
        for pFeature in pLayer:
            
            pGeometry = pFeature.GetGeometryRef()
            #print(pGeometry)
            npt = pGeometry.GetPointCount()
            print(npt)
            for i in range(0, npt):
                # GetPoint returns a tuple not a Geometry
                pt = pGeometry.GetPoint(i)
                #print(pt[0], pt[1])                
                #print (pGeometry.Centroid().ExportToWkt())

            aPt[j,0] = pGeometry.GetPoint(0)
            aPt[j,1] = pGeometry.GetPoint(npt-1)

            aPt_pair = [ pGeometry.GetPoint(0), pGeometry.GetPoint(npt-1)]
            iFlag, aDic = search_duplicate_pair(aDic, aPt_pair)
            j = j +1
            if(iFlag ==1):
                pass    
            else:
                #save this geomery
                pFeatureOut.SetGeometry(pGeometry)
                pFeatureOut.SetField("id", j)
                pLayerOut.CreateFeature(pFeatureOut)
                pass
            #aFeature.append(pGeometry)

            pass
        print(aPt)
        pDatasetOut = pLayerOut = pFeatureOut  = None      

    return

def define_stream_segment_index():


    return


def define_stream_order():

    return

def remove_small_stream():

    return

def save_as_shapefile():
    return

if __name__ == '__main__':

    sWorkspace_data = '/people/liao313/data'

    sFilename_in = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_split.shp'


    sFilename_out = sWorkspace_data + slash + '/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline_nonloop.shp'

    #remove_stream_network_loops(sFilename_in, sFilename_out)

    #merge again

    #feature to line

    




