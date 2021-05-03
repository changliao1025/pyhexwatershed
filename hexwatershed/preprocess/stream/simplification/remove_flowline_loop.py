import sys, os
import numpy as np
from osgeo import gdal, osr, ogr, gdalconst

from hexwatershed.preprocess.stream.simplification.add_unique_line import  add_unique_line

def remove_flowline_loop(sFilename_flowline_in, sFilename_flowline_out):

    if  os.path.exists(sFilename_flowline_in): 
        pass
    else:
        print('The input file does not exist')
        return

    if os.path.exists(sFilename_flowline_out): 
        #delete it if it exists
        os.remove(sFilename_flowline_out)

    sDriverName = "GeoJSON"
    pDriver = ogr.GetDriverByName( sDriverName )


    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)

    pDataset_in = pDriver.Open(sFilename_flowline_in, gdal.GA_ReadOnly) 

    # Check to see if shapefile is found.
    if pDataset_in is None:
        print ('Could not open %s' % (sFilename_flowline_in))
    else:
        print ('Opened %s' % (sFilename_flowline_in))
        pLayer_in = pDataset_in.GetLayer()
        pSpatailRef_in = pLayer_in.GetSpatialRef() 

        #output
        pSpatailRef_out = pSpatailRef_in
        pDataset_out = pDriver.CreateDataSource(sFilename_flowline_out)
        pLayer_out = pDataset_out.CreateLayer('flowline', pSpatailRef_out, ogr.wkbLineString)
        # Add one attribute
        pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        pLayerDefn = pLayer_out.GetLayerDefn()
        pFeatureOut = ogr.Feature(pLayerDefn)
        lFeatureCount = pLayer_in.GetFeatureCount()
        print ( "Number of features in %s: %d" %  (os.path.basename(sFilename_flowline_in),lFeatureCount) )    
        
        j = 0
        aLine =[]
        for pFeature_in in pLayer_in:            
            pGeometry_in = pFeature_in.GetGeometryRef()
     
            npt = pGeometry_in.GetPointCount()         

            aPt_pair = [ pGeometry_in.GetPoint(0), pGeometry_in.GetPoint(npt-1)]

            iFlag, aLine = add_unique_line(aLine, aPt_pair)

            

            if(iFlag ==1):
                pass    
            else:           
                pFeatureOut.SetGeometry(pGeometry_in)
                pFeatureOut.SetField("id", j)
                pLayer_out.CreateFeature(pFeatureOut)
                j = j + 1
                pass
            

            pass
     
        pDataset_out = pLayer_out = pFeatureOut  = None      

    return