
def rebuild_cell_neighbor(aCell_elevation_in, aCell_in):
    '''
    update neighbor
    aCell_elevation_in: cells with valid elevation
    aCell_in: all cells
    '''
    ncell_elev = len(aCell_elevation_in)
    ncell_all = len(aCell_in)
    
    aCell_out = list()    
    aCellID  = list()  #cell that has elevation
    aCell_mid = list()

    for i in range(ncell_all):
        pCell = aCell_in[i]
        lCellID = pCell.lCellID   

        for j in range(ncell_elev):
            pCell_elevation = aCell_elevation_in[j]
            if lCellID == pCell_elevation.lCellID:
                aCellID.append(lCellID)
                #copy content
                pCell.nNeighbor = pCell_elevation.nNeighbor
                pCell.dElevation_mean = pCell_elevation.dElevation_mean
                pCell.dElevation_profile0 = pCell_elevation.dElevation_profile0 #for mpas
                pCell.aEdge = pCell_elevation.aEdge
                pCell.aNeighbor = pCell_elevation.aNeighbor
                pCell.aNeighbor_distance = pCell_elevation.aNeighbor_distance
                
                aCell_mid.append(pCell)
                break        
    
    ncell_mid = len(aCell_mid)
    
    for i in range(ncell_mid):
        pCell = aCell_mid[i]
        aNeighbor = pCell.aNeighbor
        nNeighbor = pCell.nNeighbor
        aNeighbor_land = list()
        nNeighbor_land = 0 
        aNeighbor_ocean = list()
        nNeighbor_ocean = 0 
        for j in range(nNeighbor):
            lNeighbor = int(aNeighbor[j])
            if lNeighbor in aCellID:
                nNeighbor_land = nNeighbor_land +1 
                aNeighbor_land.append(lNeighbor)
            else:
                #nNeighbor_ocean = nNeighbor_ocean +1 
                #aNeighbor_ocean.append(lNeighbor)
                pass
                
        pCell.nNeighbor_land= len(aNeighbor_land)
        pCell.aNeighbor_land = aNeighbor_land
        #pCell.nNeighbor_ocean= len(aNeighbor_ocean)
        #pCell.aNeighbor_ocean = aNeighbor_ocean
  
        if pCell.nNeighbor_ocean> 0:
            pCell.iFlag_coast = 1
        else:
            pCell.iFlag_coast = 0

        aCell_out.append(pCell)
    
    return aCell_out
