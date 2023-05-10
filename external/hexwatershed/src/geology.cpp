#include "geology.h"

/**
 * @brief calculate arc distance
 * 
 * @param dLongitude_degree0 
 * @param dLatitude_degree0 
 * @param dLongitude_degree1 
 * @param dLatitude_degree1 
 * @return float 
 */
float calculate_distance_based_on_lon_lat_degree(float dLongitude_degree0, 
float dLatitude_degree0, 
float dLongitude_degree1, 
float dLatitude_degree1)
{
    float dDistance = 0.0;
    float dLongitude_radian0, dLongitude_radian1, dLatitude_radian0, dLatitude_radian1;
    float dDelta_longitude_radian, dDelta_latitude_radian;
    float a, c, r;

    //convert decimal degrees to radians 
    
    dLongitude_radian0 = convert_degree_to_radian(dLongitude_degree0);
    dLatitude_radian0 = convert_degree_to_radian(dLatitude_degree0);

    dLongitude_radian1 = convert_degree_to_radian(dLongitude_degree1);
    dLatitude_radian1 = convert_degree_to_radian(dLatitude_degree1);

    //haversine formula 
    dDelta_longitude_radian = dLongitude_radian1 - dLongitude_radian0;
    dDelta_latitude_radian = dLatitude_radian1 - dLatitude_radian0;

    a = sin(dDelta_latitude_radian/2)* sin(dDelta_latitude_radian/2) + cos(dLatitude_radian0) * cos(dLatitude_radian1) * sin(dDelta_longitude_radian/2)* sin(dDelta_longitude_radian/2);
    c = 2 * asin(sqrt(a)); 
    

    r = dRadius_earth;

    dDistance = c * r;
    return dDistance;
}

/**
 * @brief calculate xyz location using lat/lon and elevation
 * 
 * @param dLongitude_radian 
 * @param dLatitude_radian 
 * @param dElevation 
 * @return std::array<float ,3> 
 */
std::array<float, 3>  calculate_location_based_on_lon_lat_radian(float dLongitude_radian, float dLatitude_radian, float dElevation)
{
    std::array<float, 3> aLocation;
    // see: http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html
    float f = 1.0/298.257223563 ; //# Flattening factor WGS84 Model
    float cosLat = cos(dLatitude_radian);
    float sinLat = sin(dLatitude_radian);
    float FF     = (1.0-f)*(1.0-f);
    float C      = 1/sqrt(cosLat*cosLat + FF * sinLat*sinLat);
    float S      = C * FF;

    float x = (dRadius_earth * C + dElevation)*cosLat * cos(dLongitude_radian);
    float y = (dRadius_earth * C + dElevation)*cosLat * sin(dLongitude_radian);
    float z = (dRadius_earth * S + dElevation)*sinLat;

    aLocation[0] = x;
    aLocation[1] = y;
    aLocation[2] = z;
    return aLocation;
}