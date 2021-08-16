def rebuild_cell_neighbor(aCell_elevation_in, aCell_in):
    #update neighbor
    aCell_out=list()
    ncell = len(aCell_in)
    aCellID  = list()

    ncell2=len(aCell_elevation_in)

    aCell_mid = list()

    for i in range(ncell):
        pCell = aCell_in[i]
        lCellID = pCell.lCellID   

        for j in range(ncell2):
            pCell2 = aCell_elevation_in[j]
            if lCellID == pCell2.lCellID   :
                aCellID.append(lCellID)
                pCell.aNeighbor = pCell2.aNeighbor
                pCell.nNeighbor = pCell2.nNeighbor
                pCell.dElevation = pCell2.dElevation
                aCell_mid.append(pCell)
                break        
    
    ncell3 = len(aCell_mid)
    aCell_out = list()
    for i in range(ncell3):
        pCell = aCell_mid[i]
        aNeighbor = pCell.aNeighbor
        nNeighbor = pCell.nNeighbor
        aNeighbor_new = list()
        nNeighbor_new = 0 
        for j in range(nNeighbor):
            lNeighbor = int(aNeighbor[j])
            if lNeighbor in aCellID:
                nNeighbor_new = nNeighbor_new +1 
                aNeighbor_new.append(lNeighbor)
                
        pCell.nNeighbor= len(aNeighbor_new)
        pCell.aNeighbor = aNeighbor_new
        aCell_out.append(pCell)
    
    return aCell_out
