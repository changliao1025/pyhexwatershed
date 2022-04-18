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
    //update vertex first
    update_cell_elevation();
    update_vertex_elevation();
    std::string sFilename;
    if (iFlag_global !=1)
      {
        //now we will update some new result due to debug flag
        //compset_save_variable(eV_elevation);
        //compset_save_variable(eV_flow_direction);
        //compset_save_variable(eV_slope_between);
        //compset_save_variable(eV_slope_within);
        //compset_save_variable(eV_flow_accumulation);
        //compset_save_variable(eV_wetness_index);
        //close log file
        //compset_save_watershed_characteristics();

      }
    else
      {

      }
    sFilename = sFilename_json;
    std::cout << sFilename << endl;
    compset_save_json(sFilename);
    sFilename = sFilename_vtk;

    compset_save_vtk(sFilename);

    ofs_log.close();
    std::cout << "Finished saving results!" << endl;
    std::flush(std::cout);

    return error_code;
  }

  int compset::compset_save_json(std::string sFilename_in)
  {
    int error_code=1;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    std::vector<hexagon>::iterator iIterator;

    jsonmodel::mesh cMesh;
    if (iFlag_global !=1)
      {

        if (iFlag_multiple_outlet !=1)
          {
            for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
              {
                if (  (*iIterator).iFlag_watershed ==1)
                  {
                    cell pCell;
                    pCell.dLongitude_center_degree = (*iIterator).dLongitude_center_degree;
                    pCell.dLatitude_center_degree = (*iIterator).dLatitude_center_degree;
                    pCell.dSlope_between = (*iIterator).dSlope_max_downslope;
                    pCell.dSlope_profile = (*iIterator).dSlope_elevation_profile0;
                    pCell.dElevation_mean = (*iIterator).dElevation_mean;
                    pCell.dElevation_raw = (*iIterator).dElevation_raw;
                    pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
                    pCell.dArea =  (*iIterator).dArea;
                    pCell.lCellID = (*iIterator).lCellID;
                    pCell.iStream_segment_burned = (*iIterator).iStream_segment_burned; //flag for burned stream

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
                
                //pCell.dSlope_within = (*iIterator).dSlope_within;
                pCell.dElevation_mean = (*iIterator).dElevation_mean;
                pCell.dElevation_raw = (*iIterator).dElevation_raw;
                pCell.dElevation_profile0 = (*iIterator).dElevation_profile0;
                pCell.lCellID = (*iIterator).lCellID;
                pCell.lCellID_downslope = (*iIterator).lCellID_downslope_dominant;
                pCell.dArea =  (*iIterator).dArea;
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
            pCell.dArea =  (*iIterator).dArea;
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

    error_code = cWatershed.save_watershed_characteristics(sFilename_watershed_characteristics);

    return error_code;
  }

  /**
   * an advanced way to save important watershed dataset
   * @param eV_in
   * @return
   */
  int compset::compset_save_variable(eVariable eV_in)
  {
    int error_code = 1;
    int iFlag_debug = cParameter.iFlag_debug;
    std::string sFieldname;
    std::string sFilename;
    std::string sLayername;
    if (iFlag_debug == 1)
      {
        switch (eV_in)
          {
          case eV_elevation:
            sFieldname = "loid";
            sFilename = sFilename_elevation_polygon_debug;
            sLayername = "elevation";
            compset_save_polygon_vector(eV_elevation, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_direction:
            sFieldname = "dire";
            sFilename = sFilename_flow_direction_polyline_debug;
            sLayername = "direction";
            compset_save_polyline_vector(eV_flow_direction, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_accumulation:


            break;
          case eV_stream_grid:
            sFieldname = "strg";
            sFilename = sFilename_stream_grid_polygon_debug;
            sLayername = "accumulation";

            compset_save_polygon_vector(eV_stream_grid, sFieldname, sFilename, sLayername);
            break;
          default:
            break;
          }
      }
    else
      {
        switch (eV_in)
          {
          case eV_elevation:
            sFieldname = "loid";
            sFilename = sFilename_elevation_polygon;
            sLayername = "elevation";

            compset_save_polygon_vector(eV_elevation, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_direction:
            sFieldname = "dire";
            sFilename = sFilename_flow_direction_polyline;
            sLayername = "direction";
            compset_save_polyline_vector(eV_flow_direction, sFieldname, sFilename, sLayername);

            break;
          case eV_slope_between:
            sFieldname = "slopb";
            sFilename = sFilename_slope_between_polygon;
            sLayername = "slopebet";
            compset_save_polygon_vector(eV_slope_between, sFieldname, sFilename, sLayername);

            break;
          case eV_slope_within:
            sFieldname = "slopw";
            sFilename = sFilename_slope_within_polygon;
            sLayername = "slopewit";
            compset_save_polygon_vector(eV_slope_within, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_accumulation:
            sFieldname = "accu";

            sLayername = "accumulation";

            sFilename = sFilename_flow_accumulation_polygon;
            compset_save_polygon_vector(eV_flow_accumulation, sFieldname, sFilename, sLayername);

            break;
          case eV_watershed:
            sFieldname = "wash";

            sLayername = "watershed";


            sFilename = sFilename_watershed_polygon;
            compset_save_polygon_vector(eV_watershed, sFieldname, sFilename, sLayername);
            break;

          case eV_confluence:
            sFieldname = "conf";
            sFilename = sFilename_stream_confluence_polygon;
            sLayername = "confluence";
            compset_save_polygon_vector(eV_confluence, sFieldname, sFilename, sLayername);

            break;
          case eV_segment:
            sFieldname = "segm";

            sLayername = "segment";

            sFilename = sFilename_stream_segment_polygon;
            compset_save_polygon_vector(eV_segment, sFieldname, sFilename, sLayername);



            sFilename = sFilename_stream_segment_merge_polyline;
            compset_save_polyline_vector(eV_segment, sFieldname, sFilename, sLayername);
            break;

          case eV_stream_order:
            sFieldname = "stro";
            sLayername = "strord";

            sFilename = sFilename_stream_order_polyline;
            compset_save_polyline_vector(eV_stream_order, sFieldname, sFilename, sLayername);
            break;

          case eV_subbasin:
            sFieldname = "suba";

            sLayername = "subbasin";

            sFilename = sFilename_subbasin_polygon;
            compset_save_polygon_vector(eV_subbasin, sFieldname, sFilename, sLayername);
            break;
          case eV_wetness_index:
            sFieldname = "weti";
            //sFilename = sFilename_wetness_index_point;
            sLayername = "wetness";

            sFilename = sFilename_wetness_index_polygon;
            compset_save_polygon_vector(eV_wetness_index, sFieldname, sFilename, sLayername);
            break;

          default:
            break;
          }
      }

    return error_code;
  }

  /**
   * save point based shapefile
   * @param eV_in :the variable enumerate
   * @param sFieldname_in :the attribute table field name
   * @param sFilename_in :the filename of the output file
   * @param sLayer_name_in :the layer name
   * @return error_code
   */


  /**
   * save model outputs in the polyline shapefile format
   * @param eV_in :the variable enumerate
   * @param sFieldname_in :the attribute table field name
   * @param sFilename_in :the filename of the output file
   * @param sLayername_in :the layer name
   * @return
   */
  int compset::compset_save_polyline_vector(eVariable eV_in, std::string sFieldname_in, std::string sFilename_in,
                                            std::string sLayername_in)
  {
    int error_code = 1;
    int iValue;
    int iReach;
    int iFlag_debug = cParameter.iFlag_debug;
    int iFlag_merge_reach = cParameter.iFlag_merge_reach;
    long lIndex;

    long lIndex_downslope;
    float dx, dy;
    float dX_start, dY_start;
    float dX_end, dY_end;
    std::vector<hexagon> vReach_segment;
    std::vector<hexagon>::iterator iIterator;

    std::vector<segment>::iterator iIterator_segment;



    switch (eV_in)
      {
      case eV_flow_direction:

        break;
      case eV_stream_order:

        break;
      case eV_flow_accumulation:

        break;
      case eV_segment:

        break;
      default:
        break;
      }


    if (iFlag_debug == 1)
      {
        switch (eV_in)
          {
          case eV_flow_direction:
            {
              for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
                {


                }
              break;
            }

          default:

            break;
          }
      }
    else
      {
        switch (eV_in)
          {
          case eV_flow_direction:
            {
              for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
                {

                  if ((*iIterator).iFlag_watershed == 1)
                    {

                      lIndex_downslope = (*iIterator).lCellID_downslope_dominant;
                      if (lIndex_downslope >= 0) //this might be not useful because a grid in watershed should has downslope
                        {


                        }
                      else
                        {
                          std::cout << "This is the outlet? :" << (*iIterator).iFlag_outlet << std::endl;
                        }
                    }
                  else
                    {
                    }
                }
              break;
            }
          case eV_stream_order:
            {
              for (iIterator_segment = cWatershed.vSegment.begin(); iIterator_segment != cWatershed.vSegment.end(); iIterator_segment++)
                {



                }
              break;
            }
          default: //stream segment
            {
              if (iFlag_merge_reach != 1)
                {
                  for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
                    {

                      if ((*iIterator).iFlag_stream == 1 && (*iIterator).iFlag_watershed == 1)
                        {

                        }
                      else
                        {
                        }
                    }
                }
              else //merge flowline using segment class
                {
                  for (iIterator_segment = cWatershed.vSegment.begin(); iIterator_segment != cWatershed.vSegment.end(); iIterator_segment++)
                    {

                    }
                }

              break;
            }
          }
      }



    return error_code;
  }

  /**
   * save model outputs in the polygon shapefile format
   * @param eV_in :the variable enumerate
   * @param sFieldname_in :the attribute table field name
   * @param sFilename_in :the filename of the output file
   * @param sLayername_in :the layer name
   * @return error_code
   */
  int compset::compset_save_polygon_vector(eVariable eV_in,
                                           std::string sFieldname_in, std::string sFilename_in,
                                           std::string sLayername_in)
  {
    int error_code = 1;
    int iFlag_debug = cParameter.iFlag_debug;
    const char *pszDriverName = "ESRI Shapefile";



    std::vector<hexagon>::iterator iIterator;

    std::vector<vertex>::iterator iIterator2;



    switch (eV_in)
      {
      case eV_elevation:

        break;
      case eV_flow_direction:

        break;
      case eV_slope_between:

        break;
      case eV_slope_within:

        break;
      case eV_flow_accumulation:

        break;
      case eV_stream_grid:

        break;
      case eV_watershed:

        break;
      case eV_confluence:

        break;
      case eV_segment:

        break;
      case eV_subbasin:

        break;
      case eV_wetness_index:

        break;
      default:
        break;
      }
    int iValue;
    float dValue;


    if (iFlag_debug == 1)
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {

            //if ((*iIterator).nNeighbor_land >=1)




          }
      }
    else
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {

            if ((*iIterator).iFlag_watershed == 1)
              {

              }
            else
              {
              }
          }
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
        //point
        nHexagon = vCell_active.size();
        nVertex = vVertex_active.size();

        //we consider both vertex and the center of hexagon
        sPoint = convert_long_to_string(nVertex + nHexagon);

        sLine = "POINTS " + sPoint + " float";
        ofs_vtk << sLine << std::endl;

        //hexagon center first
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {

            dx = (*iIterator).dx;
            dy = (*iIterator).dy;
            dz = (*iIterator).dz* dRatio_vtk_z_exaggerate;
            sLine = convert_float_to_string(dx) + " "
              + convert_float_to_string(dy) + " "
              + convert_float_to_string(dz);
            ofs_vtk << sLine << std::endl;
          }
        //then hexagon vertex
        //because the vertex index start from 0, we need to add the nhexagon to have unique index
        for (iIterator2 = vVertex_active.begin(); iIterator2 != vVertex_active.end(); iIterator2++)
          {
            dx = (*iIterator2).dx;
            dy = (*iIterator2).dy;
            dz = (*iIterator2).dz* dRatio_vtk_z_exaggerate;

            sLine = convert_float_to_string(dx) + " "
              + convert_float_to_string(dy) + " "
              + convert_float_to_string(dz);
            ofs_vtk << sLine << std::endl;
          }

        //then cell (polygon + polyline)
        //we need to execlude boundary because they have no downslope for line feature
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
            lCount  = lCount + (*iIterator).nVertex + 1 ;
          }
        sCell_size = convert_long_to_string(lCount + (nHexagon - nBoundary) * 3);

        sLine = "CELLS " + sCell + " " + sCell_size;
        ofs_vtk << sLine << std::endl;
        //hexagon polygon
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

        //polyline
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            if ((*iIterator).lCellID_downslope_dominant != -1)
              {
                sLine = "2 ";
                lCellID = (*iIterator).lCellID_downslope_dominant;
                lCellIndex = compset_find_index_by_cellid(lCellID);
                sLine = sLine + convert_long_to_string((*iIterator).lCellIndex) + " "
                  + convert_long_to_string(lCellIndex);
                ofs_vtk << sLine << std::endl;
              }
          }
        //cell type information

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
        //attributes

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

        //we consider both vertex and the center of hexagon
        sPoint = convert_long_to_string(nVertex + nHexagon);

        sLine = "POINTS " + sPoint + " float";
        ofs_vtk << sLine << std::endl;

        //hexagon center first
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            dx = (*iIterator).dx;
            dy = (*iIterator).dy;
            dz = (*iIterator).dz* dRatio_vtk_z_exaggerate;
            sLine = convert_float_to_string(dx) + " "
              + convert_float_to_string(dy) + " "
              + convert_float_to_string(dz);
            ofs_vtk << sLine << std::endl;
          }
        //then hexagon vertex
        //because the vertex index start from 0, we need to add the nhexagon to have unique index
        for (iIterator2 = vVertex_active.begin(); iIterator2 != vVertex_active.end(); iIterator2++)
          {

            dx = (*iIterator2).dx;
            dy = (*iIterator2).dy;
            dz = (*iIterator2).dz * dRatio_vtk_z_exaggerate;

            sLine = convert_float_to_string(dx) + " "
              + convert_float_to_string(dy) + " "
              + convert_float_to_string(dz);
            ofs_vtk << sLine << std::endl;
          }

        //then cell (polygon + polyline)
        //we need to execlude boundary because they have no downslope
        nBoundary = 0;
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            if ((*iIterator).lCellID_downslope_dominant == -1)
              {
                nBoundary = nBoundary + 1;
              }
          }
        sCell = convert_long_to_string(nHexagon + (nHexagon - nBoundary));


        lCount =0 ;
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            lCount  = lCount + (*iIterator).nVertex +1 ;
          }
        sCell_size = convert_long_to_string(lCount + (nHexagon - nBoundary) * 3);

        sLine = "CELLS " + sCell + " " + sCell_size;
        ofs_vtk << sLine << std::endl;
        //hexagon polygon
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

        //polyline
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            if ((*iIterator).lCellID_downslope_dominant != -1)
              {
                sLine = "2 ";
                //cannot use cellindex anymore?
                lCellID = (*iIterator).lCellID_downslope_dominant;
                lCellIndex = compset_find_index_by_cellid(lCellID);
                sLine = sLine + convert_long_to_string((*iIterator).lCellIndex) + " "
                  + convert_long_to_string(lCellIndex);
                ofs_vtk << sLine << std::endl;
              }
          }
        //cell type information

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

        //attributes

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
