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

    nField_in = len(aVariable_json_in)

    nField_out = len(aVariable_geojson_out)
    if nField_in != nField_out:
        print("Error: the field number of input and output are not the same")
        return

    for i in range(nField_out):
        sVariable = aVariable_geojson_out[i].lower()
        iVariable_type = aVariable_type_out[i]
        if iVariable_type == 1: #integer
            pField = ogr.FieldDefn(sVariable, ogr.OFTInteger)
            pField.SetWidth(10)
        else: #float
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
        cell_dict = {int(pcell['lCellID']): pcell for pcell in data}
        lLineID = 0

        for pcell in data:
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start = float(pcell['dLongitude_center_degree'])
            y_start = float(pcell['dLatitude_center_degree'])

            for k in range(nField_out):
                iDataType = aVariable_type_out[k]
                if iDataType == 1:
                    dValue = int(pcell[aVariable_json_in[k]])
                else:
                    dValue = float(pcell[aVariable_json_in[k]])

            pcell2 = cell_dict.get(lCellID_downslope, None)
            if pcell2:
                x_end = float(pcell2['dLongitude_center_degree'])
                y_end = float(pcell2['dLatitude_center_degree'])

                #line = [x_start, y_start, x_end, y_end]
                #feature = {"lineid": lLineID, "geometry": line}

                pLine = ogr.Geometry(ogr.wkbLineString)
                pLine.AddPoint(x_start, y_start)
                pLine.AddPoint(x_end, y_end)
                pFeature.SetGeometry(pLine)
                pFeature.SetField("lineid", lLineID)

                for k in range(nField_out):                        
                    pFeature.SetField(aVariable_geojson_out[k].lower(), dValue)

                pLayer.CreateFeature(pFeature)
                lLineID = lLineID + 1       
               
                        
    #delete and write to dick                    
    pFac_field =None
    pLine = None
    pLayer = None 
    pFeature = None 
    pDataset  = None 
