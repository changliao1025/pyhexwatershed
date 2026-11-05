import json
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from osgeo import gdal, gdalconst, ogr, osr


def export_json_to_geojson_polygon(
    sFilename_json_in,
    sFilename_geojson_out,
    aVariable_json_in=None,
    aVariable_geojson_out=None,
    aVariable_type_out=None,
):
    """Export a hexwatershed json to geojson polygon."""

    if os.path.exists(sFilename_geojson_out):
        os.remove(sFilename_geojson_out)

    pDriver_geojson = ogr.GetDriverByName("GeoJSON")
    pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson_out)
    pSrs = osr.SpatialReference()
    pSrs.ImportFromEPSG(4326)  # WGS84 lat/lon
    pLayer = pDataset.CreateLayer("hexwatershed", pSrs, geom_type=ogr.wkbPolygon)
    # Add basic attributes cellid
    pLayer.CreateField(ogr.FieldDefn("cellid", ogr.OFTInteger64))  # long type for high resolution

    nField_in = len(aVariable_json_in) if aVariable_json_in is not None else 0
    nField_out = len(aVariable_geojson_out) if aVariable_geojson_out is not None else 0
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
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell["lCellID"])
            vVertex = pcell["vVertex"]
            nvertex = len(vVertex)
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for j in range(nvertex):
                x = vVertex[j]["dLongitude_degree"]
                y = vVertex[j]["dLatitude_degree"]
                ring.AddPoint(x, y)

            x = vVertex[0]["dLongitude_degree"]
            y = vVertex[0]["dLatitude_degree"]
            ring.AddPoint(x, y)
            ring.CloseRings()
            pPolygon = ogr.Geometry(ogr.wkbPolygon)
            pPolygon.AddGeometry(ring)

            if pPolygon.GetCoordinateDimension() == 3:
                pPolygon.FlattenTo2D()

            pFeature = ogr.Feature(pLayerDefn)
            pFeature.SetGeometry(pPolygon)
            pFeature.SetField("cellid", lCellID)
            for k in range(nField_out):
                iDataType = aVariable_type_out[k]
                if iDataType == 1:
                    dValue = int(pcell[aVariable_json_in[k]])
                else:
                    dValue = float(pcell[aVariable_json_in[k]])

                pFeature.SetField(aVariable_geojson_out[k], dValue)

            pLayer.CreateFeature(pFeature)
            pFeature = None

        pDataset.FlushCache()
        pDataset = pLayer = None


def process_cell(index, pcell, aVariable_json_in, aVariable_geojson_out, aVariable_type_out):
    lCellID = int(pcell["lCellID"])
    vVertex = pcell["vVertex"]
    nvertex = len(vVertex)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for j in range(nvertex):
        vertex = vVertex[j]
        ring.AddPoint_2D(vertex["dLongitude_degree"], vertex["dLatitude_degree"])

    # Close the ring
    ring.CloseRings()
    pPolygon = ogr.Geometry(ogr.wkbPolygon)
    pPolygon.AddGeometry(ring)

    # Ensure geometry is 2D
    if pPolygon.GetCoordinateDimension() == 3:
        pPolygon.FlattenTo2D()

    feature_data = {
        "geometry": pPolygon.ExportToWkt(),
        "cellid": lCellID,
        "fields": {},
    }

    if aVariable_geojson_out is not None:
        for k in range(len(aVariable_geojson_out)):
            field_name = aVariable_geojson_out[k]
            field_value = pcell[aVariable_json_in[k]]
            if aVariable_type_out[k] == 1:
                feature_data["fields"][field_name] = int(field_value)
            else:
                feature_data["fields"][field_name] = float(field_value)

    return index, feature_data


def export_json_to_geojson_polygon_parallel(
    sFilename_json_in,
    sFilename_geojson_out,
    aVariable_json_in,
    aVariable_geojson_out,
    aVariable_type_out,
):
    """Export a hexwatershed JSON to GeoJSON polygon in parallel."""

    if os.path.exists(sFilename_geojson_out):
        os.remove(sFilename_geojson_out)

    pDriver_geojson = ogr.GetDriverByName("GeoJSON")
    pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson_out)
    pSrs = osr.SpatialReference()
    pSrs.ImportFromEPSG(4326)  # WGS84 lat/lon
    pLayer = pDataset.CreateLayer("hexwatershed", pSrs, geom_type=ogr.wkbPolygon)

    # Add basic attributes cellid
    pLayer.CreateField(ogr.FieldDefn("cellid", ogr.OFTInteger64))  # long type for high resolution

    nField_in = len(aVariable_json_in) if aVariable_json_in is not None else 0
    nField_out = len(aVariable_geojson_out) if aVariable_geojson_out is not None else 0
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

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    process_cell, i, data[i], aVariable_json_in, aVariable_geojson_out, aVariable_type_out
                ): i
                for i in range(ncell)
            }
            results = [None] * ncell
            for future in as_completed(futures):
                index, feature_data = future.result()
                results[index] = feature_data

            for feature_data in results:
                pPolygon = ogr.CreateGeometryFromWkt(feature_data["geometry"])

                if pPolygon.GetCoordinateDimension() == 3:
                    pPolygon.FlattenTo2D()

                pFeature = ogr.Feature(pLayerDefn)
                pFeature.SetGeometry(pPolygon)
                pFeature.SetField("cellid", feature_data["cellid"])
                if aVariable_geojson_out is not None:
                    for k in range(len(aVariable_geojson_out)):
                        field_name = aVariable_geojson_out[k]
                        field_value = feature_data["fields"][field_name]
                        pFeature.SetField(field_name, field_value)
                pLayer.CreateFeature(pFeature)
                pFeature = None

        pDataset.FlushCache()
        pDataset = pLayer = None
