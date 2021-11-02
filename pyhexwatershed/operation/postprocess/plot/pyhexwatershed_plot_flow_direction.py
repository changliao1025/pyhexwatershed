import json
from osgeo import ogr, osr, gdal, gdalconst
from pyearth.system.define_global_variables import *
def pyhexwatershed_plot_flow_direction(oHexwatershed_in):

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

        nedge = len(data)
        lID =0 
        for i in range(nedge):
            pedge = data[i]
            lCellID = int(pedge['lCellID'])
            lCellID_downslope = int(pedge['lCellID_downslope'])
            x_start=float(pedge['dLon_center'])
            y_start=float(pedge['dLat_center'])
            dfac = float(pedge['DrainageArea'])
            for j in range(nedge):
                pedge2 = data[j]
                lCellID2 = int(pedge2['lCellID'])
                if lCellID2 == lCellID_downslope:
                    x_end=float(pedge2['dLon_center'])
                    y_end=float(pedge2['dLat_center'])

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