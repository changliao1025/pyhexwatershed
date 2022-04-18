/**
 * @file watershed.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief 
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */

#include "watershed.h"

namespace hexwatershed
{
  watershed::watershed()
  {
  }

  watershed::~watershed()
  {
  }

  /**
   * build the stream topology based on stream segment information
   * @return
   */
  int watershed::watershed_build_stream_topology()
  {
    int error_code = 1;
    int iSegment;
    //rebuild stream topology
    std::vector<segment>::iterator iIterator_segment_self;
    std::vector<segment>::iterator iIterator_segment;
    for (iIterator_segment_self = vSegment.begin();
         iIterator_segment_self != vSegment.end();
         iIterator_segment_self++)
    {
      iSegment = (*iIterator_segment_self).iSegment_downstream;
      for (iIterator_segment = vSegment.begin();
           iIterator_segment != vSegment.end();
           iIterator_segment++)
      {
        if (iSegment == (*iIterator_segment).iSegment)
        {
          (*iIterator_segment).vSegment_upstream.push_back((*iIterator_segment_self).iSegment);
        }
      }
    }
    for (iIterator_segment = vSegment.begin();
         iIterator_segment != vSegment.end();
         iIterator_segment++)
    {
      (*iIterator_segment).nSegment_upstream = (*iIterator_segment).vSegment_upstream.size();
    }

    return error_code;
  }

  /**
   * build the stream order based on stream topology
   * @return
   */
  int watershed::watershed_define_stream_order()
  {
    int error_code = 1;
    int iSegment;
    int iUpstream;
    int iStream_order_max;
    int iFlag_all_upstream_done;

    std::vector<int> vStream_order;

    std::vector<segment>::iterator iIterator_segment;

    for (iIterator_segment = vSegment.begin();
         iIterator_segment != vSegment.end();
         iIterator_segment++)
    {
      if ((*iIterator_segment).iFlag_headwater == 1)
      {
        (*iIterator_segment).iSegment_order = 1;
      }
    }

    while (vSegment.back().iSegment_order == -1)
    {
      for (iIterator_segment = vSegment.begin();
           iIterator_segment != vSegment.end();
           iIterator_segment++)
      {

        if ((*iIterator_segment).iSegment_order == -1)
        {
          iFlag_all_upstream_done = 1;
          vStream_order.clear();
          for (iUpstream = 0;
               iUpstream < (*iIterator_segment).nSegment_upstream;
               iUpstream++)
          {
            iSegment = (*iIterator_segment).vSegment_upstream.at(iUpstream);
            if (vSegment.at(iSegment - 1).iSegment_order == -1)
            {
              iFlag_all_upstream_done = 0;
            }
            else
            {
              vStream_order.push_back(vSegment.at(iSegment - 1).iSegment_order);
            }
          }

          if (iFlag_all_upstream_done == 1)
          {
            if (vStream_order.at(0) == vStream_order.at(1))
            {
              (*iIterator_segment).iSegment_order = vStream_order.at(0) + 1;
            }
            else
            {
              iStream_order_max = (*max_element(std::begin(vStream_order), std::end(vStream_order))); // c++11
              (*iIterator_segment).iSegment_order = iStream_order_max;
            }
          }
        }
        else
        {
          //finished
        }
      }
    }

    return error_code;
  }

  /**
   * calculate the watershed characteristics
   * @return
   */
  int watershed::calculate_watershed_characteristics()
  {
    int error_code = 1;
    float dLength_stream_conceptual;

    std::vector<segment>::iterator iIterator0;
    std::vector<subbasin>::iterator iIterator1;
    

    for (iIterator0 = vSegment.begin(); iIterator0 != vSegment.end(); iIterator0++)
    {
      (*iIterator0).calculate_stream_segment_characteristics();
    }

    for (iIterator1 = vSubbasin.begin(); iIterator1 != vSubbasin.end(); iIterator1++)
    {
      dLength_stream_conceptual = vSegment.at((*iIterator1).iSubbasin - 1).dLength;
      (*iIterator1).calculate_subbasin_characteristics(dLength_stream_conceptual);
    }

    //should we write the result directly here?

    calculate_watershed_drainage_area();
    calculate_watershed_total_stream_length();
    calculate_watershed_longest_stream_length();
    calculate_watershed_drainage_density();
    calculate_watershed_average_slope();
    //calculate_topographic_wetness_index();

    //save watershed characteristics to the file

    

    std::cout << "The watershed characteristics are calculated successfully!" << std::endl;

    return error_code;
  }

  /**
   * calculate the watershed drainage total area
   * we can either sum up hexagon or sum up subbasin
   * @return
   */
  int watershed::calculate_watershed_drainage_area()
  {
    int error_code = 1;
    int iOption = 2; //sum up subbasin

    float dArea_total = 0.0;    
    std::vector<hexagon>::iterator iIterator;
    std::vector<subbasin>::iterator iIterator1;
    if (iOption == 1)
    {
      for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
      {
        dArea_total = dArea_total + (*iIterator).dArea;
      }
    }
    else
    {
      for (iIterator1 = vSubbasin.begin(); iIterator1 != vSubbasin.end(); iIterator1++)
      {

        dArea_total = dArea_total + (*iIterator1).dArea;
      }
    }    
    dArea = dArea_total;
    return error_code;
  }

  /**
   * calculate the total stream length
   * @return
   */
  int watershed::calculate_watershed_total_stream_length()
  {
    int error_code = 1;
    int iOption = 2; //sum up subbasin

    float dLength_total = 0.0;

    std::vector<hexagon>::iterator iIterator;
    std::vector<segment>::iterator iIterator1;
    if (iOption == 1)
    {
      for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
      {

        if ((*iIterator).iFlag_stream == 1)
        {
          //should have calculated dLength_stream_conceptual by now
          dLength_total = dLength_total + (*iIterator).dLength_stream_conceptual;
        }
      }
    }
    else
    {
      for (iIterator1 = vSegment.begin(); iIterator1 != vSegment.end(); iIterator1++)
      {
        dLength_total = dLength_total + (*iIterator1).dLength;
      }
    }

    dLength_stream_conceptual = dLength_total;

    return error_code;
  }

  /**
   * calculate the longest stream length
   * @return
   */
  int watershed::calculate_watershed_longest_stream_length()
  {
    int error_code = 1;

    float dLength_longest = 0.0;
    float dLength_stream_conceptual;

    //loop through head water
    std::vector<segment>::iterator iIterator;

    for (iIterator = vSegment.begin(); iIterator != vSegment.end(); iIterator++)
    {
      dLength_stream_conceptual = (*iIterator).dLength;
      if (dLength_stream_conceptual > dLength_longest)
      {
        dLength_longest = dLength_stream_conceptual;
      }
    }

    dLongest_length_stream = dLength_longest;

    return error_code;
  }

  /**
   * calculate the watershed area to stream length ratio
   * @return
   */
  int watershed::calculate_watershed_drainage_density()
  {
    int error_code = 1;

    float dRatio = 0.0;

    if (dLength_stream_conceptual > 0)
    {
      dRatio = dArea / dLength_stream_conceptual;
    }

    dArea_2_stream_ratio = dRatio;
    dLength_2_area_ratio = 1.0 / dRatio;
    dDrainage_density = dLength_2_area_ratio;

    return error_code;
  }

  /**
   * calculate the mean slope of the watershed
   * we can use either subbasin or each cell
   * @return
   */
  int watershed::calculate_watershed_average_slope()
  {
    int error_code = 1;
    int iOption = 1;
    float dSlope_total = 0.0;
    std::vector<hexagon>::iterator iIterator;
    std::vector<subbasin>::iterator iIterator1;
    if (iOption == 1)//by cell
    {
      for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
      {
        dSlope_total = dSlope_total + (*iIterator).dSlope_within; //should mean slope?
      }
    }
    else//by subbasin
    {
      for (iIterator1 = vSubbasin.begin(); iIterator1 != vSubbasin.end(); iIterator1++)
      {
        dSlope_total = dSlope_total + (*iIterator1).dSlope;
      }
    }

    dSlope = dSlope_total / nCell;
    dSlope_mean = dSlope;
    return error_code;
  }

  /**
   * calculate the TWI index using method from //https://en.wikipedia.org/wiki/Topographic_wetness_index
   * // {\displaystyle \ln {a \over \tan b}}
   * @return
   */
  int watershed::calculate_topographic_wetness_index()
  {
    int error_code = 1;
    float a;
    float b;
    float c;
    float d;
    float dTwi;
    std::vector<hexagon>::iterator iIterator;
    //can use openmp
    for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
    {
      if ((*iIterator).iFlag_outlet == 1)
      {
        (*iIterator).dTwi = -1;
      }
      else
      {
        a = float(((*iIterator).dAccumulation ) );
        b = (*iIterator).dSlope;
        c = tan(b);
        if (a == 0 || c == 0)
        {
          std::cout << a << b << c << std::endl;
        }
        dTwi = log2(a / c);
        if (isnan(float(dTwi)))
        {
          std::cout << a << b << c << std::endl;
        }
        (*iIterator).dTwi = dTwi;
      }
    }

    return error_code;
  }

  /**
       * save the watershed characteristics in the output
       * @return
       */
  int watershed::save_watershed_characteristics(std::string sFilename_in)
  {
    int error_code = 1;

    std::string sLine;

    std::ofstream ofs;
    ofs.open(sFilename_in.c_str(), ios::out);
    if (ofs.good())
    {
      sLine = "Watershed drainage area: " + convert_float_to_string(dArea);
      ofs << sLine << std::endl;

      sLine = "Longest stream length: " + convert_float_to_string(dLongest_length_stream);
      ofs << sLine << std::endl;

      sLine = "Total stream length: " + convert_float_to_string(dLength_stream_conceptual);
      ofs << sLine << std::endl;

      sLine = "Drainage density: " + convert_float_to_string(dDrainage_density);
      ofs << sLine << std::endl;

      sLine = "Average slope: " + convert_float_to_string(dSlope_mean);
      ofs << sLine << std::endl;

      ofs.close();
    }

    return error_code;
  }
} // namespace hexwatershed