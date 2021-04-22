import os
import json
from osgeo import ogr, osr, gdal, gdalconst

def convert_shapefile_to_json(sFilename_shapefile_in, sFilename_json_out):
    """
    convert a shpefile to json format.
    This function should be used for stream flowline only.
    """

    if os.path.exists(sFilename_json_out): 
        #delete it if it exists
        os.remove(sFilename_json_out)

    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_json_out)


    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
   
    pDataset_shapefile = pDriver_shapefile.Open(sFilename_shapefile_in, gdal.GA_ReadOnly)
    pLayer_shapefile = pDataset_shapefile.GetLayer(0)
    pSpatialRef_in = pLayer_shapefile.GetSpatialRef()
    

    pLayerOut = pDataset.CreateLayer('flowline', pSpatialRef_in, ogr.wkbMultiLineString)
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
    sFilename_shapefile_in = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/mesh_id/crb_flowline_remove_small_line_split.shp'

    sFilename_json_out = 'flowline.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'
    sFilename_json_out = os.path.join(sWorkspace_out, sFilename_json_out)
    
    convert_shapefile_to_json(sFilename_shapefile_in, sFilename_json_out)