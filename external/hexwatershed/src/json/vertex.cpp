#include "vertex.h"

namespace jsonmodel
{

  vertex::vertex()
  {
    lVertexIndex = 0;
    dx = -9999; //map projection
    dy = -9999; //map projection
    dz = -9999; //elevation of VTK
  }

  vertex::~vertex()
  {
  }

  /**
   * @brief overload the equal function
   * 
   * @param cVertex 
   * @return true 
   * @return false 
   */

  bool vertex::operator==(const vertex &cVertex)
  {
    float dDistance;
    dDistance = calculate_distance( cVertex );
    if ( dDistance < 0.001) //careful
    {
      return true;
    }
    else
    {
      return false;
    }
  }

  /**
   * @brief calculate the slope between two vertices
   * 
   * @param pVertex_in 
   * @return float 
   */

  float vertex::calculate_slope(vertex pVertex_in)
  {
    float dSlope = 0.0;
    float x1;
    float y1;
    float z1;
    float dElevation1;
    float dDistance;
    x1 = pVertex_in.dx;
    y1 = pVertex_in.dy;
    z1 = pVertex_in.dz;
    dElevation1 = pVertex_in.dElevation;
    dDistance=  calculate_distance(pVertex_in); 

    if (this->dx != x1)
    {
      dSlope = abs(this->dElevation - dElevation1) / dDistance;
    }
    else
    {
      /* code */
    }
    return dSlope;
  }
  float vertex::calculate_distance(vertex pVertex_in)
  {
    float dDistance = 0.0;
    float dLon0 = this->dLongitude_degree;
    float dLat0 = this->dLatitude_degree;
    float dLon1 = pVertex_in.dLongitude_degree;
    float dLat1 = pVertex_in.dLatitude_degree;

    dDistance = calculate_distance_based_on_lon_lat_degree(dLon0, dLat0, dLon1, dLat1);

    return dDistance;
  }

  int vertex::update_location()
  {
    int error_code =1;
    
    std::array<float, 3> aLocation = calculate_location_based_on_lon_lat_radian(dLongitude_radian, dLatitude_radian, dElevation);
    dx = aLocation[0];
    dy = aLocation[1];
    dz = aLocation[2];

    return error_code;
  }
} // namespace hexwatershed