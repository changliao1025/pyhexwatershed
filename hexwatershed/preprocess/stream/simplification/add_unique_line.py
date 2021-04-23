import numpy as np
def add_unique_line(aLine, aPt_pair):

    nPair = len(aLine)
    iFlag = 0 # not in the dictionary
    for i in np.arange(0, nPair):
        start = aLine[i][0]
        end = aLine[i][1]
        start_x = start[0]
        start_y = start[1]
        end_x = end[0]
        end_y = end[1]
        x1 = aPt_pair[0][0]
        y1 = aPt_pair[0][1]
        x2 = aPt_pair[1][0]
        y2 = aPt_pair[1][1]

        a = np.power(  (start_x - x1 ) ,2)  + np.power(  (start_y - y1 ) ,2) + np.power(  (end_x - x2 ) ,2)  + np.power(  (end_y - y2 ) ,2)
        #reverse
        b = np.power(  (start_x - x2 ) ,2)  + np.power(  (start_y - y2 ) ,2) + np.power(  (end_x - x1 ) ,2)  + np.power(  (end_y - y1 ) ,2)
        if a < 0.0001 or b < 0.0001:
            #we found one repeating segment
            iFlag = 1
            break
        else:
            pass

    if iFlag == 0:
        #add it into the dic
        aLine.append(aPt_pair)

    return iFlag, aLine

