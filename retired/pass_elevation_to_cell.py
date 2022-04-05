
def pass_elevation_to_cell(aCell_elevation_in, aCell_intersect_in):

    ncell_elev = len(aCell_elevation_in)
    ncell_intersect = len(aCell_intersect_in)
    
    aCell_out = list()  

    for i in range(ncell_elev):
        pCell = aCell_elevation_in[i]
        lCellID = pCell.lCellID   

        for j in range(ncell_intersect):
            pCell_intersect = aCell_intersect_in[j]
            if lCellID == pCell_intersect.lCellID:
                #replace
                pCell.dLength_flowline = pCell_intersect.dLength_flowline
                aCell_out.append(pCell)
                break

    return aCell_out


