/**
 * @file domain.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the realization of the domain class
 * @version 0.1
 * @date 2019-08-02
 *
 * @copyright Copyright (c) 2019
 *
 */
#include "./compset.h"

namespace hexwatershed
{

  /**
   * initialize the model
   * @return
   */
  int compset::compset_initialize_model()
  {
    int error_code = 1;   

    //get informaiton from the domain pass variable
    long lVertexIndex = 0;
    long lLocalID=0;
    long lCellIndex_outlet;
    long ncell = this->aCell.size();
  
    std::vector<cell>::iterator iIterator1;
    std::vector<vertex>::iterator iIterator2;
    
    vVertex_active.clear();
    lVertexIndex =0;
    for (iIterator1 = aCell.begin(); iIterator1 != aCell.end(); ++iIterator1)
      {
        hexagon pHexagon;
        pHexagon.lCellIndex = lLocalID;
        pHexagon.lCellID = (*iIterator1).lCellID;
        pHexagon.dElevation_mean = (*iIterator1).dElevation_mean;
        pHexagon.dElevation_raw = (*iIterator1).dElevation_raw;
        pHexagon.dElevation_profile0 = (*iIterator1).dElevation_profile0;
     
        pHexagon.dLength_stream_burned = (*iIterator1).dLength_flowline;
        pHexagon.dArea = (*iIterator1).dArea;
        pHexagon.dAccumulation = pHexagon.dArea;
        pHexagon.dLongitude_center_degree=(*iIterator1).dLongitude_center_degree;
        pHexagon.dLatitude_center_degree=(*iIterator1).dLatitude_center_degree;
        pHexagon.dLongitude_center_radian = convert_degree_to_radian(pHexagon.dLongitude_center_degree);
        pHexagon.dLatitude_center_radian = convert_degree_to_radian(pHexagon.dLatitude_center_degree);
        pHexagon.vNeighbor = (*iIterator1).aNeighbor;
        pHexagon.vNeighbor_distance = (*iIterator1).aNeighbor_distance;
        pHexagon.vNeighbor_land = (*iIterator1).aNeighbor_land;
        //pHexagon.vNeighbor_ocean = (*iIterator1).aNeighbor_ocean;
        //edge and vertex coordinates are not yet used
        pHexagon.nNeighbor = (*iIterator1).nNeighbor;
        pHexagon.nNeighbor_land = (*iIterator1).nNeighbor_land;
        //pHexagon.nNeighbor_ocean = (*iIterator1).nNeighbor_ocean;
        pHexagon.nEdge = (*iIterator1).nEdge;
        pHexagon.nVertex = (*iIterator1).nVertex;

        for (int i=0; i< pHexagon.nVertex; i++)
        {
          vertex pVertex = (*iIterator1).vVertex.at(i);
          //pVertex.dLongitude_degree = (*iIterator1).aLongitude_vertex.at(i);
          //pVertex.dLatitude_degree = (*iIterator1).aLatitude_vertex.at(i);
          pVertex.dElevation = pHexagon.dElevation_mean; //this needs to be updated          
          iIterator2 = std::find(vVertex_active.begin(), vVertex_active.end(), pVertex);
            if (iIterator2 != vVertex_active.end())
            {
              //it is already indexed
              pVertex.lVertexIndex = (*iIterator2).lVertexIndex;
            }
            else
            {
              pVertex.lVertexIndex = lVertexIndex;
              lVertexIndex = lVertexIndex + 1;
              vVertex_active.push_back(pVertex);
            }      

          pHexagon.vVertex.push_back(pVertex);

        }

        pHexagon.iStream_segment_burned = (*iIterator1).iStream_segment_burned;
        pHexagon.iStream_order_burned = (*iIterator1).iStream_order_burned;
        pHexagon.lCellID_downstream_burned = (*iIterator1).lCellID_downstream_burned;

        if (pHexagon.iStream_segment_burned > 0) //check it starts with 1
          {
            pHexagon.iFlag_stream_burned = 1;
          }

        pHexagon.calculate_effective_resolution();
        //we require the 
        if (pHexagon.dLength_stream_burned  < pHexagon.dLength_stream_conceptual)
        {
          pHexagon.dLength_stream_burned  = pHexagon.dLength_stream_conceptual;
        }


        vCell_active.push_back(pHexagon);
        lLocalID = lLocalID +1 ;
      }

    std::cout << "Finished initialization!" << std::endl;
    std::flush(std::cout);
    return error_code;
  }

  int compset::compset_assign_stream_burning_cell()
  {
    int error_code = 1;
    int iFlag_stream_burning_topology= cParameter.iFlag_stream_burning_topology;
    int iMeshStrseg;
    int iMeshStrord;
    int iFlag_merged;
    int iFlag_active;
    long lCellID;
    std::vector<flowline>::iterator iIterator;
    std::vector<hexagon>::iterator iIterator2;

    if (iFlag_stream_burning_topology == 0)
      {
        for (iIterator = vFlowline.begin(); iIterator != vFlowline.end(); iIterator++)
          {

            lCellID = (*iIterator).lCellID;
            //find in vector
            //at this time, we do not yet know whether a stream is within watershed or not
            //a mesh may have multiple nhd within
            for (iIterator2 = vCell_active.begin(); iIterator2 != vCell_active.end(); iIterator2++)
              {
                if ((*iIterator2).lCellID == lCellID)
                  {
                    (*iIterator2).iFlag_stream_burned = 1;
                  }
              }
          }
      }
    else
      {

        for (iIterator = vFlowline.begin(); iIterator != vFlowline.end(); iIterator++)
          {
            iFlag_active = (*iIterator).iFlag_active;
            lCellID = (*iIterator).lCellID;
            iMeshStrseg = (*iIterator).iStream_segment;
            iMeshStrord = (*iIterator).iStream_order;
            if (iFlag_active == 1)
              {
                //find in vector
                //at this time, we do not yet know whether a stream is within watershed or not
                //a mesh may have multiple nhd within
                for (iIterator2 = vCell_active.begin(); iIterator2 != vCell_active.end(); iIterator2++)
                  {
                    if ((*iIterator2).lCellID == lCellID)
                      {
                        (*iIterator2).iFlag_stream_burned = 1;
                        //assign the stream order
                        if (iMeshStrord > (*iIterator2).iStream_order_burned)
                          {
                            //this code will be run at least once because default value is negative
                            (*iIterator2).iStream_order_burned = iMeshStrord;
                            //because the stream order is changed, the stream segment must be updated as well
                            (*iIterator2).iStream_segment_burned = iMeshStrseg;
                          }
                        else
                          {
                            /* code */
                          }
                      }
                  }
              }
            else
              {
                //simplified
              }
          }
      }

    return error_code;
  }

  long compset::compset_find_index_by_cellid(long lCellID_in)
  {
    long lCellIndex=-1;

    std::vector<hexagon>::iterator iIterator;
    for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID == lCellID_in)
          {
            lCellIndex = (*iIterator).lCellIndex;
            break;
          }
      }

    return lCellIndex;
  }
}
