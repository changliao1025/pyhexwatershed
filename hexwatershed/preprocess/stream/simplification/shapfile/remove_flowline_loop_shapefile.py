def remove_flowline_loops(sFilename_in, sFilename_out):

    sDriverName = "ESRI Shapefile"
    pDriver = ogr.GetDriverByName( sDriverName )


    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)

    pDataSource = pDriver.Open(sFilename_in, 0) # 0 means      read-only. 1 means writeable.

    

    # Check to see if shapefile is found.
    if pDataSource is None:
        print ('Could not open %s' % (sFilename_in))
    else:
        print ('Opened %s' % (sFilename_in))
        pLayer = pDataSource.GetLayer()
        pSpatailRef = pLayer.GetSpatialRef() 

        #output
        pSrs = pSpatailRef
        pDatasetOut = pDriver.CreateDataSource(sFilename_out)
        pLayerOut = pDatasetOut.CreateLayer('flowline', pSrs, ogr.wkbLineString)
        # Add one attribute
        pLayerOut.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        pLayerDefn = pLayerOut.GetLayerDefn()
        pFeatureOut = ogr.Feature(pLayerDefn)
        lFeatureCount = pLayer.GetFeatureCount()
        print ( "Number of features in %s: %d" %  (os.path.basename(sFilename_in),lFeatureCount) )        
        pSpatailRef = pLayer.GetSpatialRef() 
        #aFeature=[]
        
        j = 0
        aDic =[]
        for pFeature in pLayer:            
            pGeometry = pFeature.GetGeometryRef()
            #print(pGeometry)
            npt = pGeometry.GetPointCount()
            print(npt)
            for i in range(0, npt):
                # GetPoint returns a tuple not a Geometry
                pt = pGeometry.GetPoint(i)
                #print(pt[0], pt[1])                
                #print (pGeometry.Centroid().ExportToWkt())

           

            aPt_pair = [ pGeometry.GetPoint(0), pGeometry.GetPoint(npt-1)]
            iFlag, aDic = search_duplicate_pair(aDic, aPt_pair)
            j = j + 1
            if(iFlag ==1):
                pass    
            else:
                #save this geomery
                pFeatureOut.SetGeometry(pGeometry)
                pFeatureOut.SetField("id", j)
                pLayerOut.CreateFeature(pFeatureOut)
                pass
            #aFeature.append(pGeometry)

            pass
     
        pDatasetOut = pLayerOut = pFeatureOut  = None      

    return