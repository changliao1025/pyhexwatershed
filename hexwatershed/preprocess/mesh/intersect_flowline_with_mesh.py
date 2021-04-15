
import os
import json
from osgeo import ogr, osr
os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'


def intersect_flowline_with_mesh(sFilename_mesh, sFilename_flowline, sFilename_output):

    pDriver = ogr.GetDriverByName('GeoJSON')

    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)

    
    #geojson
    
   
    pDataset1 = pDriver.Open(sFilename_mesh, 0)
    pDataset2 = pDriver.Open(sFilename_flowline, 0)

    
 
    #mesh_geojson =  json.loads(sFilename_mesh)
    #flowline_geojson =   json.loads(sFilename_flowline)
    #mesh_polygon = ogr.CreateGeometryFromJson(mesh_geojson)
    #flowline = ogr.CreateGeometryFromJson(flowline_geojson)

    pLayer1 = pDataset1.GetLayer(0)
    pSpatialRef1 = pLayer1.GetSpatialRef()
    print( pSpatialRef1)
    pLayer2 = pDataset2.GetLayer(0)
    pSpatialRef2 = pLayer2.GetSpatialRef()
    
    print( pSpatialRef2)
    comparison = pSpatialRef1.IsSame(pSpatialRef2)
    if(comparison != 1):
        iFlag_transform =1
        transform = osr.CoordinateTransformation(pSpatialRef1, pSpatialRef2)
    else:
        iFlag_transform =0

    pDataset3 = pDriver.CreateDataSource(sFilename_output)

    pLayerOut = pDataset3.CreateLayer('flowline', pSpatialRef2, ogr.wkbMultiLineString)
    # Add one attribute
    pLayerOut.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayerOut.GetLayerDefn()
    pFeatureOut = ogr.Feature(pLayerDefn)

    
    lID = 0
    for pFeature1 in pLayer1:       
        pGeometry1 = pFeature1.GetGeometryRef()
        if (iFlag_transform ==1): #projections are different
            pGeometry1.Transform(transform)

        if (pGeometry1.IsValid()):
            pass
        else:
            print('Geometry issue')
        #print(pGeometry1.GetGeometryName())
        for pFeature2 in pLayer2:
            pGeometry2 = pFeature2.GetGeometryRef()
            if (pGeometry2.IsValid()):
                pass
            else:
                print('Geometry issue')
            #print(pGeometry2.GetGeometryName())
            
            iFlag_intersect = pGeometry2.Intersects( pGeometry1 )
            if( iFlag_intersect == True):
                pGeometry3 = pGeometry2.Intersection(pGeometry1) 
                #print('Found intersection')
                
                #print( pGeometry3.ExportToJson() )
                #print(pGeometry3.GetGeometryName())
                #print(lID)
                pFeatureOut.SetGeometry(pGeometry3)
                pFeatureOut.SetField("id", lID)

                # Add new feature to output Layer
                pLayerOut.CreateFeature(pFeatureOut)    
                lID = lID + 1

            else:
                pass


if __name__ == '__main__':
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'

  
    sFilename_flowline = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline.json'
    sFilename_output = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline_intersect_hexagon.json'

    intersect_flowline_with_mesh(sFilename_mesh, sFilename_flowline, sFilename_output)