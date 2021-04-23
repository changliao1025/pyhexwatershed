import numpy as np
def add_unique_point(aPoint, pPoint):

    nPair = len(aPoint)
    iFlag = 0 # not in the dictionary
    for i in np.arange(0, nPair):
        x0 = aPoint[i][0]
        y0 = aPoint[i][1]
        x1 = pPoint[0]
        y1 = pPoint[1]       

        a = np.power(  (x0 - x1 ) ,2)  + np.power(  (y0 - y1 ) ,2)        
        if a < 0.0001 :
            #we found one repeating segment
            iFlag = 1
            break
        else:
            pass

    if iFlag == 0:
        #add it into the dic
        aPoint.append(pPoint)

    return iFlag, aPoint

