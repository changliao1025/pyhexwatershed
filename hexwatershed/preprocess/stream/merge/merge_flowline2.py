import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np
import shapely
from shapely.geometry import Point, LineString
from shapely.ops import split
from shapely.wkt import loads

from hexwatershed.preprocess.stream.check_same_point  import check_same_point
from hexwatershed.preprocess.stream.find_vertex_in_list  import find_vertex_in_list
lID = 0
def merge_flowline2(sFilename_flowline_in,sFilename_confluence_in, sFilename_out):
    if  os.path.exists(sFilename_flowline_in) and os.path.exists(sFilename_confluence_in): 
        pass
    else: 
        print('The input file does not exist')
        return
        
    if os.path.exists(sFilename_out): 
        #delete it if it exists
        os.remove(sFilename_out)

    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset_out = pDriver.CreateDataSource(sFilename_out)
    pDataset_in1 = pDriver.Open(sFilename_flowline_in, gdal.GA_ReadOnly)
    pLayer_in1 = pDataset_in1.GetLayer(0)
    pSpatialRef_in = pLayer_in1.GetSpatialRef()    

    lOutlet = 0

    #we have to go reversely
    iFeature_current= lOutlet

    pFeature_in1 = pLayer_in1.GetFeature(iFeature_current)

    pGeometry_in1 = pFeature_in1.GetGeometryRef()
    npt = pGeometry_in1.GetPointCount()
    pt_outlet_start = pGeometry_in1.GetPoint(0)
    pt_outlet_end = pGeometry_in1.GetPoint(npt-1)

    pDataset_in2 = pDriver.Open(sFilename_confluence_in, gdal.GA_ReadOnly)
    pLayer_in2 = pDataset_in2.GetLayer(0)

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)
    nfeature1 = pLayer_in1.GetFeatureCount()
    nfeature2 = pLayer_in2.GetFeatureCount()
    
    aVertex_head=[]
    aVertex_middle=[]
    aVertex_confluence=[]
    for i in range(0, nfeature2):   
        pFeature_in2 = pLayer_in2.GetFeature(i)
        pGeometry_in2 = pFeature_in2.GetGeometryRef()
        pt_start = pGeometry_in2.GetPoint(0)
        isconf = pFeature_in2.GetField('isconf')
        #print(isconf)
        if isconf >= 3:
            aVertex_confluence.append(pt_start)
        else:
            if isconf ==1:
                aVertex_head.append(pt_start)
            else:
                if isconf ==2:
                    aVertex_middle.append(pt_start)


    global lID
    lID=0
    
            
    def merge_flowline_reach(i, pt1, pt2):
        global lID
        pFeature_in1 = pLayer_in1.GetFeature(i)
        pGeometry_in1 = pFeature_in1.GetGeometryRef()
        line = loads( pGeometry_in1.ExportToWkt() )
        pt_current = pt1
        #while pt_current not in aVertex_confluence and pt_current not in aVertex_head:
        while (find_vertex_in_list(aVertex_confluence, pt_current) ==-1) \
            and (find_vertex_in_list(aVertex_head, pt_current)==-1):
            
            for j in range(0, nfeature1):      
                pFeature_in2 = pLayer_in1.GetFeature(j)
                pGeometry_in2 = pFeature_in2.GetGeometryRef()
                npoint = pGeometry_in2.GetPointCount()        
                pt_start = pGeometry_in2.GetPoint(0)
                pt_end = pGeometry_in2.GetPoint(npoint-1)

                line_coords = list(line.coords)

                if check_same_point(pt_end, pt_current)==1:#find_vertex_in_list(aVertex_middle, pt_start) !=-1 and 
                    #print(j)
                    #this is the upstream
                    new_line = loads( pGeometry_in2.ExportToWkt() )
                    new_line_coords = list(new_line.coords)
                    

                    pt_current = pt_start
                    
                    #inlines = shapely.geometry.MultiLineString(     [LineString(new_point_coords), LineString(l_coords )] )

                    #newcoords = [list(i.coords) for i in inlines]
                    npoint_down = len(line_coords)
                    for x in range(1, npoint_down):
                        new_line_coords.append( line_coords[x] )

                    #line = LineString(new_point_coords[0:len(new_point_coords)]) 
                    line = shapely.geometry.LineString([i for i in new_line_coords])

                    break
                else:

                    pass

        #save 
        pGeometry_out = ogr.CreateGeometryFromWkb(line.wkb)

        pFeature_out.SetGeometry(pGeometry_out)
        pFeature_out.SetField("id", lID)
        pLayer_out.CreateFeature(pFeature_out) 
        print(lID)
        lID = lID +1        
        #go to next 
        if find_vertex_in_list(aVertex_head, pt_current) !=-1: #pt_current in aVertex_head:
            pass
        else:
            #it must be confluence
            for j in range(0, nfeature1):      
                pFeature_in2 = pLayer_in1.GetFeature(j)
                pGeometry_in2 = pFeature_in2.GetGeometryRef()
                npoint = pGeometry_in2.GetPointCount()        
                pt_start = pGeometry_in2.GetPoint(0)
                pt_end = pGeometry_in2.GetPoint(npoint-1)
                if check_same_point(pt_end, pt_current)==1:
                    merge_flowline_reach(j, pt_start, pt_end)
                    pass


    
    merge_flowline_reach(iFeature_current, pt_outlet_start, pt_outlet_end)   


    
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    

    return 
