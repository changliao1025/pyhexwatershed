import os, sys
import json
import numpy as np
from osgeo import gdal, ogr, osr, gdalconst
from pyearth.gis.gdal.gdal_function import obtain_raster_metadata
from pyearth.gis.gdal.gdal_function import reproject_coordinates
from pyearth.gis.gdal.world2Pixel import world2Pixel

def assign_elevation_to_cell(iMesh_type, aCell_in, sFilename_dem_in, sFilename_shapefile_out, sWorkspace_simulation_case):
    if os.path.exists(sFilename_shapefile_out): 
        #delete it if it exists
        os.remove(sFilename_shapefile_out)
    
    aCell_out=list()

    ncell = len(aCell_in)
    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    pDriver_memory = gdal.GetDriverByName('MEM')

    #sFilename_shapefile_cut = sWorkspace_simulation_case + '/tmp_polygon.shp'
    sFilename_shapefile_cut = "/vsimem/tmp_polygon.shp"
    
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
    pDataset_elevation = gdal.Open(sFilename_dem_in, gdal.GA_ReadOnly)

    dPixelWidth, dOriginX, dOriginY, \
        nrow, ncolumn, pSpatialRef_target, pProjection, pGeotransform = obtain_raster_metadata(sFilename_dem_in)

    transform = osr.CoordinateTransformation(pSrs, pSpatialRef_target) 
    
    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    #pDriver_json = ogr.GetDriverByName('GeoJSON')
    pDataset_out = pDriver_shapefile.CreateDataSource(sFilename_shapefile_out)
    
    #get raster extent 
    dX_left=dOriginX
    dX_right = dOriginX + ncolumn * dPixelWidth
    dY_top = dOriginY
    dY_bot = dOriginY - nrow * dPixelWidth
    if iMesh_type ==4:
        #iFlag_transform=1        
        pLayer2 = pDataset_out.CreateLayer('cell', pSpatialRef_target, ogr.wkbPolygon)
        pLayer2.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64))
        pLayer2.CreateField(ogr.FieldDefn('elev', ogr.OFTReal))
        pLayerDefn = pLayer2.GetLayerDefn()
        pFeature2 = ogr.Feature(pLayerDefn)
        for i in range(1, ncell+1):
            pCell=  aCell_in[i-1]
            lCellID = pCell.lCellID
            dLon_center = pCell.dLon_center
            dLat_center = pCell.dLat_center
            nVertex = pCell.nVertex

            ring = ogr.Geometry(ogr.wkbLinearRing)
            for j in range(nVertex):
                
                x1 = pCell.aVertex[j].dLongitude
                y1 = pCell.aVertex[j].dLatitude

                x1,y1 = reproject_coordinates(x1,y1,pSrs,pSpatialRef_target)
                ring.AddPoint(x1, y1)                
                pass        
            x1 = pCell.aVertex[0].dLongitude
            y1 = pCell.aVertex[0].dLatitude
            x1,y1 = reproject_coordinates(x1,y1,pSrs,pSpatialRef_target)    
            ring.AddPoint(x1, y1)        

            pPolygon = ogr.Geometry(ogr.wkbPolygon)
            
            pPolygon.AddGeometry(ring)
            #pPolygon.AssignSpatialReference(pSrs)
            if os.path.exists(sFilename_shapefile_cut):   
                os.remove(sFilename_shapefile_cut)
            pDataset3 = pDriver_shapefile.CreateDataSource(sFilename_shapefile_cut)
            pLayerOut = pDataset3.CreateLayer('cell', pSpatialRef_target, ogr.wkbPolygon)    
            pLayerDefn = pLayerOut.GetLayerDefn()
            pFeatureOut = ogr.Feature(pLayerDefn)
            pFeatureOut.SetGeometry(pPolygon)  
            pLayerOut.CreateFeature(pFeatureOut)    
            pDataset3.FlushCache()

            #if iFlag_transform ==1: #projections are different
            #    pPolygon.Transform(transform)
            minX, maxX, minY, maxY = pPolygon.GetEnvelope()
            #ulX, ulY = world2Pixel(pGeotransform, minX, maxY)
            #lrX, lrY = world2Pixel(pGeotransform, maxX, minY)
            #iBeginRow = 0
            #iBeginCol = 0
            iNewWidth = int( (maxX - minX) / abs(dPixelWidth)  )
            iNewHeigh = int( (maxY - minY) / abs(dPixelWidth) )
            newGeoTransform = (minX, dPixelWidth, 0,    maxY, 0, -dPixelWidth)  
            
            if minX > dX_right or maxX < dX_left or minY > dY_top or maxY < dY_bot:
                #print(lCellID)
                continue
            else:         
                pDataset_clip = pDriver_memory.Create('', iNewWidth, iNewHeigh, 1, gdalconst.GDT_Float32)
                pDataset_clip.SetGeoTransform( newGeoTransform )
                pDataset_clip.SetProjection( pProjection)   
                pWrapOption = gdal.WarpOptions( cropToCutline=True,cutlineDSName = sFilename_shapefile_cut , \
                        width=iNewWidth,   \
                            height=iNewHeigh,      \
                                dstSRS=pProjection , format = 'MEM' )
                pDataset_clip = gdal.Warp('',pDataset_elevation, options=pWrapOption)
                pBand = pDataset_clip.GetRasterBand( 1 )
                dMissing_value = pBand.GetNoDataValue()
                aData_out = pBand.ReadAsArray(0,0,iNewWidth, iNewHeigh)

                aElevation = aData_out[np.where(aData_out !=dMissing_value)]                

                if(len(aElevation) >0 and np.mean(aElevation)!=-9999):
                    pFeature2.SetGeometry(pPolygon)
                    pFeature2.SetField("id", lCellID)
                    dElevation =  float(np.mean(aElevation) )  
                    pFeature2.SetField("elev",  dElevation )
                    pLayer2.CreateFeature(pFeature2)    
                    pCell.dElevation =    dElevation  
                    pCell.dz = dElevation  
                    aCell_out.append(pCell)
                else:
                    pFeature2.SetField("elev", -9999.0)

    pDataset_out.FlushCache()
    
        
    return aCell_out
