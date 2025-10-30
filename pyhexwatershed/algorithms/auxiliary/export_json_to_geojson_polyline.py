import os
import json
from osgeo import ogr, osr
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor,as_completed

def export_json_to_geojson_polyline(sFilename_json_in,
                                    sFilename_geojson_out,
                                    aVariable_json_in = None,
                                    aVariable_geojson_out= None,
                                    aVariable_type_out= None):
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
    #pLayer = pDataset.CreateLayer('stream', pSrs, ogr.wkbLineString)
    pLayer = pDataset.CreateLayer('stream', pSrs, geom_type=ogr.wkbLineString)

    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('lineid', ogr.OFTInteger64)) #long type for high resolution

    if aVariable_json_in is not None:
        nField_in = len(aVariable_json_in)
    else:
        nField_in = 0

    if aVariable_geojson_out is not None:
        nField_out = len(aVariable_geojson_out)
    else:
        nField_out = 0

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
        lLineID = 1 #change to start from 1

        for pcell in data:
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start = float(pcell['dLongitude_center_degree'])
            y_start = float(pcell['dLatitude_center_degree'])

            aValue  =list()
            for k in range(nField_out):
                iDataType = aVariable_type_out[k]
                if iDataType == 1:
                    dValue = int(pcell[aVariable_json_in[k]])
                else:
                    dValue = float(pcell[aVariable_json_in[k]])

                aValue.append(dValue)

            pcell2 = cell_dict.get(lCellID_downslope, None)
            if pcell2:
                x_end = float(pcell2['dLongitude_center_degree'])
                y_end = float(pcell2['dLatitude_center_degree'])

                #line = [x_start, y_start, x_end, y_end]
                #feature = {"lineid": lLineID, "geometry": line}

                pLine = ogr.Geometry(ogr.wkbLineString)
                pLine.AddPoint(x_start, y_start) #AddPoint_2D
                pLine.AddPoint(x_end, y_end)
                pFeature.SetGeometry(pLine)
                pFeature.SetField("lineid", lLineID)

                for k in range(nField_out):
                    pFeature.SetField(aVariable_geojson_out[k].lower(), aValue[k])

                pLayer.CreateFeature(pFeature)
                lLineID = lLineID + 1


    #delete and write to dick
    pFac_field =None
    pLine = None
    pLayer = None
    pFeature = None
    pDataset  = None

def process_line(index, pcell, cell_dict, aVariable_json_in, aVariable_geojson_out, aVariable_type_out):
    lCellID = int(pcell['lCellID'])
    lCellID_downslope = int(pcell['lCellID_downslope'])
    x_start = float(pcell['dLongitude_center_degree'])
    y_start = float(pcell['dLatitude_center_degree'])

    aValue = []
    for k in range(len(aVariable_geojson_out)):
        iDataType = aVariable_type_out[k]
        if iDataType == 1:
            dValue = int(pcell[aVariable_json_in[k]])
        else:
            dValue = float(pcell[aVariable_json_in[k]])
        aValue.append(dValue)

    pcell2 = cell_dict.get(lCellID_downslope, None)
    if pcell2:
        x_end = float(pcell2['dLongitude_center_degree'])
        y_end = float(pcell2['dLatitude_center_degree'])

        line_data = {
            'geometry': f"LINESTRING ({x_start} {y_start}, {x_end} {y_end})",
            'lineid': index + 1,
            'fields': {aVariable_geojson_out[k].lower(): aValue[k] for k in range(len(aVariable_geojson_out))}
        }

        return line_data
    return None

def export_json_to_geojson_polyline_parallel(sFilename_json_in,
                                    sFilename_geojson_out,
                                    aVariable_json_in=None,
                                    aVariable_geojson_out=None,
                                    aVariable_type_out=None):
    """
    Convert a hexwatershed JSON into a GeoJSON polyline.

    Args:
        sFilename_json_in (str): Input JSON filename.
        sFilename_geojson_out (str): Output GeoJSON filename.
        aVariable_json_in (list): List of input variable names.
        aVariable_geojson_out (list): List of output variable names.
        aVariable_type_out (list): List of output variable types (1 for integer, 2 for float).
    """

    if os.path.exists(sFilename_geojson_out):
        os.remove(sFilename_geojson_out)

    pDriver_geojson = ogr.GetDriverByName('GeoJSON')
    pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson_out)
    pSrs = osr.SpatialReference()
    pSrs.ImportFromEPSG(4326)  # WGS84 lat/lon
    pLayer = pDataset.CreateLayer('stream', pSrs, geom_type=ogr.wkbLineString)

    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('lineid', ogr.OFTInteger64))  # long type for high resolution

    if aVariable_json_in is not None:
        nField_in = len(aVariable_json_in)
    else:
        nField_in = 0

    if aVariable_geojson_out is not None:
        nField_out = len(aVariable_geojson_out)
    else:
        nField_out = 0

    if nField_in != nField_out:
        print("Error: the field number of input and output are not the same")
        return

    for i in range(nField_out):
        sVariable = aVariable_geojson_out[i].lower()
        iVariable_type = aVariable_type_out[i]
        if iVariable_type == 1:  # integer
            pField = ogr.FieldDefn(sVariable, ogr.OFTInteger)
            pField.SetWidth(10)
        else:  # float
            pField = ogr.FieldDefn(sVariable, ogr.OFTReal)
            pField.SetWidth(20)
            pField.SetPrecision(8)

        pLayer.CreateField(pField)  # long type for high resolution

    pLayerDefn = pLayer.GetLayerDefn()

    with open(sFilename_json_in) as json_file:
        data = json.load(json_file)
        ncell = len(data)
        cell_dict = {int(pcell['lCellID']): pcell for pcell in data}

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_line, i, data[i], cell_dict, aVariable_json_in, aVariable_geojson_out, aVariable_type_out): i for i in range(ncell)}
            results = [None] * ncell
            for future in as_completed(futures):
                index = futures[future]
                line_data = future.result()
                if line_data:
                    results[index] = line_data

            for line_data in results:
                if line_data:
                    pLine = ogr.CreateGeometryFromWkt(line_data['geometry'])
                    pFeature = ogr.Feature(pLayer.GetLayerDefn())
                    pFeature.SetGeometry(pLine)
                    pFeature.SetField("lineid", line_data['lineid'])
                    for attr_name, attr_value in line_data['fields'].items():
                        pFeature.SetField(attr_name, attr_value)

                    pLayer.CreateFeature(pFeature)
                    pFeature = None

    pDataset.FlushCache()
    pDataset = pLayer = None