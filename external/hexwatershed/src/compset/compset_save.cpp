/**
 * @file compset.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the realization of the compset class
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
   * save all the model outputs
   * @return
   */
  int compset::compset_save_model()
  {
    int error_code = 1;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;

    std::string sFilename;
    if (iFlag_global != 1)
    {
      // now we will update some new result due to debug flag
      compset_save_watershed_characteristics();
    }
    else
    {
    }
    
   

    // update from watershed to main

    // main json file
    sFilename = sFilename_json;
    compset_save_json(sFilename);
    
    sFilename=sFilename_domain_json;
    compset_save_domain_json(sFilename);

    sFilename = sFilename_animation_json;
    compset_save_animation_json(sFilename);
    sFilename = sFilename_vtk;

    compset_save_vtk(sFilename);

    ofs_log.close();
    std::cout << "Finished saving results!" << endl;
    std::flush(std::cout);

    return error_code;
  }

  int compset::compset_save_animation_json(std::string sFilename_in)
  {
    int error_code = 1;
    
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    std::vector<hexagon>::iterator iIterator;

    jsonmodel::mesh cMesh;


     if (iFlag_global != 1)
    {
      if (iFlag_multiple_outlet != 1)
      {
   //animation
        for (iIterator = vCell_priority_flood.begin(); iIterator != vCell_priority_flood.end(); iIterator++)
        {         
            cell pCell;            
            pCell.lCellID = (*iIterator).lCellID;           
            cMesh.aCell.push_back(pCell);          
        }

        cMesh.SerializeToFile(sFilename_in.c_str());
      }
    }
      return error_code;
  }
  int compset::compset_save_domain_json(std::string sFilename_in)
  {
    int error_code = 1;
    int iWatershed;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    std::vector<hexagon>::iterator iIterator;

    jsonmodel::mesh cMesh;

    if (iFlag_global != 1)
    {
      if (iFlag_multiple_outlet != 1)
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
        {
          
            cell pCell;
            pCell.dLongitude_center_degree = (*iIterator).dLongitude_center_degree;
            pCell.dLatitude_center_degree = (*iIterator).dLatitude_center_degree;
            pCell.dSlope_between = (*iIterator).dSlope_max_downslope;
            pCell.dSlope_profile = (*iIterator).dSlope_elevation_profile0;
            pCell.dDistance_to_downslope = (*iIterator).dDistance_to_downslope;
            pCell.dDistance_to_subbasin_outlet = (*iIterator).dDistance_to_subbasin_outlet;
            pCell.dDistance_to_watershed_outlet = (*iIterator).dDistance_to_watershed_outlet;
            pCell.dElevation_mean = (*iIterator).dElevation_mean;
            pCell.dElevation_raw = (*iIterator).dElevation_raw;
            pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
            pCell.dLength = (*iIterator).dLength_stream_conceptual;
            pCell.dLength_flowline = (*iIterator).dLength_stream_burned;
            pCell.dArea = (*iIterator).dArea;
            pCell.lCellID = (*iIterator).lCellID;
            pCell.iStream_segment = (*iIterator).iSegment;
            pCell.iSubbasin = (*iIterator).iSubbasin;
            pCell.iStream_segment_burned = (*iIterator).iStream_segment_burned; // flag for burned stream

            pCell.lCellID_downslope = (*iIterator).lCellID_downslope_dominant;
            pCell.dAccumulation = (*iIterator).dAccumulation;
            pCell.vVertex = (*iIterator).vVertex;
            pCell.nVertex = pCell.vVertex.size();
            cMesh.aCell.push_back(pCell);
          
        }

        cMesh.SerializeToFile(sFilename_in.c_str());

      }
    }
    return error_code;
  }
  int compset::compset_save_json(std::string sFilename_in)
  {
    int error_code = 1;
    int iWatershed;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    std::vector<hexagon>::iterator iIterator;

    jsonmodel::mesh cMesh;

    for (iWatershed = 1; iWatershed <= cParameter.nOutlet; iWatershed++)
    {
      vWatershed.at(iWatershed - 1).watershed_save_json();
      vWatershed.at(iWatershed - 1).watershed_save_stream_edge_json();
    }

    if (iFlag_global != 1)
    {
      if (iFlag_multiple_outlet != 1)
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
        {
          if ((*iIterator).iFlag_watershed == 1)
          {
            cell pCell;
            pCell.dLongitude_center_degree = (*iIterator).dLongitude_center_degree;
            pCell.dLatitude_center_degree = (*iIterator).dLatitude_center_degree;
            pCell.dSlope_between = (*iIterator).dSlope_max_downslope;
            pCell.dSlope_profile = (*iIterator).dSlope_elevation_profile0;
            pCell.dDistance_to_downslope = (*iIterator).dDistance_to_downslope;
            pCell.dDistance_to_subbasin_outlet = (*iIterator).dDistance_to_subbasin_outlet;
            pCell.dDistance_to_watershed_outlet = (*iIterator).dDistance_to_watershed_outlet;
            pCell.dElevation_mean = (*iIterator).dElevation_mean;
            pCell.dElevation_raw = (*iIterator).dElevation_raw;
            pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
            pCell.dLength = (*iIterator).dLength_stream_conceptual;
            pCell.dLength_flowline = (*iIterator).dLength_stream_burned;
            pCell.dArea = (*iIterator).dArea;
            pCell.lCellID = (*iIterator).lCellID;
            pCell.iStream_segment = (*iIterator).iSegment;
            pCell.iSubbasin = (*iIterator).iSubbasin;
            pCell.iStream_segment_burned = (*iIterator).iStream_segment_burned; // flag for burned stream

            pCell.lCellID_downslope = (*iIterator).lCellID_downslope_dominant;
            pCell.dAccumulation = (*iIterator).dAccumulation;
            pCell.vVertex = (*iIterator).vVertex;
            pCell.nVertex = pCell.vVertex.size();
            cMesh.aCell.push_back(pCell);
          }
        }

        cMesh.SerializeToFile(sFilename_in.c_str());
     
      }
      else
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
        {

          cell pCell;
          pCell.dLongitude_center_degree = (*iIterator).dLongitude_center_degree;
          pCell.dLatitude_center_degree = (*iIterator).dLatitude_center_degree;
          pCell.dSlope_between = (*iIterator).dSlope_max_downslope;
          pCell.dSlope_profile = (*iIterator).dSlope_elevation_profile0;

          // pCell.dSlope_within = (*iIterator).dSlope_within;
          pCell.dElevation_mean = (*iIterator).dElevation_mean;
          pCell.dElevation_raw = (*iIterator).dElevation_raw;
          pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
          pCell.lCellID = (*iIterator).lCellID;
          pCell.lCellID_downslope = (*iIterator).lCellID_downslope_dominant;
          pCell.dArea = (*iIterator).dArea;
          pCell.dAccumulation = (*iIterator).dAccumulation;
          pCell.vVertex = (*iIterator).vVertex;
          pCell.nVertex = pCell.vVertex.size();
          cMesh.aCell.push_back(pCell);
        }

        cMesh.SerializeToFile(sFilename_in.c_str());
      }
    }
    else
    {
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {

        cell pCell;
        pCell.dLongitude_center_degree = (*iIterator).dLongitude_center_degree;
        pCell.dLatitude_center_degree = (*iIterator).dLatitude_center_degree;
        pCell.dSlope_between = (*iIterator).dSlope_max_downslope;

        pCell.dSlope_within = (*iIterator).dSlope_within;
        pCell.dElevation_raw = (*iIterator).dElevation_raw;
        pCell.dElevation_mean = (*iIterator).dElevation_mean;
        pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
        pCell.dArea = (*iIterator).dArea;
        pCell.dAccumulation = (*iIterator).dAccumulation;
        pCell.lCellID = (*iIterator).lCellID;

        pCell.lCellID_downslope = (*iIterator).lCellID_downslope_dominant;

        pCell.vVertex = (*iIterator).vVertex;
        pCell.nVertex = pCell.vVertex.size();
        cMesh.aCell.push_back(pCell);
      }

      cMesh.SerializeToFile(sFilename_in.c_str());
    }

    return error_code;
  }
  /**
   * save the watershed characteristics in the output
   * @return
   */
  int compset::compset_save_watershed_characteristics()
  {
    int error_code = 1;
    int iWatershed;
    for (iWatershed = 1; iWatershed <= cParameter.nOutlet; iWatershed++)
    {
      vWatershed.at(iWatershed - 1).save_watershed_characteristics();
      vWatershed.at(iWatershed - 1).save_segment_characteristics();
      vWatershed.at(iWatershed - 1).save_subbasin_characteristics();
    }

    return error_code;
  }

  int compset::compset_save_vtk(std::string sFilename_in)
  {
    int error_code = 1;
    int iVertex;
    int iFlag_debug = cParameter.iFlag_debug;
    long lValue;
    long lCount;
    long lCellID, lCellIndex;
    long nVertex, nHexagon, nBoundary;
    float dr, dx, dy, dz;
    std::string sDummy;
    std::string sLine;
    std::string sPoint, sCell, sCell_size;
    std::ofstream ofs_vtk;
    std::vector<hexagon>::iterator iIterator;
    std::vector<vertex>::iterator iIterator2;

    float dRatio_vtk_z_exaggerate = 100.0;

    ofs_vtk.open(sFilename_in.c_str(), ios::out);

    sLine = "# vtk DataFile Version 2.0";
    ofs_vtk << sLine << std::endl;
    sLine = "Flow direction unstructured grid";
    ofs_vtk << sLine << std::endl;
    sLine = "ASCII";
    ofs_vtk << sLine << std::endl;
    sLine = "DATASET UNSTRUCTURED_GRID";
    ofs_vtk << sLine << std::endl;

    if (iFlag_debug == 1)
    {
      // point
      nHexagon = vCell_active.size();
      nVertex = vVertex_active.size();

      // we consider both vertex and the center of hexagon
      sPoint = convert_long_to_string(nVertex + nHexagon);

      sLine = "POINTS " + sPoint + " float";
      ofs_vtk << sLine << std::endl;

      // hexagon center first
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {

        dx = (*iIterator).dx;
        dy = (*iIterator).dy;
        dz = (*iIterator).dz * dRatio_vtk_z_exaggerate;
        sLine = convert_float_to_string(dx) + " " + convert_float_to_string(dy) + " " + convert_float_to_string(dz);
        ofs_vtk << sLine << std::endl;
      }
      // then hexagon vertex
      // because the vertex index start from 0, we need to add the nhexagon to have unique index
      for (iIterator2 = vVertex_active.begin(); iIterator2 != vVertex_active.end(); iIterator2++)
      {
        dx = (*iIterator2).dx;
        dy = (*iIterator2).dy;
        dz = (*iIterator2).dz * dRatio_vtk_z_exaggerate;

        sLine = convert_float_to_string(dx) + " " + convert_float_to_string(dy) + " " + convert_float_to_string(dz);
        ofs_vtk << sLine << std::endl;
      }

      // then cell (polygon + polyline)
      // we need to execlude boundary because they have no downslope for line feature
      nBoundary = 0;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant == -1)
        {
          nBoundary = nBoundary + 1;
        }
      }
      sCell = convert_long_to_string(nHexagon + (nHexagon - nBoundary));
      lCount = 0;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        lCount = lCount + (*iIterator).nVertex + 1;
      }
      sCell_size = convert_long_to_string(lCount + (nHexagon - nBoundary) * 3);

      sLine = "CELLS " + sCell + " " + sCell_size;
      ofs_vtk << sLine << std::endl;
      // hexagon polygon
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        iVertex = (*iIterator).nVertex;
        sLine = convert_integer_to_string(iVertex) + " ";
        for (iIterator2 = (*iIterator).vVertex.begin(); iIterator2 != (*iIterator).vVertex.end(); iIterator2++)
        {
          sLine = sLine + convert_long_to_string((*iIterator2).lVertexIndex + nHexagon) + " ";
        }
        ofs_vtk << sLine << std::endl;
      }

      // polyline
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = "2 ";
          lCellID = (*iIterator).lCellID_downslope_dominant;
          lCellIndex = compset_find_index_by_cell_id(lCellID);
          sLine = sLine + convert_long_to_string((*iIterator).lCellIndex) + " " + convert_long_to_string(lCellIndex);
          ofs_vtk << sLine << std::endl;
        }
      }
      // cell type information

      sLine = "CELL_TYPES " + sCell;
      ofs_vtk << sLine << std::endl;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        sLine = "7";
        ofs_vtk << sLine << std::endl;
      }
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = "3";
          ofs_vtk << sLine << std::endl;
        }
      }
      // attributes

      sLine = "CELL_DATA " + sCell; // convert_long_to_string(nHexagon); //CELL_DATA
      ofs_vtk << sLine << std::endl;
      sLine = "SCALARS elevation float 1";
      ofs_vtk << sLine << std::endl;
      sLine = "LOOKUP_TABLE default";

      ofs_vtk << sLine << std::endl;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        sLine = convert_float_to_string((*iIterator).dElevation_mean);
        ofs_vtk << sLine << std::endl;
      }
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = convert_float_to_string((*iIterator).dElevation_mean);
          ofs_vtk << sLine << std::endl;
        }
      }

      ofs_vtk.close();
    }
    else
    {
      nHexagon = vCell_active.size();
      nVertex = vVertex_active.size();

      // we consider both vertex and the center of hexagon
      sPoint = convert_long_to_string(nVertex + nHexagon);

      sLine = "POINTS " + sPoint + " float";
      ofs_vtk << sLine << std::endl;

      // hexagon center first
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        dx = (*iIterator).dx;
        dy = (*iIterator).dy;
        dz = (*iIterator).dz * dRatio_vtk_z_exaggerate;
        sLine = convert_float_to_string(dx) + " " + convert_float_to_string(dy) + " " + convert_float_to_string(dz);
        ofs_vtk << sLine << std::endl;
      }
      // then hexagon vertex
      // because the vertex index start from 0, we need to add the nhexagon to have unique index
      for (iIterator2 = vVertex_active.begin(); iIterator2 != vVertex_active.end(); iIterator2++)
      {

        dx = (*iIterator2).dx;
        dy = (*iIterator2).dy;
        dz = (*iIterator2).dz * dRatio_vtk_z_exaggerate;

        sLine = convert_float_to_string(dx) + " " + convert_float_to_string(dy) + " " + convert_float_to_string(dz);
        ofs_vtk << sLine << std::endl;
      }

      // then cell (polygon + polyline)
      // we need to execlude boundary because they have no downslope
      nBoundary = 0;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant == -1)
        {
          nBoundary = nBoundary + 1;
        }
      }
      sCell = convert_long_to_string(nHexagon + (nHexagon - nBoundary));

      lCount = 0;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        lCount = lCount + (*iIterator).nVertex + 1;
      }
      sCell_size = convert_long_to_string(lCount + (nHexagon - nBoundary) * 3);

      sLine = "CELLS " + sCell + " " + sCell_size;
      ofs_vtk << sLine << std::endl;
      // hexagon polygon
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        iVertex = (*iIterator).nVertex;
        sLine = convert_integer_to_string(iVertex) + " ";
        for (iIterator2 = (*iIterator).vVertex.begin(); iIterator2 != (*iIterator).vVertex.end(); iIterator2++)
        {
          sLine = sLine + convert_long_to_string((*iIterator2).lVertexIndex + nHexagon) + " ";
        }
        ofs_vtk << sLine << std::endl;
      }

      // polyline
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = "2 ";
          // cannot use cellindex anymore?
          lCellID = (*iIterator).lCellID_downslope_dominant;
          lCellIndex = compset_find_index_by_cell_id(lCellID);
          sLine = sLine + convert_long_to_string((*iIterator).lCellIndex) + " " + convert_long_to_string(lCellIndex);
          ofs_vtk << sLine << std::endl;
        }
      }
      // cell type information

      sLine = "CELL_TYPES " + sCell;
      ofs_vtk << sLine << std::endl;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        sLine = "7";
        ofs_vtk << sLine << std::endl;
      }
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = "3";
          ofs_vtk << sLine << std::endl;
        }
      }

      // attributes

      sLine = "CELL_DATA " + sCell; // convert_long_to_string(nHexagon); //CELL_DATA
      ofs_vtk << sLine << std::endl;
      sLine = "SCALARS elevation float 1";
      ofs_vtk << sLine << std::endl;
      sLine = "LOOKUP_TABLE default";

      ofs_vtk << sLine << std::endl;
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        sLine = convert_float_to_string((*iIterator).dElevation_mean);
        ofs_vtk << sLine << std::endl;
      }
      for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).lCellID_downslope_dominant != -1)
        {
          sLine = convert_float_to_string((*iIterator).dElevation_mean);
          ofs_vtk << sLine << std::endl;
        }
      }

      ofs_vtk.close();
    }

    return error_code;
  }

}
