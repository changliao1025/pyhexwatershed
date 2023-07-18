import os
import json
from osgeo import gdal, ogr, osr, gdalconst

def export_json_to_geojson_polygon(sFilename_json_in, sFilename_geojson_out, aVariable_in):
    """
    export a hexwatershed json to geojson polygon

    Args:
        sFilename_json_in (_type_): _description_
        sFilename_geojson_out (_type_): _description_
        aVariable_in (_type_): _description_
    """
    
    #os.path.join(self.sWorkspace_output_hexwatershed ,   'elevation.geojson')
    if os.path.exists(sFilename_geojson_out):
        os.remove(sFilename_geojson_out)

    pDriver_geojson = ogr.GetDriverByName('GeoJSON')
    pDataset = pDriver_geojson.CreateDataSource(sFilename_geojson_out)           
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
    pLayer = pDataset.CreateLayer('hexwatershed', pSrs, geom_type=ogr.wkbPolygon)
    # Add one attribute
    
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution       
    pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
    pFac_field.SetWidth(20)
    pFac_field.SetPrecision(2)
    pLayer.CreateField(pFac_field) #long type for high resolution
    pSlp_field = ogr.FieldDefn('elev', ogr.OFTReal)
    pSlp_field.SetWidth(20)
    pSlp_field.SetPrecision(8)
    pLayer.CreateField(pSlp_field) #long type for high resolution
    pSlp_field = ogr.FieldDefn('elep', ogr.OFTReal)
    pSlp_field.SetWidth(20)
    pSlp_field.SetPrecision(8)
    pLayer.CreateField(pSlp_field) #long type for high resolution
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)
    with open(sFilename_json) as json_file:
        data = json.load(json_file)  
        ncell = len(data)
        lID = 0 
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start=float(pcell['dLongitude_center_degree'])
            y_start=float(pcell['dLatitude_center_degree'])
            dfac = float(pcell['DrainageArea'])
            dElev = float(pcell['Elevation'])
            dElep = float(pcell['Elevation_profile'])
            vVertex = pcell['vVertex']
            nvertex = len(vVertex)
            pPolygon = ogr.Geometry(ogr.wkbPolygon)
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for j in range(nvertex):
                x = vVertex[j]['dLongitude_degree']
                y = vVertex[j]['dLatitude_degree']
                ring.AddPoint(x, y)
            x = vVertex[0]['dLongitude_degree']
            y = vVertex[0]['dLatitude_degree']
            ring.AddPoint(x, y)
            pPolygon.AddGeometry(ring)
            pFeature.SetGeometry(pPolygon)
            pFeature.SetField("id", lCellID)                
            pFeature.SetField("fac", dfac)
            pFeature.SetField("elev", dElev)
            pFeature.SetField("elep", dElep)
            pLayer.CreateFeature(pFeature)
        pDataset = pLayer = pFeature  = None      
    pass   