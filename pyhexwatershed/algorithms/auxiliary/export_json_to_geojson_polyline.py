import os
import json
from osgeo import gdal, ogr, osr, gdalconst
def export_json_to_geojson_polyline(sFilename_json_in, 
                                    sFilename_geojson_out,
                                    aVariable_json_in,
                                    aVariable_geojson_out,
                                    aVariable_type_out):
    """
    Convert a hexwatershed json into a geojson polyline

    Args:
        sFilename_json_in (_type_): _description_
        sFilename_geojson_out (_type_): _description_
    """
    
    if os.path.exists(sFilename_geojson_out):
        os.remove(sFilename_geojson_out)
        
    pDriver_geojson = ogr.GetDriverByName('GeoJSON')
    pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson_out)    
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)  #WGS84 lat/lon
    pLayer = pDataset.CreateLayer('stream', pSrs, ogr.wkbLineString)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('lineid', ogr.OFTInteger64)) #long type for high resolution

    nField = len(aVariable_geojson_out)

    for i in range(nField):
        sVariable = aVariable_geojson_out[i].lower()
        iVariable_type = aVariable_type_out[i]
        if iVariable_type == 1:
            pField = ogr.FieldDefn(sVariable, ogr.OFTInteger)
            pField.SetWidth(10)
        else:
            pField = ogr.FieldDefn(sVariable, ogr.OFTReal)
            pField.SetWidth(20)
            pField.SetPrecision(8)
            pass

        pLayer.CreateField(pField) #long type for high resolution 


    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)
    with open(sFilename_json_in) as json_file:
        data = json.load(json_file)  
        ncell = len(data)
        lLineID =0 
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell['lCellID']) #this is the cell id
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start=float(pcell['dLongitude_center_degree'])
            y_start=float(pcell['dLatitude_center_degree'])
            iSegment = int(pcell['iSegment'])                           
            dfac = float(pcell['DrainageArea'])
            for j in range(ncell):
                pcell2 = data[j]
                lCellID2 = int(pcell2['lCellID'])
                if lCellID2 == lCellID_downslope:
                    x_end=float(pcell2['dLongitude_center_degree'])
                    y_end=float(pcell2['dLatitude_center_degree'])
                    pLine = ogr.Geometry(ogr.wkbLineString)
                    pLine.AddPoint(x_start, y_start)
                    pLine.AddPoint(x_end, y_end)
                    pFeature.SetGeometry(pLine)
                    pFeature.SetField("lineid", lLineID)
                    pFeature.SetField("drainage", dfac)
                    pFeature.SetField("isegment", iSegment)
                    pLayer.CreateFeature(pFeature)
                    lLineID = lLineID + 1
                    break           
                        
    #delete and write to dick                    
    pFac_field =None
    pLine = None
    pLayer = None 
    pFeature = None 
    pDataset  = None 
