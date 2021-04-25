import numpy as np
def check_same_point(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    a = (x1-x2) * (x1-x2)
    b= (y1-y2) * (y2-y2)
    c = np.sqrt(a+b)
    if( c < 0.0000001 ):
        return 1
    else:
        return 0