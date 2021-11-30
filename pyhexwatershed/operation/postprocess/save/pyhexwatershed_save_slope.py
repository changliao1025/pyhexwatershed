import json
from osgeo import ogr, osr, gdal, gdalconst
from pyearth.system.define_global_variables import *
def pyhexwatershed_save_slope(oHexwatershed_in):

    sWorkspace_output_case = oHexwatershed_in.sWorkspace_output_case

    sFilename_json = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'hexwatershed.json'

    sFilename_shapefile = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'slope_between.shp'
    pDriver_shapefile = ogr.GetDriverByName('Esri Shapefile')
    pDataset = pDriver_shapefile.CreateDataSource(sFilename_shapefile)

   
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    pLayer = pDataset.CreateLayer('slpb', pSrs, geom_type=ogr.wkbPolygon)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    pLayer.CreateField(ogr.FieldDefn('idd', ogr.OFTInteger64)) #long type for high resolution
    pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
    pFac_field.SetWidth(20)
    pFac_field.SetPrecision(2)
    pLayer.CreateField(pFac_field) #long type for high resolution

    pSlp_field = ogr.FieldDefn('slp', ogr.OFTReal)
    pSlp_field.SetWidth(20)
    pSlp_field.SetPrecision(6)
    pLayer.CreateField(pSlp_field) #long type for high resolution
    
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)


    with open(sFilename_json) as json_file:
        data = json.load(json_file)  

        #print(type(data))

        ncell = len(data)
        lID =0 
        for i in range(ncell):
            pcell = data[i]
            lCellID = int(pcell['lCellID'])
            lCellID_downslope = int(pcell['lCellID_downslope'])
            x_start=float(pcell['dLongitude_center_degree'])
            y_start=float(pcell['dLatitude_center_degree'])
            dfac = float(pcell['DrainageArea'])
            dslp = float(pcell['dSlope_profile'])
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
            pFeature.SetField("idd", lCellID_downslope)
            pFeature.SetField("fac", dfac)
            pFeature.SetField("slp", dslp)
            pLayer.CreateFeature(pFeature)
            
            


        pDataset = pLayer = pFeature  = None      
    pass