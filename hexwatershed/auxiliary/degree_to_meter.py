import numpy as np
def degree_to_meter(dLatitude, dResolution_degree):
    dRadius = 6378.1 * 1000 #unit: m earth radius
    dRadius2 = dRadius * np.cos( dLatitude / 180.0 * np.pi)
    dResolution_meter = dResolution_degree / 360.0 * 2*np.pi * dRadius2

    return dResolution_meter