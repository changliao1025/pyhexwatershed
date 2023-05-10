#pragma once
#include <cmath>

#include "global.h"
#include "conversion.h"

using namespace std;

float calculate_distance_based_on_lon_lat_degree(float dLongitude_degree0, 
float dLatitude_degree0, 
float dLongitude_degree1, 
float dLatitude_degree1);

std::array<float ,3>  calculate_location_based_on_lon_lat_radian(float dLatitude_radian,  
float dLongitude_radian,
float dElevation);