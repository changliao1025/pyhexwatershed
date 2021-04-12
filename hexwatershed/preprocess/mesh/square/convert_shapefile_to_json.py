import os
#import json
from osgeo import ogr, osr, gdal, gdalconst
os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'
def convert_shapefile_to_json(sFilename_shapefile, sFilename_output):
    

    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)

    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_output)


    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
   
    pDataset_shapefile = pDriver_shapefile.Open(sFilename_shapefile, 0)
    pLayer_shapefile = pDataset_shapefile.GetLayer(0)
    pSrs = pLayer_shapefile.GetSpatialRef()
    #pSrs = osr.SpatialReference()  
    #pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    pLayerOut = pDataset.CreateLayer('flowline', pSrs, ogr.wkbMultiLineString)
    # Add one attribute
    pLayerOut.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayerOut.GetLayerDefn()
    pFeatureOut = ogr.Feature(pLayerDefn)

    lID = 0
    for feature in pLayer_shapefile:
        geom = feature.GetGeometryRef()
        pFeatureOut.SetGeometry(geom)
        pFeatureOut.SetField("id", lID)
        
        # Add new feature to output Layer
        pLayerOut.CreateFeature(pFeatureOut)        
        lID =  lID +1
    
    pDataset = pLayerOut = pFeatureOut  = None    

    return


    

if __name__ == '__main__':
    sFilename_shapefile = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/mesh_id/crb_flowline_remove_small_line_split.shp'

    sFilename_output = 'flowline.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'
    sFilename_output = os.path.join(sWorkspace_out, sFilename_output)
    
    convert_shapefile_to_json(sFilename_shapefile, sFilename_output)