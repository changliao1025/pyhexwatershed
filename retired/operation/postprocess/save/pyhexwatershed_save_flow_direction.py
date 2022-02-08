import json
from osgeo import ogr, osr, gdal, gdalconst
from pyearth.system.define_global_variables import *
def pyhexwatershed_save_flow_direction(oHexwatershed_in):

    sWorkspace_output_case = oHexwatershed_in.sWorkspace_output_case

    sFilename_json = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'hexwatershed.json'

    sFilename_shapefile = sWorkspace_output_case + slash + 'hexwatershed' + slash + 'flow_direction.shp'
    pDriver_shapefile = ogr.GetDriverByName('Esri Shapefile')
    pDataset = pDriver_shapefile.CreateDataSource(sFilename_shapefile)

   
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    pLayer = pDataset.CreateLayer('flowdir', pSrs, ogr.wkbLineString)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    pFac_field = ogr.FieldDefn('fac', ogr.OFTReal)
    pFac_field.SetWidth(20)
    pFac_field.SetPrecision(2)
    pLayer.CreateField(pFac_field) #long type for high resolution
    
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
                    pFeature.SetField("id", lID)
                    pFeature.SetField("fac", dfac)

                    pLayer.CreateFeature(pFeature)
                    lID =lID +1
                    break


        pDataset = pLayer = pFeature  = None      
    pass