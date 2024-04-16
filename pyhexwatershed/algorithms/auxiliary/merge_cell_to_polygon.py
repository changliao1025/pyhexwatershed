import os
import json
from osgeo import gdal, ogr, osr, gdalconst
from collections import defaultdict

def merge_cell_to_polygon(sFilename_in, sFilename_out, sVariable_in):
    #https://gis.stackexchange.com/questions/85028/dissolve-aggregate-polygons-with-ogr2ogr-or-gpc
    #ogr2ogr output.shp input.shp -dialect sqlite -sql "SELECT ST_Union(geometry), dissolve_field FROM input GROUP BY dissolve_field"
    pDataset_in = ogr.Open(sFilename_in)
    layer_name = pDataset_in.GetLayerByIndex(0).GetName()
    pKwargs = ' -f "Parquet" -dialect sqlite -sql "SELECT ST_Union(geometry), ' + sVariable_in + ' FROM ' + layer_name + ' GROUP BY ' + sVariable_in + '"'
    gdal.VectorTranslate(    sFilename_out,    sFilename_in,  options = pKwargs)

    return

def merge_cell_to_polygon_slow(sFilename_in, sFilename_out, sVariable_in, iVariable_type_in):

    pDriver_geojson = ogr.GetDriverByName('GeoJSON')
    pDriver_geojson = ogr.GetDriverByName('Parquet')

    if os.path.exists(sFilename_out):
        pDriver_geojson.DeleteDataSource(sFilename_out)

    pDataset_out = pDriver_geojson.CreateDataSource(sFilename_out)
    if pDataset_out is None:
        print('Dataset not created')
        return    
    
    pDataset_in = ogr.Open(sFilename_in)    
    # Get the first layer in the file
    pLayer_in = pDataset_in.GetLayer(0)   
    pLayerDefn_in = pLayer_in.GetLayerDefn()
    # Count the number of features (polygons)
    nFeature = pLayer_in.GetFeatureCount()
    # Get the spatial reference of the layer
    pSpatial_reference = pLayer_in.GetSpatialRef()
    wkt2 = pSpatial_reference.ExportToWkt()
    pLayer_out = pDataset_out.CreateLayer('layer', pSpatial_reference, geom_type=ogr.wkbPolygon)
    pGeometry_merge = ogr.Geometry(ogr.wkbPolygon)
    #copy layer definition
    pLayerDefn = pLayer_out.GetLayerDefn()             
    if iVariable_type_in == 1: #integer
        pField = ogr.FieldDefn(sVariable_in, ogr.OFTInteger)
        pField.SetWidth(10)
    else: #float
        pField = ogr.FieldDefn(sVariable_in, ogr.OFTReal)
        pField.SetWidth(20)
        pField.SetPrecision(8)
        pass
    pLayer_out.CreateField(pField)

    pLayerDefn = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn)

    features_by_attribute = defaultdict(list)
    for i in range(nFeature):
        pFeature_in = pLayer_in.GetFeature(i)
        pGeometry = pFeature_in.GetGeometryRef()            
        # Get the attribute value
        attribute_value = pFeature_in.GetField(sVariable_in)
        # Add the feature to the list of features for this attribute value
        features_by_attribute[attribute_value].append(pGeometry)

        # For each attribute value, merge the features and create a new feature in the output layer
    for attribute_value, features in features_by_attribute.items():
        pGeometry_merge = ogr.Geometry(ogr.wkbPolygon)
        for pGeometry in features:
            # Union the geometry of each feature with the merged polygon
            pGeometry_merge = pGeometry_merge.Union(pGeometry)

        # Create a new feature in the output layer
        pFeature_out = ogr.Feature(pLayer_out.GetLayerDefn())
        pFeature_out.SetGeometry(pGeometry_merge)
        pFeature_out.SetField(sVariable_in, attribute_value)
        pLayer_out.CreateFeature(pFeature_out)
    
    pDataset_out.Destroy()
    pDataset_in.Destroy()

    return



