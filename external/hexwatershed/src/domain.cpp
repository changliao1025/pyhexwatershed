
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file domain.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the realization of the domain class
 * @version 0.1
 * @date 2019-08-02
 *
 * @copyright Copyright (c) 2019
 *
 */
#include "domain.h"

namespace hexwatershed
{

  domain::domain(){};

  domain::~domain(){};

  /**
   *
   * @param sFilename_configuration_in: user provided model configuration file
   * please refer to the user guide for I/O instruction
   */
  domain::domain(std::string sFilename_configuration_in)
  {
    iFlag_debug = 0;
    // check the length of the configuration file
    std::size_t iLength = sFilename_configuration_in.length();
    if (iLength < 5)
      {
        this->iFlag_configuration_file = 0;
      }
    else
      {
        std::cout << "The configuration file is:" << sFilename_configuration_in
                  << std::endl;
        // check the existence of the configuration file
        if (1 != file_test(sFilename_configuration_in)) // the file does not even exist
          {
            this->iFlag_configuration_file = 0;
          }
        else
          {
            this->sFilename_configuration = sFilename_configuration_in;
            this->iFlag_configuration_file = 1;
          }
      }
    iMesh_type = 1;
    nColumn_mesh = 1;
    nRow_mesh = 1;
    dAccumulation_threshold = 0.01;
    sExtension_header = ".hdr";
    sExtension_envi = ".dat";
    sExtension_text = ".txt";
    sRegion = "user";
  }

  /**
   * set up the model
   * @return
   */
  int domain::domain_setup_model()
  {
    int error_code = 1;
    mParameter.insert(std::pair<std::string, std::string>("sRegion",
                                                          sRegion)); //where most global data is stored
    mParameter.insert(std::pair<std::string, std::string>("sWorkspace_data",
                                                          sWorkspace_data)); //where most global data is stored

    mParameter.insert(std::pair<std::string, std::string>("sWorkspace_output",
                                                          sWorkspace_output));
    mParameter.insert(std::pair<std::string, std::string>("sFilename_elevation_raster", sFilename_elevation_raster));

    mParameter.insert(
                      std::pair<std::string, std::string>("sFilename_hexagon_point_shapefile",
                                                          sFilename_hexagon_point_shapefile));

    mParameter.insert(
                      std::pair<std::string, std::string>("sFilename_hexagon_polygon_shapefile",
                                                          sFilename_hexagon_polygon_shapefile));
    mParameter.insert(std::pair<std::string, std::string>(
                                                          "iCase",
                                                          convert_integer_to_string(iCase, 1)));

    mParameter.insert(std::pair<std::string, std::string>(
                                                          "iMesh_type",
                                                          convert_integer_to_string(iMesh_type, 1)));

    mParameter.insert(std::pair<std::string, std::string>(
                                                          "nColumn_mesh",
                                                          convert_integer_to_string(nColumn_mesh)));

    mParameter.insert(std::pair<std::string, std::string>(
                                                          "nRow_mesh",
                                                          convert_integer_to_string(nRow_mesh)));

    mParameter.insert(std::pair<std::string, std::string>(
                                                          "dAccumulation_threshold",
                                                          convert_double_to_string(dAccumulation_threshold)));

    std::cout << "Finished set up model" << std::endl;
    std::flush(std::cout);
    return error_code;
  }

  /**
   * read data from the model configuration file
   * @return
   */
  int domain::domain_read_data()
  {
    int error_code = 1;
    domain_read_configuration_file();
    domain_retrieve_user_input();

    //read shapefile
    if (file_test(sFilename_hexagon_polygon_shapefile) != 1)
      {
        error_code = 0;
        std::cout << "Shapefile does not exist: " << sFilename_hexagon_polygon_shapefile << std::endl;
        iFlag_hexagon_polygon = 0;
        return error_code;
      }
    else
      {
        iFlag_hexagon_polygon = 1;
      }

    if (file_test(sFilename_hexagon_point_shapefile) != 1)
      {
        error_code = 2;
        std::cout << "Point Hexagon Shapefile does not exist: " << sFilename_hexagon_point_shapefile << std::endl;
        std::cout << "We will use polygon center instead! " << std::endl;
        iFlag_hexagon_point = 0;
      }
    else
      {
        iFlag_hexagon_point = 1;
      }

    if (file_test(sFilename_elevation_raster) != 1)
      {
        error_code = 0;
        std::cout << " dem does not exist! " << sFilename_elevation_raster << std::endl;
        return error_code;
      }
    else
      {
      }
    //at this point, we must at least have both polygon and dem data set.
    domain_read_all_cell_information(sFilename_hexagon_point_shapefile, sFilename_hexagon_polygon_shapefile,
                                     sFilename_elevation_raster);

    std::cout << "Finished reading data!" << std::endl;
    std::flush(std::cout);
    return error_code;
  }

  /**
   * read the user provided configuration file
   * @return
   */
  int domain::domain_read_configuration_file()
  {
    int error_code = 1;
    std::size_t iVector_size;
    std::string sLine;  //used to store each sLine
    std::string sKey;   //used to store the sKey
    std::string sValue; //used to store the sValue
    std::ifstream ifs;  //fstream object to read_eco3d the file
    std::vector<std::string> vTokens;
    //50==================================================
    //the existence of the configuration file is checked already
    //50==================================================
    ifs.open(sFilename_configuration.c_str(), ios::in);
    if (ifs.good())
      {
        std::cout << "Start to read hexwatershed configuration file" << std::endl;
        while (!ifs.eof()) //read_eco3d all the content
          {
            //reset sKey and sValue to null for each sLine
            //50==================================================
            //we should read_eco3d one sLine at a time and then break the sLine into substrings.
            //50==================================================
            std::getline(ifs, sLine); //read_eco3d the sLine
            std::size_t iLength0 = sLine.length();
            if (iLength0 <= 2)
              {
                continue;
              }
            //split the sLine
            vTokens = split_string_by_delimiter(sLine, ',');
            //test the size of the vector
            iVector_size = vTokens.size();
            if (iVector_size == 2)
              {
                sKey = trim(vTokens[0]);   //sKey holds the sKey(address)!
                sValue = trim(vTokens[1]); //the real sValue of the sKey.
              }
            else
              {
                sKey = trim(vTokens[0]); //sKey holds the sKey(address)!
                sValue = trim(sKey);
              }
            //50==================================================
            //check the completeness of the sLine
            //50==================================================
            std::size_t iLength1 = sKey.length();
            std::size_t iLength2 = sValue.length();
            if (iLength1 >= 1 && iLength2 >= 1) //both of them are not NULL
              {
                auto search = this->mParameter.find(sKey); //search the dictionary
                if (search != this->mParameter.end())      //if found, add the sValue to the sKey/address
                  {
                    search->second = sValue;
                  }
                else
                  {
                    //if not, insert this sKey and sValue pair into user map
                    //this map should be used to output control
                  }
              }
            else
              {
                //this may be a empty sLine
                continue;
              }
          }
        //close the file after reading
      }
    else
      {
        error_code = 0;
      }
    ifs.close();

    return error_code;
  }

  /**
   * extract the dictionary from user provided configuration file
   * @return
   */
  int domain::domain_retrieve_user_input()
  {
    int error_code = 1;
    std::string sKey = "sWorkspace_data";
    auto search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sWorkspace_data = search->second;
      }

    sKey = "sRegion";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sRegion = search->second;
      }

    sKey = "sWorkspace_output";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sWorkspace_output = search->second;
      }
    sKey = "sFilename_elevation_raster";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sFilename_elevation_raster = sWorkspace_data + slash + "raster" + slash + "dem" + slash + search->second;
      }
    sKey = "sFilename_hexagon_point_shapefile";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sFilename_hexagon_point_shapefile = sWorkspace_data + slash + "vector" + slash + "mesh" + slash + search->second;
      }

    sKey = "sFilename_hexagon_polygon_shapefile";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->sFilename_hexagon_polygon_shapefile = sWorkspace_data + slash + "vector" + slash + "mesh" + slash + search->second;
      }

    sKey = "iCase";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->iCase = std::stoi(search->second);
      }
    sKey = "iMesh_type";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->iMesh_type = std::stoi(search->second);
      }
    sKey = "nColumn_mesh";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->nColumn_mesh = std::stoi(search->second);
      }
    sKey = "nRow_mesh";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->nRow_mesh = std::stoi(search->second);
      }

    sKey = "dAccumulation_threshold";
    search = mParameter.find(sKey);
    if (search != mParameter.end())
      {
        this->dAccumulation_threshold = std::stod(search->second);
      }

    //output=================================

    if (sWorkspace_output.length() > 3)
      {
        //this will be the output workspace
        if (path_test(sWorkspace_output) == 0)
          {
            make_directory(sWorkspace_output);
          }
        sWorkspace_output = sWorkspace_output + slash + "case" + convert_integer_to_string(iCase);
        if (path_test(sWorkspace_output) == 0)
          {
            make_directory(sWorkspace_output);
          }
      }
    else
      {
        sWorkspace_output = sWorkspace_data + slash + "output";
        if (path_test(sWorkspace_output) == 0)
          {
            make_directory(sWorkspace_output);
          }
      }
    //point
    sFilename_flow_accumulation_point = sWorkspace_output + slash + "flow_accumulation_point.shp";
    sFilename_flow_accumulation_point_debug = sWorkspace_output + slash + "flow_accumulation_point_debug.shp";
    sFilename_stream_grid_point = sWorkspace_output + slash + "stream_grid.shp";

    sFilename_stream_grid_point_debug = sWorkspace_output + slash + "stream_grid_debug.shp";
    sFilename_watershed_point = sWorkspace_output + slash + "watershed_point.shp";
    sFilename_stream_segment_point = sWorkspace_output + slash + "stream_segment_point.shp";
    sFilename_subbasin_point = sWorkspace_output + slash + "subbasin_point.shp";
    sFilename_stream_confluence_point = sWorkspace_output + slash + "stream_confluence.shp";
    sFilename_wetness_index_point = sWorkspace_output + slash + "wetness_index_point.shp";
    //polygon
    sFilename_elevation_polygon = sWorkspace_output + slash + "elevation_polygon.shp";
    sFilename_elevation_polygon_debug = sWorkspace_output + slash + "elevation_polygon_debug.shp";

    sFilename_flow_accumulation_polygon = sWorkspace_output + slash + "flow_accumulation_polygon.shp";
    sFilename_flow_accumulation_polygon_debug = sWorkspace_output + slash + "flow_accumulation_polygon_debug.shp";
    sFilename_watershed_polygon = sWorkspace_output + slash + "watershed_polygon.shp";
    sFilename_stream_confluence_polygon = sWorkspace_output + slash + "stream_confluence_polygon.shp";
    sFilename_stream_segment_polygon = sWorkspace_output + slash + "stream_segment_polygon.shp";
    sFilename_subbasin_polygon = sWorkspace_output + slash + "subbasin_polygon.shp";
    sFilename_wetness_index_polygon = sWorkspace_output + slash + "wetness_index_polygon.shp";
    // polyline
    sFilename_flow_direction_polyline = sWorkspace_output + slash + "flow_direction.shp";

    sFilename_flow_direction_polyline_debug = sWorkspace_output + slash + "flow_direction_debug.shp";
    sFilename_stream_order_polyline = sWorkspace_output + slash + "stream_order.shp";
    sFilename_stream_segment_polyline = sWorkspace_output + slash + "stream_segment_polyline.shp";
    sFilename_stream_segment_merge_polyline = sWorkspace_output + slash + "stream_segment_merge_polyline.shp";

    //others

    sFilename_watershed_characteristics = sWorkspace_output + slash + "watershed_characteristics" + sExtension_text;

    sFilename_log = sWorkspace_output + slash + "starlog" + sExtension_text;
    this->ofs_log.open(this->sFilename_log.c_str(), ios::out);

    sLog = "=Level 1: Simulation log will be save to log file: " +
      this->sFilename_log;
    ofs_log << sLog << std::endl;
    return error_code;
  }

  /**
   * read the cell information from input data
   * @param sFilename_hexagon_point_shapefile_in: the point based shapefile
   * @param sFilename_hexagon_polygon_shapefile_in : the polygon based shapefile
   * @param sFilename_elevation_in :the digital elevation model file
   * @return
   */
  int domain::domain_read_all_cell_information(std::string sFilename_hexagon_point_shapefile_in,
                                               std::string sFilename_hexagon_polygon_shapefile_in,
                                               std::string sFilename_elevation_in)
  {
    int error_code;
    unsigned long lRecord;
    unsigned long lIndex;
    unsigned long lColumn_index, lRow_index;
    double dDummy1, dDummy2;
    double dX_dummy, dY_dummy;

    std::vector<hexagon>::iterator iIterator;
    //first read all the hexagon

    error_code = read_hexagon_polygon_shapefile(sFilename_hexagon_polygon_shapefile_in);
    if (error_code != 0)
      {
        //point feature is not required
        if (iFlag_hexagon_point == 1)
          {
            read_hexagon_point_shapefile(std::move(sFilename_hexagon_point_shapefile_in));
          }
        else
          {
            //each polygon should have 5/6 vextex
            //now we will calculate point location based on polygon location
            domain_calculate_hexagon_polygon_center_location();
          }

        //second read the dem data as a matrix
        read_digital_elevation_model(std::move(sFilename_elevation_in));

        //third assign elevation for hexagon
        //get elevation for each point
        //#pragma omp parallel for private(lRecord, dX_dummy, dY_dummy, \
        //                              lColumn_index,lRow_index,  dDummy1, dDummy2, lIndex)
        for (lRecord = 0; lRecord < nRecord_shapefile; lRecord++)
          {
            dX_dummy = vCell.at(lRecord).dX;
            dY_dummy = vCell.at(lRecord).dY;

            //calculate location

            dDummy1 = (dX_dummy - dX_origin) / dResolution_elevation;
            lColumn_index = long(round(dDummy1));

            dDummy2 = (dY_origin - dY_dummy) / dResolution_elevation;
            lRow_index = long(round(dDummy2));

            if (lColumn_index >= 0 && lColumn_index < nColumn_elevation && lRow_index >= 0 && lRow_index < nRow_elevation)
              //if (dDummy1 >= 0 && dDummy1 < nColumn_elevation && dDummy2 >= 0 && dDummy2 < nRow_elevation)
              {
                //within the range
                lColumn_index = lround(dDummy1);
                lRow_index = lround(dDummy2);
                lIndex = lRow_index * nColumn_elevation + lColumn_index;
                if (vElevation.at(lIndex) == missing_value)
                  {
                    vCell.at(lRecord).dElevation = missing_value;
                    vCell.at(lRecord).iFlag_active = 0;
                  }
                else
                  {
                    vCell.at(lRecord).dElevation = vElevation.at(lIndex);
                    vCell.at(lRecord).iFlag_active = 1;
                  }
              }
            else
              {
                //out of bound
                vCell.at(lRecord).dElevation = missing_value;
                vCell.at(lRecord).iFlag_active = 0;
              }
          }
        //setup the local index starting from 0
        lIndex = 0;
        for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
          {
            if ((*iIterator).iFlag_active == 1)
              {
                (*iIterator).lID = lIndex;
                vCell_active.push_back(*iIterator);
                lIndex = lIndex + 1;
              }
            else
              {
                /* code */
              }
          }
      }
    else
      {
        //failed reading
      }

    return error_code;
  }

  /**
   * calculate the center location of a hexagon using 6 vertex
   * @return
   */
  int domain::domain_calculate_hexagon_polygon_center_location()
  {
    int error_code = 1;
    int nPt;
    int i;
    double dX, dY;
    std::vector<double> vX;
    std::vector<double> vY;
    std::vector<hexagon>::iterator iIterator;

    for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
      {
        nPt = (*iIterator).nPtVertex;
        vX.clear();
        vY.clear();
        for (i = 0; i < nPt; i++)
          {
            dX = (*iIterator).vPtVertex.at(i).dX;
            dY = (*iIterator).vPtVertex.at(i).dY;
            vX.push_back(dX);
            vY.push_back(dY);
          }

        (*iIterator).dX = (std::accumulate(vX.begin(), vX.end(), 0.0)) / nPt;

        (*iIterator).dY = (std::accumulate(vY.begin(), vY.end(), 0.0)) / nPt;
      }

    return error_code;
  }

  /**
   * read the elevation file
   * @param sFilename_elevation_in
   * @return
   */
  int domain::read_digital_elevation_model(std::string sFilename_elevation_in)
  {
    int error_code = 1;
    int nXSize;
    int nYSize;
    int nBlockXSize;
    int nBlockYSize;
    int bGotMin;
    int bGotMax;
    float *pData;
    double adfMinMax[2];
    double adfGeoTransform[6];
    GDALAllRegister();
    GDALRasterBand *poBand;
    GDALDataset *poDS_elevation;

    poDS_elevation = (GDALDataset *)GDALOpen(sFilename_elevation_in.c_str(),
                                             GA_ReadOnly);
    if (poDS_elevation == NULL)
      {
        printf("Open failed.\n");
        error_code = 0;
      }
    else
      {

        printf("Driver: %s/%s\n",
               poDS_elevation->GetDriver()->GetDescription(),
               poDS_elevation->GetDriver()->GetMetadataItem(GDAL_DMD_LONGNAME));
        printf("Size is %dx%dx%d\n",
               poDS_elevation->GetRasterXSize(), poDS_elevation->GetRasterYSize(),
               poDS_elevation->GetRasterCount());
        if (poDS_elevation->GetProjectionRef() != NULL)
          {
            printf("Projection is `%s'\n", poDS_elevation->GetProjectionRef());
          }
        if (poDS_elevation->GetGeoTransform(adfGeoTransform) == CE_None)
          {
            printf("Origin = (%.6f,%.6f)\n",
                   adfGeoTransform[0], adfGeoTransform[3]);
            printf("Pixel Size = (%.6f,%.6f)\n",
                   adfGeoTransform[1], adfGeoTransform[5]);

            this->dX_origin = adfGeoTransform[0];
            this->dY_origin = adfGeoTransform[3];
            this->dResolution_elevation = adfGeoTransform[1];
          }
        poBand = poDS_elevation->GetRasterBand(1);
        poBand->GetBlockSize(&nBlockXSize, &nBlockYSize);
        printf("Block=%dx%d Type=%s, ColorInterp=%s\n",
               nBlockXSize, nBlockYSize,
               GDALGetDataTypeName(poBand->GetRasterDataType()),
               GDALGetColorInterpretationName(
                                              poBand->GetColorInterpretation()));
        adfMinMax[0] = poBand->GetMinimum(&bGotMin);
        adfMinMax[1] = poBand->GetMaximum(&bGotMax);
        if (!(bGotMin && bGotMax))
          GDALComputeRasterMinMax((GDALRasterBandH)poBand, TRUE, adfMinMax);
        printf("Min=%.3fd, Max=%.3f\n", adfMinMax[0], adfMinMax[1]);
        if (poBand->GetOverviewCount() > 0)
          printf("Band has %d overviews.\n", poBand->GetOverviewCount());
        if (poBand->GetColorTable() != NULL)
          printf("Band has a color table with %d entries.\n",
                 poBand->GetColorTable()->GetColorEntryCount());

        nXSize = poBand->GetXSize();
        nYSize = poBand->GetYSize();

        this->nColumn_elevation = nXSize;
        this->nRow_elevation = nYSize;

        pData = (float *)CPLMalloc(sizeof(float) * nXSize * nYSize);

        auto dummy = poBand->RasterIO(GF_Read,
                                      0, 0, nXSize, nYSize,
                                      pData, nXSize, nYSize,
                                      GDT_Float32,
                                      0, 0);
        //convert to vector
        std::vector<float> vDummy(pData, pData + (nXSize * nYSize));

        vElevation = vDummy;

        GDALClose(poDS_elevation);
      }

    missing_value = *(std::min_element(std::begin(vElevation), std::end(vElevation)));

    return error_code;
  }

  /**
   * read the polygon shapefile
   * @param sFilename_hexagon_polygon_shapefile_in :the filename of the polygon shapefile
   * @return
   */
  int domain::read_hexagon_polygon_shapefile(std::string sFilename_hexagon_polygon_shapefile_in)
  {
    int error_code = 1;
    int nVertex;
    long lCellID = 0;
    long lGlobalID; //global id start from 1
    double dX1, dY1;
    double dX2, dY2;
    double dLength;

    GDALAllRegister();
    GDALDataset *poDS_shapefile;
    OGRLayer *poLayer;
    OGRFeatureDefn *poFDefn;
    OGRFeature *poFeature;
    OGRFieldDefn *poFieldDefn;
    OGRGeometry *poGeometry;
    OGRPolygon *poPolygon;
    OGRPoint ptTemp;
    OGRLinearRing *poExteriorRing;
    poDS_shapefile = (GDALDataset *)GDALOpenEx(sFilename_hexagon_polygon_shapefile_in.c_str(),
                                               GDAL_OF_VECTOR,
                                               NULL, NULL, NULL);
    if (poDS_shapefile == NULL)
      {
        printf("Open failed.\n");
        error_code = 0;
      }
    else
      {
        poDS_shapefile->GetLayerCount();
        poLayer = poDS_shapefile->GetLayer(0);
        poLayer->ResetReading();
        poFDefn = poLayer->GetLayerDefn();

        //use polygon srs to define output
        oSRS = poLayer->GetSpatialRef();

        std::cout << (oSRS) << std::endl;

        char *pszWKT = NULL;

        oSRS->exportToWkt(&pszWKT);
        printf("%s\n", pszWKT);

        while ((poFeature = poLayer->GetNextFeature()) != NULL)
          {
            //define global id

            poGeometry = poFeature->GetGeometryRef();
            if (poGeometry != NULL)
              {
                if (wkbFlatten(poGeometry->getGeometryType()) == wkbPolygon)
                  {
                    hexagon cCell;
                    lGlobalID = lCellID + 1;
                    cCell.lGlobalID = lGlobalID; //global id is the same with field id.
                    //OGRFeature *poFeature;
                    poPolygon = (OGRPolygon *)poGeometry;

                    poExteriorRing = poPolygon->getExteriorRing();
                    nVertex = poExteriorRing->getNumPoints();
                    for (int k = 0; k < nVertex - 1; k++)
                      {
                        ptVertex pt;
                        poExteriorRing->getPoint(k, &ptTemp);
                        pt.dX = ptTemp.getX();
                        pt.dY = ptTemp.getY();
                        cCell.vPtVertex.push_back(pt);
                      }
                    //calculate mean edge length, in the future, if the mesh is adaptive resolution,
                    //we need a different algorithm
                    dLength = 0.0;
                    for (int k = 0; k < nVertex - 1; k++)
                      {
                        dX1 = cCell.vPtVertex.at(k).dX;
                        dY1 = cCell.vPtVertex.at(k).dY;
                        if (k != (nVertex - 2))
                          {
                            dX2 = cCell.vPtVertex.at(k + 1).dX;
                            dY2 = cCell.vPtVertex.at(k + 1).dY;
                          }
                        else
                          {
                            dX2 = cCell.vPtVertex.at(0).dX;
                            dY2 = cCell.vPtVertex.at(0).dY;
                          }

                        dLength = dLength + sqrt((dX1 - dX2) * (dX1 - dX2) + (dY1 - dY2) * (dY1 - dY2));
                      }
                    dLength = dLength / (nVertex - 1);

                    cCell.nPtVertex = nVertex - 1;
                    cCell.dLength_edge = dLength;
                    vCell.push_back(cCell);

                    lCellID = lCellID + 1;
                  }
              }

            else
              {
                printf("no polygon geometry\n");
              }
          }
        nRecord_shapefile = lCellID;
      }
    return error_code;
  }

  /**
   * read point based shapefile information if available
   * @param sFilename_hexagon_point_shapefile_in :filename of the point shapefile
   * @return
   */
  int domain::read_hexagon_point_shapefile(std::string sFilename_hexagon_point_shapefile_in)
  {
    int error_code = 1;
    int nField;
    long lCellID = 0;
    long lGlobalID;
    GDALAllRegister();
    GDALDataset *poDS_shapefile;
    OGRLayer *poLayer;
    OGRFeatureDefn *poFDefn;
    OGRFeature *poFeature;
    OGRFieldDefn *poFieldDefn;

    poDS_shapefile = (GDALDataset *)GDALOpenEx(sFilename_hexagon_point_shapefile_in.c_str(),
                                               GDAL_OF_VECTOR,
                                               NULL, NULL, NULL);
    if (poDS_shapefile == NULL)
      {
        printf("Open failed.\n");
        error_code = 0;
      }
    else
      {
        poDS_shapefile->GetLayerCount();
        poLayer = poDS_shapefile->GetLayer(0);

        poLayer->ResetReading();
        poFDefn = poLayer->GetLayerDefn();
        nField = poFDefn->GetFieldCount();
        while ((poFeature = poLayer->GetNextFeature()) != NULL)
          {

            //hexagon cCell;
            lGlobalID = lCellID + 1;
            vCell[lCellID].lGlobalID = lGlobalID;
            for (int iField = 0; iField < nField; iField++)
              {
                switch (iField)
                  {
                  case 0:

                    break;
                  case 1:
                    vCell[lCellID].dX = poFeature->GetFieldAsDouble(iField);
                    break;
                  case 2:
                    vCell[lCellID].dY = poFeature->GetFieldAsDouble(iField);
                    break;
                  default:
                    break;
                  }
              }

            lCellID = lCellID + 1;
          }
      }

    return error_code;
  }

  /**
   * initialize the model
   * @return
   */
  int domain::domain_initialize_model()
  {
    int error_code = 1;
    std::cout << "Finished initialization!" << std::endl;
    std::flush(std::cout);
    return error_code;
  }

  /**
   * run the model
   * @return
   */
  int domain::domain_run_model()
  {
    int error_code = 1;
    iFlag_debug = 1;
    domain_fill_depression();
    sLog = "Finished depression filling";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_elevation);
    std::flush(std::cout);

    domain_calculate_flow_direction();
    sLog = "Finished flow direction";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_flow_direction);
    std::flush(std::cout);

    domain_calculate_flow_accumulation();
    sLog = "Finished flow accumulation";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_flow_accumulation);
    std::flush(std::cout);

    domain_define_stream_grid();
    sLog = "Finished defining stream grid";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;

    std::flush(std::cout);

    //starting from here, use the watershed boundary
    iFlag_debug = 0;
    domain_define_watershed_boundary();
    sLog = "Finished defining watershed boundary";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;

    domain_save_variable(eV_watershed);
    std::flush(std::cout);

    domain_define_stream_confluence();
    sLog = "Finished defining confluence";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_confluence);
    std::flush(std::cout);

    domain_define_stream_segment();
    sLog = "Finished defining stream segment";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_segment);
    std::flush(std::cout);

    domain_build_stream_topology();
    sLog = "Finished defining stream topology";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    std::flush(std::cout);

    domain_define_stream_order();
    sLog = "Finished defining stream order";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_stream_order);
    std::flush(std::cout);

    domain_define_subbasin();
    sLog = "Finished defining subbasin";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    domain_save_variable(eV_subbasin);
    std::flush(std::cout);

    domain_calculate_watershed_characteristics();
    sLog = "Finished watershed characteristics";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    std::flush(std::cout);
    return error_code;
  }

  /**
   * DEM depression filling
   * @return
   */
  int domain::domain_fill_depression()
  {
    int error_code = 1;
    int iFlag_finished = 0;
    long lIndex_lowest;
    long lIndex_active;
    long lIndex_neighbor;
    long iAttemp = 0;
    double dElevation_center;
    double dElevation_neighbor;

    std::vector<int> vFlag(vCell_active.size());
    std::array<long, 3> aIndex;
    std::vector<hexagon>::iterator iIterator;

    std::fill(vFlag.begin(), vFlag.end(), 0);
    std::vector<hexagon> vCell_boundary;
    //find all the neighbors first

    find_all_neighbors();

    iFlag_finished = check_digital_elevation_model_depression(vCell_active);
    if (iFlag_finished == 1)
      {
        //there is no depression at all
      }
    else
      {
        vCell_boundary = domain_get_boundary(vCell_active);
        //set initial as true for boundary
        for (iIterator = vCell_boundary.begin(); iIterator != vCell_boundary.end(); iIterator++)
          {
            vFlag.at((*iIterator).lID) = 1;
          }

        while (!vCell_boundary.empty())
          {
            aIndex = find_lowest_cell(vCell_boundary);
            lIndex_lowest = aIndex[0];
            lIndex_active = aIndex[1];
            dElevation_center = vCell_active.at(lIndex_active).dElevation;
            vCell_boundary.erase(vCell_boundary.begin() + lIndex_lowest);
            //set flag

            vFlag.at(lIndex_active) = 1;
            //loop through
            for (int i = 0; i < vCell_active.at(lIndex_active).nNeighbor; i++)
              {
                lIndex_neighbor = vCell_active.at(lIndex_active).vNeighbor[i];
                if (vFlag[lIndex_neighbor] == 1)
                  {
                    //already removed?
                  }
                else
                  {
                    dElevation_neighbor = vCell_active[lIndex_neighbor].dElevation;
                    if (dElevation_neighbor <= dElevation_center)
                      {
                        vCell_active[lIndex_neighbor].dElevation = dElevation_center + 0.001 + abs(dElevation_center) * 0.0001; //add some difference
                        iAttemp = iAttemp + 1;
                      }
                    else
                      {
                      }
                    vFlag[lIndex_neighbor] = 1;
                    //push on to queue
                    vCell_boundary.push_back(vCell_active[lIndex_neighbor]);
                  }
              }
          }
        //recheck !!!

        iFlag_finished = check_digital_elevation_model_depression(vCell_active);

        if (iFlag_finished != 1)
          {
            //something is wrong
          }
      }
    return error_code;
  }

  /**
   * calculate the flow direction based on elevation, this step "should" only be run after the depression filling
   * @return
   */
  int domain::domain_calculate_flow_direction()
  {
    int error_code = 1;
    long lIndex_lowest;
    long lIndex_self;
    double dElevation;
    double dDifference;
    double dDifference_new;

    std::vector<long>::iterator iIterator_neighbor;
    std::vector<long> vNeighbor;

#pragma omp parallel for private(lIndex_self, vNeighbor, lIndex_lowest, dElevation, dDifference, dDifference_new, iIterator_neighbor)
    for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
      {
        vNeighbor = (vCell_active.at(lIndex_self)).vNeighbor;
        lIndex_lowest = -1;
        dElevation = (vCell_active.at(lIndex_self)).dElevation;
        dDifference = 0.0;

        //iterate through all neighbors
        for (iIterator_neighbor = vNeighbor.begin(); iIterator_neighbor < vNeighbor.end(); iIterator_neighbor++)
          {
            dDifference_new = vCell_active.at(*iIterator_neighbor).dElevation - dElevation;

            if (dDifference_new < dDifference)
              {
                dDifference = dDifference_new;
                lIndex_lowest = *iIterator_neighbor;
              }
          }

        //mark the direction as the largest elevation differences
        if (lIndex_lowest != -1)
          {
            (vCell_active.at(lIndex_self)).lIndex_downslope = lIndex_lowest;
            //before define stream, we cannot establish upslope relationship
            //calculate slope
            if (dDifference > 0.0)
              {
                std::cout << "Slope should be positive!" << std::endl;
              }
            (vCell_active.at(lIndex_self)).dSlope = -dDifference / ((vCell_active.at(lIndex_self)).dLength_edge * sqrt(3.0));
          }
      }
    return error_code;
  }

  /**
   * calculate the flow accumulation based on flow direction
   * @return
   */
  int domain::domain_calculate_flow_accumulation()
  {
    int error_code = 1;
    int iFlag_has_upslope = 0;
    int iFlag_all_upslope_done; //assume all are done
    long lFlag_total = 0;
    long lIndex_neighbor;
    long lIndex_downslope_neighbor;

    std::vector<hexagon>::iterator iIterator_self;
    std::vector<long>::iterator iIterator_neighbor;
    std::vector<int> vFlag(vCell_active.size());
    std::vector<int> vFinished(vCell_active.size());
    std::fill(vFlag.begin(), vFlag.end(), 0);
    std::fill(vFinished.begin(), vFinished.end(), 0);

    //the initial run

    lFlag_total = std::accumulate(vFlag.begin(), vFlag.end(), 0);

    while (lFlag_total != vCell_active.size())
      {
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {

            if (vFlag.at((*iIterator_self).lID) == 1)
              {
                //this hexagon is finished
                continue;
              }
            else
              {
                //check whether one or more of the neighbors flow to itself
                iFlag_has_upslope = 0;
                iFlag_all_upslope_done = 1;
                for (int i = 0; i < (*iIterator_self).nNeighbor; i++)
                  {
                    lIndex_neighbor = (*iIterator_self).vNeighbor.at(i);
                    lIndex_downslope_neighbor = (vCell_active.at(lIndex_neighbor)).lIndex_downslope;

                    if (lIndex_downslope_neighbor == (*iIterator_self).lID)
                      {
                        //there is one upslope neighbor found
                        iFlag_has_upslope = 1;
                        if (vFlag.at(lIndex_neighbor) == 1)
                          {
                            //std::cout << "==" << lIndex_neighbor << std::endl;
                          }
                        else
                          {
                            iFlag_all_upslope_done = 0;
                          }
                      }
                    else
                      {
                      }
                  }
                //std::cout << "has upslope: " << iFlag_has_upslope << std::endl;
                //std::cout << "upslope done:" << iFlag_all_upslope_done << std::endl;
                //there are the ones have no upslope at all
                if (iFlag_has_upslope == 0)
                  {
                    vFlag.at((*iIterator_self).lID) = 1;
                  }
                else
                  {
                    //these ones have upslope,
                    if (iFlag_all_upslope_done == 1)
                      {
                        //and they are finished scanning
                        for (int i = 0; i < (*iIterator_self).nNeighbor; i++)
                          {
                            lIndex_neighbor = (*iIterator_self).vNeighbor.at(i);

                            lIndex_downslope_neighbor = (vCell_active.at(lIndex_neighbor)).lIndex_downslope;

                            if (lIndex_downslope_neighbor == (*iIterator_self).lID)
                              {
                                //std::cout << "===" << lIndex_neighbor << std::endl;
                                //std::cout << "====" << lIndex_downslope_neighbor << std::endl;
                                //this one accepts upslope and the upslope is done
                                (*iIterator_self).lAccumulation =
                                  (*iIterator_self).lAccumulation + 1 + vCell_active.at(lIndex_neighbor).lAccumulation;
                              }
                            else
                              {
                                //this neighbor does not flow here, sorry
                              }
                          }
                        //now this one is also done
                        //std::cout << "======" << (*iIterator_self).lAccumulation << std::endl;
                        vFlag.at((*iIterator_self).lID) = 1;
                      }
                    else
                      {
                        //we have wait temporally
                      }
                  }
              }
          }
        lFlag_total = std::accumulate(vFlag.begin(), vFlag.end(), 0);
      }
    return error_code;
  }

  /**
   * define the stream network using flow accumulation value
   * @return
   */
  int domain::domain_define_stream_grid()
  {
    int error_code = 1;
    long lIndex_self;
    //in watershed hydrology, a threshold is usually used to define the network
    //here we use similar method
    long lAccumulation_threshold;
    std::vector<hexagon>::iterator iIterator_self;

    lAccumulation_threshold = long(dAccumulation_threshold);

#pragma omp parallel for private(lIndex_self)
    for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
      {
        if ((vCell_active.at(lIndex_self)).lAccumulation >= lAccumulation_threshold)
          {
            (vCell_active.at(lIndex_self)).iFlag_stream = 1;
          }
        else
          {
            (vCell_active.at(lIndex_self)).iFlag_stream = 0;
          }
      }

    return error_code;
  }

  /**
   * define the watershed boundary using outlet
   * @return
   */
  int domain::domain_define_watershed_boundary()
  {
    int error_code = 1;
    int iFound_outlet;

    long iIndex_out;
    long lIndex_self, lIndex_current;
    long lIndex_downslope;
    std::vector<long> vAccumulation;
    std::vector<long>::iterator iterator_long;
    std::vector<hexagon>::iterator iIterator_self;
    std::vector<hexagon>::iterator iIterator_current;
    iIndex_out = -1;

    //find the max accumulation outlet

    for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
      {
        vAccumulation.push_back((*iIterator_self).lAccumulation);
      }
    iterator_long = max_element(std::begin(vAccumulation), std::end(vAccumulation)); // c++11
    iIndex_out = std::distance(vAccumulation.begin(), iterator_long);
    vAccumulation.clear();
    lOutlet = iIndex_out;

#pragma omp parallel for private(lIndex_self, iFound_outlet, lIndex_downslope, lIndex_current)
    for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
      {
        iFound_outlet = 0;
        lIndex_current = lIndex_self;
        while (iFound_outlet != 1)
          {
            lIndex_downslope = (vCell_active.at(lIndex_current)).lIndex_downslope;
            if (iIndex_out == lIndex_downslope)
              {
                iFound_outlet = 1;
                (vCell_active.at(lIndex_self)).iFlag_watershed = 1;
              }
            else
              {
                //iIterator_current = vCell_active.begin() + lIndex_downslope;
                lIndex_current = lIndex_downslope;
                if (lIndex_current == -1)
                  {
                    //this one is going out, but it is not the one belong in this watershed
                    iFound_outlet = 1;
                    (vCell_active.at(lIndex_self)).iFlag_watershed = 0;
                  }
              }
          }
      }

    return error_code;
  }
  /**
   * define the stream confluence point
   * @return
   */
  int domain::domain_define_stream_confluence()
  {
    int error_code = 1;
    int iCount = 0;
    long lIndex_downstream;
    std::vector<hexagon>::iterator iIterator_self;

    for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
      {
        if ((*iIterator_self).iFlag_stream == 1 && (*iIterator_self).iFlag_watershed == 1)
          {
            lIndex_downstream = (*iIterator_self).lIndex_downslope;

            (vCell_active.at(lIndex_downstream)).vUpslope.push_back((*iIterator_self).lID);
          }
      }
    //calculate the size the upslope
    for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
      {
        (*iIterator_self).nUpslope = ((*iIterator_self).vUpslope).size();
      }
    //calculate total segment
    for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
      {
        if ((*iIterator_self).nUpslope > 1 && (*iIterator_self).iFlag_watershed == 1 && (*iIterator_self).iFlag_stream == 1)
          {
            iCount = iCount + 1;

            (*iIterator_self).iFlag_confluence = 1;

            vConfluence.push_back((*iIterator_self));
          }
      }
    nSegment = 1;
    for (iIterator_self = vConfluence.begin(); iIterator_self < vConfluence.end(); iIterator_self++)
      {
        nSegment = nSegment + (*iIterator_self).vUpslope.size();
      }

    //sort cannot be used directly here

    return error_code;
  }
  /**
   * define the stream segment
   * @return
   */
  int domain::domain_define_stream_segment()
  {
    int error_code = 1;
    int iFlag_confluence = 0;
    int iUpslope;
    long lID_current = vCell_active.at(lOutlet).lID;

    vCell_active.at(lOutlet).iFlag_last_reach = 1;
    iSegment_current = nSegment;
    segment cSegment;
    std::vector<hexagon> vReach_segment;

    vReach_segment.push_back(vCell_active.at(lOutlet));

    while (iFlag_confluence != 1)
      {
        iUpslope = vCell_active.at(lID_current).nUpslope;
        if (iUpslope == 1)
          {
            lID_current = (vCell_active.at(lID_current)).vUpslope[0];

            vCell_active.at(lID_current).iSegment = iSegment_current;

            vReach_segment.push_back(vCell_active.at(lID_current));
          }
        else
          {
            vCell_active.at(lID_current).iSegment = iSegment_current;
            vCell_active.at(lID_current).iFlag_first_reach = 1;
            vReach_segment.push_back(vCell_active.at(lID_current));
            iFlag_confluence = 1;
          }
      }
    //this is the last segment of watershed
    std::reverse(vReach_segment.begin(), vReach_segment.end());
    cSegment.vReach_segment = vReach_segment;
    cSegment.nReach = vReach_segment.size();
    cSegment.cReach_start = vReach_segment.front();
    cSegment.cReach_end = vReach_segment.back();
    cSegment.iSegment = nSegment;
    cSegment.nSegment_upstream = 2;
    cSegment.iFlag_has_upstream = 1;
    cSegment.iFlag_has_downstream = 0;
    if (cSegment.cReach_start.iFlag_headwater == 1)
      {
        cSegment.iFlag_headwater = 1;
      }
    vSegment.push_back(cSegment);
    //std::cout << iSegment_current << std::endl;
    iSegment_current = iSegment_current - 1;

    domain_tag_confluence_upstream(lID_current);

    //in fact the segment is ordered by default already

    std::sort(vSegment.begin(), vSegment.end());

    return error_code;
  }
  /**
   * build the stream topology based on stream segment information
   * @return
   */
  int domain::domain_build_stream_topology()
  {
    int error_code = 1;
    int iSegment;
    //rebuild stream topology
    std::vector<segment>::iterator iIterator_segment_self;
    std::vector<segment>::iterator iIterator_segment;
    for (iIterator_segment_self = vSegment.begin(); iIterator_segment_self < vSegment.end(); iIterator_segment_self++)
      {
        iSegment = (*iIterator_segment_self).iSegment_downstream;
        for (iIterator_segment = vSegment.begin(); iIterator_segment < vSegment.end(); iIterator_segment++)
          {
            if (iSegment == (*iIterator_segment).iSegment)
              {
                (*iIterator_segment).vSegment_upstream.push_back((*iIterator_segment_self).iSegment);
              }
          }
      }
    for (iIterator_segment = vSegment.begin(); iIterator_segment < vSegment.end(); iIterator_segment++)
      {
        (*iIterator_segment).nSegment_upstream = (*iIterator_segment).vSegment_upstream.size();
      }

    return error_code;
  }
  /**
   * build the stream order based on stream topology
   * @return
   */
  int domain::domain_define_stream_order()
  {
    int error_code = 1;
    int iSegment;
    int iUpstream;
    int iStream_order_max;
    int iFlag_all_upstream_done;

    std::vector<int> vStream_order;
    std::vector<hexagon>::iterator iIterator_hexagon;
    std::vector<segment>::iterator iIterator_segment;

    for (iIterator_segment = vSegment.begin(); iIterator_segment < vSegment.end(); iIterator_segment++)
      {
        if ((*iIterator_segment).iFlag_headwater == 1)
          {
            (*iIterator_segment).iSegment_order = 1;
          }
      }

    while (vSegment.back().iSegment_order == -1)
      {
        for (iIterator_segment = vSegment.begin(); iIterator_segment < vSegment.end(); iIterator_segment++)
          {

            if ((*iIterator_segment).iSegment_order == -1)
              {
                iFlag_all_upstream_done = 1;
                vStream_order.clear();
                for (iUpstream = 0; iUpstream < (*iIterator_segment).nSegment_upstream; iUpstream++)
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
   * find the confluence recursively from existing confluence point.
   * @param lID_confluence
   * @return
   */
  int domain::domain_tag_confluence_upstream(long lID_confluence)
  {
    int error_code = 1;

    int nUpslope;
    int iFlag_first_reach;
    int iFlag_confluence;
    int iSegment_confluence;
    long lUpslope;
    std::vector<long> vUpslope;
    std::vector<long>::iterator iterator_upslope;
    segment cSegment;
    std::vector<hexagon> vReach_segment;

    vUpslope = (vCell_active.at(lID_confluence)).vUpslope;
    iSegment_confluence = (vCell_active.at(lID_confluence)).iSegment;

    for (iterator_upslope = vUpslope.begin();
         iterator_upslope < vUpslope.end();
         iterator_upslope++)
      {
        lUpslope = *iterator_upslope;
        iFlag_first_reach = 0;
        iFlag_confluence = vCell_active.at(lUpslope).iFlag_confluence;

        vCell_active.at(lUpslope).iFlag_last_reach = 1;
        //use last reach to find next stream segment

        vCell_active.at(lUpslope).iSegment_downstream = vCell_active.at(lID_confluence).iSegment;

        vReach_segment.clear();
        vReach_segment.push_back(vCell_active.at(lUpslope));
        while (iFlag_confluence != 1)
          {
            //it has only one upslope
            nUpslope = (vCell_active.at(lUpslope)).nUpslope;
            vCell_active.at(lUpslope).iSegment = iSegment_current;
            if (nUpslope == 0)
              {
                //this is the headwater
                iFlag_first_reach = 1;
                (vCell_active.at(lUpslope)).iFlag_first_reach = 1;
                (vCell_active.at(lUpslope)).iFlag_headwater = 1;
                break;
              }
            else
              {
                //we are on the stream segment and there is only one upstream
                lUpslope = (vCell_active.at(lUpslope)).vUpslope[0];
                iFlag_confluence = vCell_active.at(lUpslope).iFlag_confluence;

                vReach_segment.push_back(vCell_active.at(lUpslope));
              }
          }
        //now we find the next confluence
        vCell_active.at(lUpslope).iSegment = iSegment_current;
        //std::cout << iSegment_current << std::endl;

        vCell_active.at(lUpslope).iFlag_first_reach = 1;

        //the headwater reach is actually the last one added into the vector
        vReach_segment.back().iFlag_first_reach = 1;
        if (iFlag_first_reach == 1)
          {
            vReach_segment.back().iFlag_headwater = 1;
            cSegment.iFlag_has_upstream = 0;
            cSegment.iFlag_headwater = 1;
          }
        else
          {
            cSegment.iFlag_has_upstream = 1;
            cSegment.iFlag_headwater = 0;
          }

        std::reverse(vReach_segment.begin(), vReach_segment.end());
        cSegment.vReach_segment = vReach_segment;
        cSegment.nReach = vReach_segment.size();
        cSegment.cReach_start = vReach_segment.front();
        cSegment.cReach_end = vReach_segment.back();
        cSegment.iSegment = iSegment_current;
        cSegment.iFlag_has_downstream = 1;
        cSegment.iSegment_downstream = iSegment_confluence;
        vSegment.push_back(cSegment);
        iSegment_current = iSegment_current - 1;

        if (iFlag_first_reach != 1)
          {
            domain_tag_confluence_upstream(lUpslope);
          }
      }

    return error_code;
  }

  /**
   * define subbasin boundary
   * @return
   */
  int domain::domain_define_subbasin()
  {
    int error_code = 1;
    int iFound_outlet;
    int iSubbasin;
    long lIndex_outlet;
    long lIndex_downslope;
    long lAccumulation;
    std::vector<long> vAccumulation;
    std::vector<long>::iterator iterator_accumulation;
    std::vector<hexagon> vConfluence_copy(vConfluence);
    std::vector<hexagon>::iterator iIterator_self;
    std::vector<long>::iterator iIterator_upslope;
    std::vector<hexagon>::iterator iIterator_current;

    //the whole watershed first
    for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
      {
        if ((*iIterator_self).iFlag_watershed == 1)
          {
            (*iIterator_self).iSubbasin = nSegment;
          }
      }

    for (iIterator_self = vConfluence.begin(); iIterator_self < vConfluence.end(); iIterator_self++)
      {
        vAccumulation.push_back((*iIterator_self).lAccumulation);
      }
    //now starting from the confluences loop

    while (vConfluence_copy.size() != 0)
      {
        iterator_accumulation = max_element(std::begin(vAccumulation), std::end(vAccumulation));
        lAccumulation = std::distance(vAccumulation.begin(), iterator_accumulation);

        //nUpslope = (vConfluence_copy.at(lAccumulation)).nUpslope;

        std::vector<long> vUpslope((vConfluence_copy.at(lAccumulation)).vUpslope);

        for (iIterator_upslope = vUpslope.begin(); iIterator_upslope < vUpslope.end(); iIterator_upslope++)
          {
            //use the watershed method again here

            lIndex_outlet = *iIterator_upslope;
            iSubbasin = (vCell_active.at(lIndex_outlet)).iSegment;
            (vCell_active.at(lIndex_outlet)).iSubbasin = iSubbasin;

            for (iIterator_self = vCell_active.begin(); iIterator_self < vCell_active.end(); iIterator_self++)
              {
                iFound_outlet = 0;
                iIterator_current = iIterator_self;
                while (iFound_outlet != 1)
                  {
                    lIndex_downslope = (*iIterator_current).lIndex_downslope;

                    if (lIndex_outlet == lIndex_downslope)
                      {
                        iFound_outlet = 1;
                        (*iIterator_self).iSubbasin = iSubbasin;
                      }
                    else
                      {
                        iIterator_current = vCell_active.begin() + lIndex_downslope;
                        if (lIndex_downslope == -1)
                          {
                            //this one does not belong here
                            iFound_outlet = 1;
                          }
                      }
                  }
              }

            //std::cout << iSubbasin << std::endl;
          }

        //remove the confluence now
        vAccumulation.erase(iterator_accumulation);
        vConfluence_copy.erase(vConfluence_copy.begin() + lAccumulation);
        //repeat
      }

    return error_code;
  }

  /**
   * calculate the watershed characteristics
   * @return
   */
  int domain::domain_calculate_watershed_characteristics()
  {
    int error_code = 1;

    //should we write the result directly here?

    domain_calculate_watershed_drainage_area();
    domain_calculate_watershed_total_stream_length();
    domain_calculate_watershed_longest_stream_length();
    domain_calculate_watershed_area_to_stream_length_ratio();
    domain_calculate_watershed_average_slope();
    domain_calculate_topographic_wetness_index();

    //save watershed characteristics to the file

    domain_save_watershed_characteristics();

    std::cout << "The watershed characteristics are calculated successfully!" << std::endl;

    return error_code;
  }

  /**
   * calculate the watershed drainage total area
   * @return
   */
  int domain::domain_calculate_watershed_drainage_area()
  {
    int error_code = 1;
    long lCount = 0;

    double dArea_hexagon;
    double dLength_hexagon = (vCell_active[0]).dLength_edge;

    std::vector<hexagon>::iterator iIterator;

    for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {
        if ((*iIterator).iFlag_watershed == 1)
          {
            lCount = lCount + 1;
          }
      }

    lCell_count = lCount;
    dArea_hexagon = 1.5 * sqrt(3.0) * dLength_hexagon * dLength_hexagon;
    dArea_watershed = dArea_hexagon * lCount;
    return error_code;
  }

  /**
   * calculate  the total stream length
   * @return
   */
  int domain::domain_calculate_watershed_total_stream_length()
  {
    int error_code = 1;

    long lSegment = 0;

    double dLength_hexagon = (vCell_active[0]).dLength_edge;

    std::vector<hexagon>::iterator iIterator;

    for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {

        if ((*iIterator).iFlag_stream == 1)
          {
            lSegment = lSegment + 1;
          }
      }
    dLength_stream = sqrt(3.0) * dLength_hexagon * lSegment;
    return error_code;
  }
  /**
   * calculate the longest stream length
   * @return
   */
  int domain::domain_calculate_watershed_longest_stream_length()
  {
    int error_code = 1;
    int iFlag_outlet = 0;
    long lReach_max = 0;
    long lReach_count;
    long lIndex_current;
    long lIndex_ownstream;

    double dLength_hexagon = (vCell_active[0]).dLength_edge;
    //loop through head water
    std::vector<segment>::iterator iIterator;

    for (iIterator = vSegment.begin(); iIterator != vSegment.end(); iIterator++)
      {
        if ((*iIterator).iFlag_headwater == 1)
          {
            iFlag_outlet = 0;

            lIndex_current = (*iIterator).cReach_start.lID;

            //follow the flow direction
            lReach_count = 1;
            while (iFlag_outlet != 1)
              {
                //get the next reach

                lIndex_ownstream = (vCell_active[lIndex_current]).lIndex_downslope;
                if (lIndex_ownstream != -1)
                  {
                    lReach_count = lReach_count + 1;
                    lIndex_current = lIndex_ownstream;
                  }
                else
                  {
                    //this is the outlet
                    iFlag_outlet = 1;
                  }
              }
            //
            if (lReach_count > lReach_max)
              {
                lReach_max = lReach_count;
              }
            else
              {
              }
          }
        else
          {
            //ignore
          }
      }

    dLongest_length_stream = lReach_max * dLength_hexagon * sqrt(3.0);

    return error_code;
  }
  /**
   * calculate the watershed area to stream length ratio
   * @return
   */
  int domain::domain_calculate_watershed_area_to_stream_length_ratio()
  {
    int error_code = 1;

    double dRatio = 0.0;

    if (dLength_stream > 0)
      {
        dRatio = dArea_watershed / dLength_stream;
      }

    this->dArea_2_stream_ratio = dRatio;
    return error_code;
  }
  /**
   * calculate the mean slope of the watershed
   * @return
   */
  int domain::domain_calculate_watershed_average_slope()
  {
    int error_code = 1;
    double dSlope_total = 0.0;
    std::vector<hexagon>::iterator iIterator;

    for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {

        if ((*iIterator).iFlag_watershed == 1)
          {
            dSlope_total = dSlope_total + (*iIterator).dSlope;
          }
      }

    dSlope_mean = dSlope_total / lCell_count;
    return error_code;
  }

  /**
   * calculate the TWI index using method from //https://en.wikipedia.org/wiki/Topographic_wetness_index
   * // {\displaystyle \ln {a \over \tan b}}
   * @return
   */
  int domain::domain_calculate_topographic_wetness_index()
  {
    int error_code = 1;

    double a;
    double b;
    double c;
    double d;
    double dLength_hexagon = (vCell_active[0]).dLength_edge;
    double dArea_hexagon;
    double dTwi;
    dArea_hexagon = 1.5 * sqrt(3.0) * dLength_hexagon * dLength_hexagon;
    std::vector<hexagon>::iterator iIterator;
    //can use openmp
    for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
      {

        if ((*iIterator).iFlag_watershed == 1)
          {
            a = double(((*iIterator).lAccumulation + 1) * dArea_hexagon);
            b = (*iIterator).dSlope;
            c = tan(b);
            if (a == 0 || c == 0)
              {
                std::cout << "wrong" << std::endl;
              }
            dTwi = log2(a / c);
            if (isnan(float(dTwi)))
              {
                std::cout << "wrong" << std::endl;
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
  int domain::domain_save_watershed_characteristics()
  {
    int error_code = 1;

    std::string sLine;

    std::ofstream ofs;
    ofs.open(this->sFilename_watershed_characteristics.c_str(), ios::out);
    if (ofs.good())
      {
        sLine = "Watershed drainage area: " + convert_double_to_string(dArea_watershed);
        ofs << sLine << std::endl;

        sLine = "Longest stream length: " + convert_double_to_string(dLongest_length_stream);
        ofs << sLine << std::endl;

        sLine = "Total stream length: " + convert_double_to_string(dLength_stream);
        ofs << sLine << std::endl;

        sLine = "Area to stream length ratio: " + convert_double_to_string(dArea_2_stream_ratio);
        ofs << sLine << std::endl;

        sLine = "Average slope: " + convert_double_to_string(dSlope_mean);
        ofs << sLine << std::endl;

        ofs.close();
      }

    return error_code;
  }

  /**
   * save all the model outputs
   * @return
   */
  int domain::domain_save_result()
  {
    int error_code = 1;

    //now we will update some new result due to debug flag
    domain_save_variable(eV_elevation);
    domain_save_variable(eV_flow_direction);
    domain_save_variable(eV_flow_accumulation);

    //domain_save_variable(eV_watershed);
    //domain_save_variable(eV_confluence);
    //domain_save_variable(eV_segment);
    //domain_save_variable(eV_stream_order);
    //domain_save_variable(eV_subbasin);

    domain_save_variable(eV_wetness_index);

    //close log file

    ofs_log.close();
    std::cout << "Finished saving results!" << endl;
    std::flush(std::cout);

    return error_code;
  }

  /**
   * an advanced way to save important watershed dataset
   * @param eV_in
   * @return
   */
  int domain::domain_save_variable(eVariable eV_in)
  {
    int error_code = 1;
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
            domain_save_polygon_vector(eV_elevation, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_direction:
            sFieldname = "dire";
            sFilename = sFilename_flow_direction_polyline_debug;
            sLayername = "direction";
            domain_save_polyline_vector(eV_flow_direction, sFieldname, sFilename, sLayername);
            break;
          case eV_flow_accumulation:
            sFieldname = "accu";
            sFilename = sFilename_flow_accumulation_point_debug;
            sLayername = "accumulation";
            domain_save_point_vector(eV_flow_accumulation, sFieldname, sFilename, sLayername);
            sFilename = sFilename_flow_accumulation_polygon;
            domain_save_polygon_vector(eV_flow_accumulation, sFieldname, sFilename, sLayername);

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

            domain_save_polygon_vector(eV_elevation, sFieldname, sFilename, sLayername);

            break;
          case eV_flow_direction:
            sFieldname = "dire";
            sFilename = sFilename_flow_direction_polyline;
            sLayername = "direction";
            domain_save_polyline_vector(eV_flow_direction, sFieldname, sFilename, sLayername);
            break;
          case eV_flow_accumulation:
            sFieldname = "accu";
            sFilename = sFilename_flow_accumulation_point;
            sLayername = "accumulation";
            domain_save_point_vector(eV_flow_accumulation, sFieldname, sFilename, sLayername);
            sFilename = sFilename_flow_accumulation_polygon;
            domain_save_polygon_vector(eV_flow_accumulation, sFieldname, sFilename, sLayername);

            break;
          case eV_watershed:
            sFieldname = "wash";
            sFilename = sFilename_watershed_point;
            sLayername = "watershed";
            domain_save_point_vector(eV_watershed, sFieldname, sFilename, sLayername);

            sFilename = sFilename_watershed_polygon;
            domain_save_polygon_vector(eV_watershed, sFieldname, sFilename, sLayername);
            break;

          case eV_confluence:
            sFieldname = "conf";
            sFilename = sFilename_stream_confluence_polygon;
            sLayername = "confluence";
            domain_save_polygon_vector(eV_confluence, sFieldname, sFilename, sLayername);

            break;
          case eV_segment:
            sFieldname = "segm";
            sFilename = sFilename_stream_segment_point;
            sLayername = "segment";
            domain_save_point_vector(eV_segment, sFieldname, sFilename, sLayername);
            sFilename = sFilename_stream_segment_polygon;
            domain_save_polygon_vector(eV_segment, sFieldname, sFilename, sLayername);

            iFlag_merge = 0;
            sFilename = sFilename_stream_segment_polyline;
            domain_save_polyline_vector(eV_segment, sFieldname, sFilename, sLayername);
            iFlag_merge = 1;
            sFilename = sFilename_stream_segment_merge_polyline;
            domain_save_polyline_vector(eV_segment, sFieldname, sFilename, sLayername);
            break;

          case eV_stream_order:
            sFieldname = "stro";
            sLayername = "strord";

            sFilename = sFilename_stream_order_polyline;
            domain_save_polyline_vector(eV_stream_order, sFieldname, sFilename, sLayername);
            break;

          case eV_subbasin:
            sFieldname = "suba";
            sFilename = sFilename_subbasin_point;
            sLayername = "subbasin";
            domain_save_point_vector(eV_subbasin, sFieldname, sFilename, sLayername);

            sFilename = sFilename_subbasin_polygon;
            domain_save_polygon_vector(eV_subbasin, sFieldname, sFilename, sLayername);
            break;
          case eV_wetness_index:
            sFieldname = "weti";
            //sFilename = sFilename_wetness_index_point;
            sLayername = "wetness";
            //domain_save_point_vector(eV_wetness_index, sFieldname, sFilename, sLayername);

            sFilename = sFilename_wetness_index_polygon;
            domain_save_polygon_vector(eV_wetness_index, sFieldname, sFilename, sLayername);
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
  int domain::domain_save_point_vector(eVariable eV_in,
                                       std::string sFieldname_in,
                                       std::string sFilename_in,
                                       std::string sLayer_name_in)
  {
    int error_code = 1;
    const char *pszDriverName = "ESRI Shapefile";
    double dX, dY;

    std::vector<hexagon>::iterator iIterator;
    OGRRegisterAll();
    GDALDriver *poDriver;
    GDALDataset *poDS;
    OGRLayer *poLayer;
    OGRPoint pt;

    OGRFeature *poFeature;
    int iValue;
    double dValue;

    GIntBig lValue;

    OGRFieldDefn oField(sFieldname_in.c_str(), OFTInteger);

    switch (eV_in)
      {
      case eV_elevation:
        oField.SetType(OFTReal);
        oField.SetWidth(64);
        oField.SetPrecision(4);
        break;
      case eV_flow_direction:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_flow_accumulation:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_watershed:
        oField.SetWidth(32);
        break;
      case eV_segment:
        oField.SetWidth(32);
        break;
      case eV_subbasin:
        oField.SetWidth(32);
        break;
      default:
        break;
      }

    poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName);
    if (poDriver == NULL)
      {
        printf("%s driver not available.\n", pszDriverName);
        exit(1);
      }
    poDS = poDriver->Create(sFilename_in.c_str(), 0, 0, 0, GDT_Unknown, NULL);

    if (poDS == NULL)
      {
        printf("Creation of output file failed.\n");
        exit(1);
      }

    poLayer = poDS->CreateLayer(sLayer_name_in.c_str(), oSRS, wkbPoint, NULL);
    if (poLayer == NULL)
      {
        printf("Layer creation failed.\n");
        exit(1);
      }

    if (poLayer->CreateField(&oField) != OGRERR_NONE)
      {
        printf("Creating Name field failed.\n");
        exit(1);
      }

    if (iFlag_debug == 1)
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

            switch (eV_in)
              {
              case eV_elevation:
                dValue = (*iIterator).dElevation;
                poFeature->SetField(sFieldname_in.c_str(), dValue);
                break;
              case eV_flow_direction:
                lValue = (*iIterator).lIndex_downslope;
                poFeature->SetField(sFieldname_in.c_str(), lValue);
                break;
              case eV_flow_accumulation:
                lValue = (*iIterator).lAccumulation;
                poFeature->SetField(sFieldname_in.c_str(), lValue);
                break;

              default:
                break;
              }

            dX = (*iIterator).dX;
            dY = (*iIterator).dY;

            pt.setX(dX);
            pt.setY(dY);

            poFeature->SetGeometry(&pt);

            if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
              {
                printf("Failed to create feature in shapefile.\n");
                exit(1);
              }

            OGRFeature::DestroyFeature(poFeature);
          }
      }
    else
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {
            poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

            if ((*iIterator).iFlag_watershed != 1)
              {
                continue;
              }

            switch (eV_in)
              {
              case eV_elevation:
                dValue = (*iIterator).dElevation;
                poFeature->SetField(sFieldname_in.c_str(), dValue);
                break;
              case eV_flow_direction:
                lValue = (*iIterator).lIndex_downslope;
                poFeature->SetField(sFieldname_in.c_str(), lValue);
                break;
              case eV_flow_accumulation:
                lValue = (*iIterator).lAccumulation;
                poFeature->SetField(sFieldname_in.c_str(), lValue);
                break;
              case eV_watershed:
                iValue = (*iIterator).iFlag_watershed;
                poFeature->SetField(sFieldname_in.c_str(), iValue);
                break;
              case eV_segment:
                iValue = (*iIterator).iSegment;
                poFeature->SetField(sFieldname_in.c_str(), iValue);
                break;
              case eV_subbasin:
                iValue = (*iIterator).iSubbasin;
                poFeature->SetField(sFieldname_in.c_str(), iValue);
                break;
              default:
                break;
              }

            dX = (*iIterator).dX;
            dY = (*iIterator).dY;

            pt.setX(dX);
            pt.setY(dY);

            poFeature->SetGeometry(&pt);

            if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
              {
                printf("Failed to create feature in shapefile.\n");
                exit(1);
              }

            OGRFeature::DestroyFeature(poFeature);
          }
      }

    GDALClose(poDS);
    return error_code;
  }

  /**
   * save model outputs in the polyline shapefile format
   * @param eV_in :the variable enumerate
   * @param sFieldname_in :the attribute table field name
   * @param sFilename_in :the filename of the output file
   * @param sLayername_in :the layer name
   * @return
   */
  int domain::domain_save_polyline_vector(eVariable eV_in, std::string sFieldname_in, std::string sFilename_in,
                                          std::string sLayername_in)
  {
    int error_code = 1;
    int iValue;
    int iReach;
    long lIndex;
    const char *pszDriverName = "ESRI Shapefile";
    long lIndex_downslope;
    double dX, dY;
    double dX_start, dY_start;
    double dX_end, dY_end;
    std::vector<hexagon>::iterator iIterator;
    std::vector<hexagon> vReach_segment;
    std::vector<segment>::iterator iIterator_segment;

    OGRRegisterAll();
    GDALDriver *poDriver;
    GDALDataset *poDS;
    OGRLayer *poLayer;
    OGRFeature *poFeature;

    OGRFieldDefn oField(sFieldname_in.c_str(), OFTInteger);
    oField.SetWidth(64);
    switch (eV_in)
      {
      case eV_flow_direction:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_stream_order:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_flow_accumulation:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_segment:
        oField.SetWidth(32);
        break;
      default:
        break;
      }

    GIntBig lValue;
    poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName);
    if (poDriver == NULL)
      {
        printf("%s driver not available.\n", pszDriverName);
        exit(1);
      }

    poDS = poDriver->Create(sFilename_in.c_str(), 0, 0, 0, GDT_Unknown, NULL);

    if (poDS == NULL)
      {
        printf("Creation of output file failed.\n");
        exit(1);
      }

    poLayer = poDS->CreateLayer(sLayername_in.c_str(), oSRS, wkbLineString, NULL);
    if (poLayer == NULL)
      {
        printf("Layer creation failed.\n");
        exit(1);
      }

    if (poLayer->CreateField(&oField) != OGRERR_NONE)
      {
        printf("Creating Name field failed.\n");
        exit(1);
      }

    if (iFlag_debug == 1)
      {
        switch (eV_in)
          {
          case eV_flow_direction:
            {
              for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
                {

                  if ((*iIterator).nNeighbor == 6)
                    {
                      poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                      lValue = (*iIterator).lID;

                      //iValue = (*iIterator).iSegment;
                      poFeature->SetField(sFieldname_in.c_str(), lValue);

                      dX_start = (*iIterator).dX;
                      dY_start = (*iIterator).dY;

                      lIndex_downslope = (*iIterator).lIndex_downslope;
                      dX_end = vCell_active.at(lIndex_downslope).dX;
                      dY_end = vCell_active.at(lIndex_downslope).dY;

                      OGRLineString pt;
                      pt.addPoint(dX_start, dY_start);
                      pt.addPoint(dX_end, dY_end);

                      poFeature->SetGeometry(&pt);

                      if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                        {
                          printf("Failed to create feature in shapefile.\n");
                          exit(1);
                        }

                      OGRFeature::DestroyFeature(poFeature);
                    }
                  else
                    {
                    }
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

                  if ((*iIterator).nNeighbor == 6 && (*iIterator).iFlag_watershed == 1)
                    {
                      poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                      lValue = (*iIterator).lID;

                      //iValue = (*iIterator).iSegment;
                      poFeature->SetField(sFieldname_in.c_str(), lValue);

                      dX_start = (*iIterator).dX;
                      dY_start = (*iIterator).dY;

                      lIndex_downslope = (*iIterator).lIndex_downslope;
                      dX_end = vCell_active.at(lIndex_downslope).dX;
                      dY_end = vCell_active.at(lIndex_downslope).dY;

                      OGRLineString pt;
                      pt.addPoint(dX_start, dY_start);
                      pt.addPoint(dX_end, dY_end);

                      poFeature->SetGeometry(&pt);

                      if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                        {
                          printf("Failed to create feature in shapefile.\n");
                          exit(1);
                        }

                      OGRFeature::DestroyFeature(poFeature);
                    }
                  else
                    {
                    }
                }
              break;
            }
          case eV_stream_order:
            {
              for (iIterator_segment = vSegment.begin(); iIterator_segment != vSegment.end(); iIterator_segment++)
                {
                  poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                  iValue = (*iIterator_segment).iSegment_order;
                  poFeature->SetField(sFieldname_in.c_str(), iValue);

                  vReach_segment = (*iIterator_segment).vReach_segment;
                  OGRLineString pt;
                  for (iReach = 0; iReach < (*iIterator_segment).nReach; iReach++)
                    {
                      dX = vReach_segment.at(iReach).dX;
                      dY = vReach_segment.at(iReach).dY;
                      pt.addPoint(dX, dY);
                    }
                  //link the next one
                  lIndex = vReach_segment.back().lIndex_downslope;
                  if (lIndex != -1)
                    {
                      dX = vCell_active.at(lIndex).dX;
                      dY = vCell_active.at(lIndex).dY;
                      pt.addPoint(dX, dY);
                    }

                  poFeature->SetGeometry(&pt);
                  if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                    {
                      printf("Failed to create feature in shapefile.\n");
                      exit(1);
                    }

                  OGRFeature::DestroyFeature(poFeature);
                }
              break;
            }
          default: //stream segment
            {
              if (iFlag_merge != 1)
                {
                  for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
                    {

                      if ((*iIterator).iFlag_stream == 1 && (*iIterator).nNeighbor == 6 && (*iIterator).iFlag_watershed == 1)
                        {
                          poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                          iValue = (*iIterator).iSegment;
                          poFeature->SetField(sFieldname_in.c_str(), iValue);

                          dX_start = (*iIterator).dX;
                          dY_start = (*iIterator).dY;

                          lIndex_downslope = (*iIterator).lIndex_downslope;
                          dX_end = vCell_active.at(lIndex_downslope).dX;
                          dY_end = vCell_active.at(lIndex_downslope).dY;

                          OGRLineString pt;
                          pt.addPoint(dX_start, dY_start);
                          pt.addPoint(dX_end, dY_end);

                          poFeature->SetGeometry(&pt);

                          if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                            {
                              printf("Failed to create feature in shapefile.\n");
                              exit(1);
                            }

                          OGRFeature::DestroyFeature(poFeature);
                        }
                      else
                        {
                        }
                    }
                }
              else //merge flowline using segment class
                {
                  for (iIterator_segment = vSegment.begin(); iIterator_segment != vSegment.end(); iIterator_segment++)
                    {
                      poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                      iValue = (*iIterator_segment).iSegment;
                      poFeature->SetField(sFieldname_in.c_str(), iValue);

                      vReach_segment = (*iIterator_segment).vReach_segment;
                      OGRLineString pt;
                      for (iReach = 0; iReach < (*iIterator_segment).nReach; iReach++)
                        {
                          dX = vReach_segment.at(iReach).dX;
                          dY = vReach_segment.at(iReach).dY;
                          pt.addPoint(dX, dY);
                        }
                      //link the next one
                      lIndex = vReach_segment.back().lIndex_downslope;
                      if (lIndex != -1)
                        {
                          dX = vCell_active.at(lIndex).dX;
                          dY = vCell_active.at(lIndex).dY;
                          pt.addPoint(dX, dY);
                        }

                      poFeature->SetGeometry(&pt);
                      if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                        {
                          printf("Failed to create feature in shapefile.\n");
                          exit(1);
                        }

                      OGRFeature::DestroyFeature(poFeature);
                    }
                }

              break;
            }
          }
      }

    GDALClose(poDS);

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
  int domain::domain_save_polygon_vector(eVariable eV_in,
                                         std::string sFieldname_in, std::string sFilename_in,
                                         std::string sLayername_in)
  {
    int error_code = 1;
    const char *pszDriverName = "ESRI Shapefile";

    double dX, dY;

    std::vector<hexagon>::iterator iIterator;

    std::vector<ptVertex>::iterator pIterator;

    OGRRegisterAll();
    GDALDriver *poDriver;
    GDALDataset *poDS;
    OGRLayer *poLayer;
    OGRFeature *poFeature;

    OGRFieldDefn oField(sFieldname_in.c_str(), OFTInteger);
    oField.SetWidth(64);

    switch (eV_in)
      {
      case eV_elevation:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_flow_direction:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_flow_accumulation:
        oField.SetType(OFTInteger64);
        oField.SetWidth(64);
        break;
      case eV_watershed:
        oField.SetWidth(32);
        break;
      case eV_confluence:
        oField.SetWidth(32);
        break;
      case eV_segment:
        oField.SetWidth(32);
        break;
      case eV_subbasin:
        oField.SetWidth(32);
        break;
      case eV_wetness_index:
        oField.SetType(OFTReal);
        oField.SetWidth(32);
        oField.SetPrecision(4);
        break;
      default:
        break;
      }
    int iValue;
    double dValue;
    GIntBig lValue;

    std::string sFieldname_elevation = "elev";
    OGRFieldDefn oField_elevation(sFieldname_elevation.c_str(), OFTReal);
    oField_elevation.SetWidth(64);
    oField_elevation.SetPrecision(4);

    poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName);
    if (poDriver == NULL)
      {
        printf("%s driver not available.\n", pszDriverName);
        exit(1);
      }

    poDS = poDriver->Create(sFilename_in.c_str(), 0, 0, 0, GDT_Unknown, NULL);

    if (poDS == NULL)
      {
        printf("Creation of output file failed.\n");
        exit(1);
      }

    poLayer = poDS->CreateLayer(sLayername_in.c_str(), oSRS, wkbPolygon, NULL);
    if (poLayer == NULL)
      {
        printf("Layer creation failed.\n");
        exit(1);
      }

    if (poLayer->CreateField(&oField) != OGRERR_NONE)
      {
        printf("Creating Name field failed.\n");
        exit(1);
      }
    if (poLayer->CreateField(&oField_elevation) != OGRERR_NONE)
      {
        printf("Creating Name field failed.\n");
        exit(1);
      }

    if (iFlag_debug == 1)
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {

            if ((*iIterator).nNeighbor == 6)
              {
                poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                switch (eV_in)
                  {
                  case eV_elevation:
                    lValue = (*iIterator).lID;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_flow_direction:
                    lValue = (*iIterator).lIndex_downslope;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    break;
                  case eV_flow_accumulation:
                    lValue = (*iIterator).lAccumulation;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;

                  default:
                    break;
                  }

                OGRLinearRing poExteriorRing;
                for (pIterator = (*iIterator).vPtVertex.begin(); pIterator != (*iIterator).vPtVertex.end(); pIterator++)
                  {
                    dX = (*pIterator).dX;
                    dY = (*pIterator).dY;
                    //pt.addPoint(dX, dY);
                    poExteriorRing.addPoint(dX, dY);
                  }
                poExteriorRing.closeRings();

                OGRPolygon polygon;
                polygon.addRing(&poExteriorRing);
                poFeature->SetGeometry(&polygon);

                if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                  {
                    printf("Failed to create feature in shapefile.\n");
                    exit(1);
                  }

                OGRFeature::DestroyFeature(poFeature);
              }
            else
              {
              }
          }
      }
    else
      {
        for (iIterator = vCell_active.begin(); iIterator != vCell_active.end(); iIterator++)
          {

            if ((*iIterator).nNeighbor == 6 && (*iIterator).iFlag_watershed == 1)
              {
                poFeature = OGRFeature::CreateFeature(poLayer->GetLayerDefn());

                switch (eV_in)
                  {
                  case eV_elevation:
                    lValue = (*iIterator).lID;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_flow_direction:
                    lValue = (*iIterator).lIndex_downslope;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    break;
                  case eV_flow_accumulation:
                    lValue = (*iIterator).lAccumulation;
                    poFeature->SetField(sFieldname_in.c_str(), lValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_watershed:
                    iValue = (*iIterator).iFlag_watershed;
                    poFeature->SetField(sFieldname_in.c_str(), iValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_confluence:
                    iValue = (*iIterator).iFlag_confluence;
                    poFeature->SetField(sFieldname_in.c_str(), iValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_segment:
                    iValue = (*iIterator).iSegment;
                    poFeature->SetField(sFieldname_in.c_str(), iValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_subbasin:
                    iValue = (*iIterator).iSubbasin;
                    poFeature->SetField(sFieldname_in.c_str(), iValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  case eV_wetness_index:
                    dValue = (*iIterator).dTwi;
                    poFeature->SetField(sFieldname_in.c_str(), dValue);
                    dValue = (*iIterator).dElevation;
                    poFeature->SetField(sFieldname_elevation.c_str(), dValue);
                    break;
                  default:
                    break;
                  }

                OGRLinearRing poExteriorRing;
                for (pIterator = (*iIterator).vPtVertex.begin(); pIterator != (*iIterator).vPtVertex.end(); pIterator++)
                  {
                    dX = (*pIterator).dX;
                    dY = (*pIterator).dY;
                    //pt.addPoint(dX, dY);
                    poExteriorRing.addPoint(dX, dY);
                  }
                poExteriorRing.closeRings();

                OGRPolygon polygon;
                polygon.addRing(&poExteriorRing);
                poFeature->SetGeometry(&polygon);

                if (poLayer->CreateFeature(poFeature) != OGRERR_NONE)
                  {
                    printf("Failed to create feature in shapefile.\n");
                    exit(1);
                  }

                OGRFeature::DestroyFeature(poFeature);
              }
            else
              {
              }
          }
      }

    GDALClose(poDS);

    return error_code;
  }

  /**
   * clean up the model status
   * @return
   */
  int domain::domain_cleanup()
  {
    int error_code = 1;
    std::cout << "Finished clean up memory!" << endl;

    return error_code;
  }

  /**
   * private functions. check whether there is local depression in the dem or not. in fact, a more rigorous method should pass in dem instead of the hexagon vector
   but because we will not change any member variable here, it should be safe to pass in the vector
   * @param vCell_in
   * @return
   */
  int domain::check_digital_elevation_model_depression(std::vector<hexagon> vCell_in)
  {
    int error_code = 1;
    int iNeighbor;
    long lID;
    long lIndex_self, lIndex_search;
    double dElevation_min;
    double dElevation_self;
    std::vector<long> vNeighbor;
    std::vector<long>::iterator iIterator;
    std::vector<double> vElevation_neighbor;

#pragma omp parallel for private(lIndex_self, iIterator, iNeighbor, vNeighbor, \
                                 dElevation_self, vElevation_neighbor, lID, dElevation_min, lIndex_search)
    for (lIndex_self = 0; lIndex_self < vCell_in.size(); lIndex_self++)
      {
        if (error_code == 1)
          {
            iNeighbor = vCell_in.at(lIndex_self).nNeighbor;
            if (iNeighbor == 6)
              {
                vNeighbor = vCell_in.at(lIndex_self).vNeighbor;
                dElevation_self = vCell_in.at(lIndex_self).dElevation;
                vElevation_neighbor.clear();
                for (iIterator = vNeighbor.begin(); iIterator != vNeighbor.end(); iIterator++)
                  {
                    lID = (*iIterator);
                    //find it

                    for (lIndex_search = 0; lIndex_search < vCell_in.size(); lIndex_search++)
                      {
                        if (vCell_in.at(lIndex_search).lID == lID)
                          {
                            vElevation_neighbor.push_back(vCell_in.at(lIndex_search).dElevation);
                          }
                        else
                          {
                            //continue;
                          }
                      }
                  }
                //if it is the lowest?
                dElevation_min = *(std::min_element(vElevation_neighbor.begin(), vElevation_neighbor.end()));

                if (dElevation_self < dElevation_min)
                  {
                    error_code = 0;
                  }
              }
            else
              {
                //edge do nothing
              }
          }
        else
          {
            //continue;
          }
      }
    return error_code;
  }

  /**
   * retrieve the boundary of the hexagon grid boundary
   * @param vCell_in :the hexagon grid
   * @return
   */
  std::vector<hexagon> domain::domain_get_boundary(std::vector<hexagon> vCell_in)
  {
    int error_code = 1;
    std::vector<hexagon>::iterator iIterator1;

    std::vector<hexagon> vCell_out;

    for (iIterator1 = vCell_in.begin(); iIterator1 != vCell_in.end(); iIterator1++)
      {
        if ((*iIterator1).nNeighbor < 6)
          {
            vCell_out.push_back(*iIterator1);
          }
      }

    return vCell_out;
  }

  /**
   * find the hexagon with the lowest elevation
   * @param vCell_in :the hexagon grid
   * @return
   */
  std::array<long, 3> domain::find_lowest_cell(std::vector<hexagon> vCell_in)
  {
    long lIndex_active = 0;
    long lIndex_global = 0;
    long lIndex = 0;
    long lIndex_lowest = 0;
    double dElevation_lowest;

    std::vector<hexagon>::iterator iIterator1;
    std::array<long, 3> aIndex_out;
    if (vCell_in.size() < 2)
      {
        //something is wrong
      }
    else
      {
        //set the first as lowest
        dElevation_lowest = vCell_in[0].dElevation;
        for (iIterator1 = vCell_in.begin(); iIterator1 != vCell_in.end(); iIterator1++)
          {
            if ((*iIterator1).dElevation < dElevation_lowest)
              {
                dElevation_lowest = (*iIterator1).dElevation;
                lIndex_global = (*iIterator1).lGlobalID;
                lIndex_active = (*iIterator1).lID;
                lIndex_lowest = lIndex;
              }
            lIndex = lIndex + 1;
          }
        //be careful
        aIndex_out.at(0) = lIndex_lowest;
        aIndex_out.at(1) = lIndex_active;
        aIndex_out.at(2) = lIndex_global;
      }
    return aIndex_out;
  }

  /**
   * find all the neighbors of each hexagon cell
   * @return
   */
  int domain::find_all_neighbors()
  {
    int error_code = 1;
    int iOption = 2;
    double dX, dY;
    double dX_dummy, dY_dummy;
    double dX_self;
    double dY_self;
    double dElevation;
    double dDistance;
    double dDistance_min;

    long lIndex_self;
    long lIndex_search;
    long lIndex_pt1, lIndex_pt2;
    long lColumn_index, lRow_index;
    long lColumn_index2, lRow_index2;
    std::vector<ptVertex> vPt1, vPt2;

    switch (iMesh_type)
      {
      case 1: /* qgis mesh */
        /* code */
        if (iOption == 1)
          {
            //#pragma omp parallel for private(lIndex_self, dX_self, dY_self, dElevation, \
            dX_dummy, dY_dummy, dDistance, dDistance_min, lIndex_search)
            for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
              {
                //center location
                dX_self = (vCell_active.at(lIndex_self)).dX;
                dY_self = (vCell_active.at(lIndex_self)).dY;
                dDistance_min = (vCell_active.at(lIndex_self)).dLength_edge * sqrt(3);
                for (lIndex_search = 0; lIndex_search < vCell_active.size(); lIndex_search++)
                  {
                    if (lIndex_self == lIndex_search)
                      {
                        //itself
                      }
                    else
                      {
                        dElevation = (vCell_active.at(lIndex_search)).dElevation;
                        dX_dummy = (vCell_active.at(lIndex_search)).dX;
                        dY_dummy = (vCell_active.at(lIndex_search)).dY;
                        dDistance = sqrt(
                                         (dX_dummy - dX_self) * (dX_dummy - dX_self) + (dY_dummy - dY_self) * (dY_dummy - dY_self));
                        if (dDistance < (1.5 * dDistance_min) && dElevation != missing_value)
                          {
                            //found one
                            (vCell_active.at(lIndex_self)).vNeighbor.push_back((vCell_active.at(lIndex_search)).lID);
                          }
                        //use priority_queue later
                      }
                  }

                if ((vCell_active.at(lIndex_self)).vNeighbor.size() > 6)
                  {
                    std::cout << "Too many neighbors" << std::endl;
                  }
                else
                  {
                    (vCell_active.at(lIndex_self)).nNeighbor = (vCell_active.at(lIndex_self)).vNeighbor.size();
                  }
              }
          }
        else
          {
            if (iOption == 2)
              {
#pragma omp parallel for private(lIndex_self, vPt1, vPt2, dX, dY, lIndex_search, dX_dummy, dY_dummy, lIndex_pt1, lIndex_pt2)
                for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
                  {
                    //reset neighbot flag  to 0
                    for (lIndex_search = 0; lIndex_search < vCell_active.size(); lIndex_search++)
                      {
                        if (lIndex_self == lIndex_search)
                          {
                            //itself
                            (vCell_active.at(lIndex_search)).iFlag_neighbor = 1;
                          }
                        else
                          {
                            //reset
                            (vCell_active.at(lIndex_search)).iFlag_neighbor = 0;
                          }
                      }
                    (vCell_active.at(lIndex_self)).vNeighbor.clear();

                    vPt1 = (vCell_active.at(lIndex_self)).vPtVertex;

                    for (lIndex_pt1 = 0; lIndex_pt1 < vPt1.size(); lIndex_pt1++)
                      {
                        dX = (vPt1.at(lIndex_pt1)).dX;
                        dY = (vPt1.at(lIndex_pt1)).dY;

                        for (lIndex_search = 0; lIndex_search < vCell_active.size(); lIndex_search++)
                          {
                            if (lIndex_self == lIndex_search)
                              {
                                //itself
                              }
                            else
                              {
                                if ((vCell_active.at(lIndex_search)).iFlag_neighbor == 0) //this cell not yet checked
                                  {
                                    vPt2 = (vCell_active.at(lIndex_search)).vPtVertex;
                                    for (lIndex_pt2 = 0; lIndex_pt2 < vPt2.size(); lIndex_pt2++)
                                      {
                                        dX_dummy = (vPt2.at(lIndex_pt2)).dX;
                                        dY_dummy = (vPt2.at(lIndex_pt2)).dY;
                                        if (abs(dX_dummy - dX) < 0.01 && abs(dY_dummy - dY) < 0.01)
                                          {
                                            //this is a neighbor
                                            (vCell_active.at(lIndex_search)).iFlag_neighbor == 1;
                                            //add it

                                            if (std::find((vCell_active.at(lIndex_self)).vNeighbor.begin(),
                                                          (vCell_active.at(lIndex_self)).vNeighbor.end(), (vCell_active.at(lIndex_search)).lID) != (vCell_active.at(lIndex_self)).vNeighbor.end())
                                              {
                                                /* v contains x */
                                              }
                                            else
                                              {
                                                /* v does not contain x */
                                                (vCell_active.at(lIndex_self)).vNeighbor.push_back((vCell_active.at(lIndex_search)).lID);
                                              }

                                            //just the next vertex directly
                                            continue;
                                          }
                                      }
                                  }
                                else
                                  {
                                    /* code */
                                    //treated already
                                  }
                              }
                          }
                      }
                    //double check
                    if ((vCell_active.at(lIndex_self)).vNeighbor.size() > 6)
                      {
                        std::cout << "Too many neighbors" << std::endl;
                      }
                    else
                      {
                        (vCell_active.at(lIndex_self)).nNeighbor = (vCell_active.at(lIndex_self)).vNeighbor.size();
                      }
                  }
              }
            else
              {
                //use 2d index directly

                for (lIndex_self = 0; lIndex_self < vCell_active.size(); lIndex_self++)
                  {

                    (vCell_active.at(lIndex_self)).vNeighbor.clear();
                    long lIndex = (vCell_active.at(lIndex_self)).lGlobalID;
                    //get column and row index
                    lColumn_index = 1;
                    lRow_index = 2;

                    for (int i = 0; i < 6; i++)
                      {
                        lColumn_index2 = 2;
                        lRow_index2 = 3;
                        if (lRow_index2 > 0)
                          {
                            //add it
                            (vCell_active.at(lIndex_self)).vNeighbor.push_back((vCell_active.at(lIndex_search)).lID);
                            //just the next vertex directly
                            continue;
                          }
                      }
                  }

                //double check
                if ((vCell_active.at(lIndex_self)).vNeighbor.size() > 6)
                  {
                    std::cout << "Too many neighbors" << std::endl;
                  }
                else
                  {
                    (vCell_active.at(lIndex_self)).nNeighbor = (vCell_active.at(lIndex_self)).vNeighbor.size();
                  }
              }
          }


        break;
      case 2: //dggrid mesh

        break;
      case 3: //mpas mesh
        break;

      default:
        //qgis mesh
        break;
      }
  

  return error_code;
} // namespace hexwatershed

} // namespace hexwatershed
