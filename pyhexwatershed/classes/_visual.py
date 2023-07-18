import os, stat
import json
from pathlib import Path

from pyflowline.external.pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyflowline.external.pyearth.visual.map.map_vector_polygon_data import map_vector_polygon_data
from pyflowline.external.pyearth.visual.map.map_vector_polyline_data import map_vector_polyline_data
from pyflowline.external.pyearth.visual.map.map_multiple_vector_data import map_multiple_vector_data

def _plot(self,
          iFlag_type_in = None,
          iFlag_title_in = None,
          sVariable_in=None,
          sFilename_output_in=None,
          iFigwidth_in=None,
          iFigheight_in=None,
          aExtent_in = None,
          pProjection_map_in = None):

    if iFlag_type_in == 1: #point based
        #not yet implemented
        pass
    else:
        if iFlag_type_in == 2: #polyline based
            if self.iFlag_multiple_outlet == 1:
                self._plot_flow_direction(iFigwidth_in=iFigwidth_in,
                                          iFigheight_in=iFigheight_in,
                                          aExtent_in= aExtent_in,
                                          pProjection_map_in= pProjection_map_in)

            else:
                #for each basin
                #polyline based, only flowline
                sVariable_in = 'flow_direction'
                for pBasin in self.aBasin:
                    pBasin.basin_plot(iFlag_type_in,
                                      self.iCase_index,
                                      self.iMesh_type,
                                      self.sMesh_type,
                                      iFlag_title_in= iFlag_title_in,
                                      sVariable_in= sVariable_in,
                                      aExtent_in=aExtent_in,
                                      pProjection_map_in = pProjection_map_in)


        else:
            if iFlag_type_in == 3: #polygon based
                if sVariable_in == 'mesh':
                    self._plot_mesh(sFilename_output_in=sFilename_output_in,
                                    aExtent_in = aExtent_in,
                                    pProjection_map_in = pProjection_map_in)
                else:
                    sFilename_mesh = self.sFilename_mesh
                    if self.iFlag_multiple_outlet == 1:
                        self._plot_mesh_with_variable( sVariable_in,
                                                       iFigwidth_in=iFigwidth_in,
                                                       iFigheight_in=iFigheight_in,
                                                       sFilename_mesh_in = sFilename_mesh,
                                                       sFilename_output_in=sFilename_output_in,
                                                       aExtent_in = aExtent_in,
                                                       pProjection_map_in = pProjection_map_in)
                    else:
                        #for each basin
                        #polygon based, only mesh
                        for pBasin in self.aBasin:

                            pBasin.basin_plot(iFlag_type_in,
                                              self.iCase_index,
                                              self.iMesh_type,
                                              self.sMesh_type,
                                              sFilename_mesh_in = sFilename_mesh,
                                              iFlag_title_in = iFlag_title_in,
                                              sVariable_in = sVariable_in,
                                              aExtent_in = aExtent_in,
                                              pProjection_map_in = pProjection_map_in)

                pass
            else: #mesh + point/polyline/polygon
                if iFlag_type_in == 4: #mixed
                    if sVariable_in == 'mesh_w_flow_direction':
                        self._plot_mesh_with_flow_direction(sFilename_output_in=sFilename_output_in,
                                                            aExtent_in = aExtent_in,
                                                            pProjection_map_in = pProjection_map_in)
                    else:
                        if self.iFlag_multiple_outlet == 1:
                            self._plot_variable_with_flow_direction( sFilename_output_in=sFilename_output_in,
                                                                     iFigwidth_in = iFigwidth_in,
                                                                     iFigheight_in = iFigheight_in,
                                                                     aExtent_in = aExtent_in,
                                                                     pProjection_map_in = pProjection_map_in)
                        else:
                            for pBasin in self.aBasin:
                                pBasin.basin_plot(iFlag_type_in,
                                                  self.iCase_index,
                                                  self.iMesh_type,
                                                  self.sMesh_type,
                                                  sFilename_mesh_in = sFilename_mesh,
                                                  iFlag_title_in = iFlag_title_in,
                                                  sVariable_in = sVariable_in,
                                                  aExtent_in = aExtent_in,
                                                  pProjection_map_in = pProjection_map_in)

                    pass
                else: #careful, this one only used for special case
                    self._plot_mesh_with_flow_direction_and_river_network(sFilename_output_in=sFilename_output_in,
                                                                          iFigwidth_in = iFigwidth_in,
                                                                          iFigheight_in = iFigheight_in,
                                                                          aExtent_in = aExtent_in,
                                                                          pProjection_map_in = pProjection_map_in)
                    pass

    return

def _plot_flow_direction(self,
                         iFigwidth_in=None,
                         iFigheight_in=None,
                         iFlag_thickness_in = None,
                         sField_thickness_in = None,
                         sFilename_output_in = None,
                         aExtent_in=None,
                         pProjection_map_in = None):

    sFilename_json = self.sFilename_flow_direction
    if sFilename_output_in is None:
        sFilename_output = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , self.sMesh_type + "_flow_direction.png" )
    else:
        sFilename_output = sFilename_output_in

    sTitle = 'Flow direction'

    map_vector_polyline_data(sFilename_json,
                             sFilename_output_in,
                             iFlag_thickness_in= iFlag_thickness_in ,
                             sTitle_in=sTitle,
                             sField_thickness_in = sField_thickness_in, #use drainage area to scale the thickness
                             aExtent_in = aExtent_in,
                             pProjection_map_in = pProjection_map_in)
    return

def _plot_mesh(self,
               sFilename_output_in = None,
               aExtent_in = None,
               pProjection_map_in = None):

    sFilename_in = self.sFilename_mesh #must be in the geojson format
    sMesh_type = self.sMesh_type

    map_vector_polygon_data(sFilename_in,
                            sFilename_output_in=sFilename_output_in,
                            sTitle_in= sMesh_type,
                            aExtent_in = aExtent_in,
                            pProjection_map_in= pProjection_map_in )


    return

def _plot_mesh_with_variable(self,
                             sVariable_in,
                             iFigwidth_in=None,
                             iFigheight_in=None,
                             dData_min_in = None,
                             dData_max_in = None,
                             sMesh_type_in = None,
                             sFilename_mesh_in = None,
                             sFilename_output_in=None,
                             aExtent_in=None,
                             pProjection_map_in = None):
    """_summary_

    Args:
        sVariable_in (_type_): _description_
        sFilename_output_in (_type_, optional): _description_. Defaults to None.
        iFigwidth_in (_type_, optional): _description_. Defaults to None.
        iFigheight_in (_type_, optional): _description_. Defaults to None.
        aExtent_in (_type_, optional): _description_. Defaults to None.
        pProjection_map_in (_type_, optional): _description_. Defaults to None.
        dData_min_in (_type_, optional): _description_. Defaults to None.
        dData_max_in (_type_, optional): _description_. Defaults to None.
    """
    if sMesh_type_in is None:
        sMesh_type = self.sMesh_type
    else:
        sMesh_type = sMesh_type_in

    if sFilename_mesh_in is None:
        sFilename_mesh = self.sFilename_mesh
    else:
        sFilename_mesh = sFilename_mesh_in

    if sFilename_output_in is None:
        sFilename_output = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_" + sVariable_in + ".png" )
    else:
        sFilename_output = sFilename_output_in



    if sMesh_type != 'mpas':
        if sVariable_in == 'elevation':
            sVariable='Elevation'
            sTitle = 'Surface elevation'
            sUnit = r'Unit: m'
            dData_min = dData_min_in
            dData_max = dData_max_in
            sFilename = self.sFilename_elevation
        else:
            if sVariable_in == 'drainagearea':
                sVariable='DrainageArea'
                sTitle = 'Drainage area'
                sUnit = r'Unit: $m^{2}$'
                dData_min = dData_min_in
                dData_max = dData_max_in
                sFilename = self.sFilename_drainage_area

            else:
                if sVariable_in == 'distance_to_outlet':
                    sVariable='dDistance_to_watershed_outlet'
                    sTitle = 'Travel distance'
                    sUnit = r'Unit: m'
                    dData_min = 0.0
                    dData_max = dData_max_in
                    iFlag_subbasin = 1
                    sFilename = self.sFilename_distance_to_outlet
                else:
                    sVariable='dSlope_between'
                    sTitle = 'Surface slope'
                    sUnit = r'Unit: percent'
                    dData_min = dData_min_in
                    dData_max = dData_max_in
                    sFilename = self.sFilename_slope_between
    else:
        if sVariable_in == 'elevation':
            sVariable='Elevation' #Elevation_profile'
            sTitle = 'Surface elevation'
            sUnit = 'Unit: m'
            dData_min = dData_min_in
            dData_max = dData_max_in
        else:
            if sVariable_in == 'drainagearea':
                sVariable='DrainageArea'
                sTitle = 'Drainage area'
                sUnit = r'Unit: $m^{2}$'
                dData_min = dData_min_in
                dData_max = dData_max_in
            else:
                if sVariable_in == 'distance_to_outlet':
                    sVariable='dDistance_to_watershed_outlet'
                    sTitle = 'Distance to outlet'
                    sUnit = r'Unit: m'
                    dData_min = 0.0
                    dData_max = dData_max_in
                else:
                    sVariable='dSlope_between'
                    sTitle = 'Surface slope'
                    sUnit = 'Unit: percent'
                    dData_min = 0.0
                    dData_max = dData_max_in




    aFiletype_in = [3, 3]
    aFilename_in = [sFilename_mesh, sFilename]
    map_multiple_vector_data(aFiletype_in,
                             aFilename_in,
                             sFilename_output_in=sFilename_output,
                             sTitle_in= 'Mesh with flowline',
                             aFlag_color_in=[0, 1],
                             aExtent_in = aExtent_in,
                             pProjection_map_in = pProjection_map_in)


    return



def _plot_mesh_with_flow_direction(self,
                                   iFigwidth_in=None,
                                   iFigheight_in=None,
                                   sMesh_type_in = None,
                                   sFilename_mesh_in = None,
                                   sFilename_output_in = None,
                                   aExtent_in = None,
                                   pProjection_map_in = None):
    if sMesh_type_in is None:
        sMesh_type = self.sMesh_type
    else:
        sMesh_type = sMesh_type_in

    if sFilename_mesh_in is None:
        sFilename_mesh = self.sFilename_mesh
    else:
        sFilename_mesh = sFilename_mesh_in

    if sFilename_output_in is None:
        sFilename_output = os.path.join(str(Path(self.sWorkspace_output_hexwatershed)  ) , sMesh_type + "_mesh_w_flow_direction.png" )
    else:
        sFilename_output = sFilename_output_in

    sFilename = self.sFilename_flow_direction #this can be either domain wide or subbasin level

    aFiletype_in = [3, 2]

    aFilename_in = [sFilename_mesh, sFilename]
    map_multiple_vector_data(aFiletype_in,
                             aFilename_in,
                             sFilename_output_in=sFilename_output_in,
                             sTitle_in= 'Mesh with flowline',
                             aFlag_color_in=[0, 1])
    return

def basin_plot(self,
               iFlag_type_in,
               sMesh_type,
               iFlag_title_in=None,
               dData_min_in = None,
               dData_max_in = None,

               sFilename_output_in=None,
               sFilename_mesh_in = None,

               sVariable_in=None,
               aExtent_in = None,
               pProjection_map_in = None):

    iFlag_label = 0

    sWorkspace_output_basin = self.sWorkspace_output_basin

    if sFilename_output_in is None:
        sFilename_output = os.path.join(sWorkspace_output_basin, sMesh_type + "_" + sVariable_in + "_basin"  + ".png")
    else:
        sFilename_output = sFilename_output_in

    if sFilename_mesh_in is None:
        sFilename_mesh = self.sFilename_mesh
    else:
        sFilename_mesh = sFilename_mesh_in

    if iFlag_type_in ==1:
        #point based
        pass
    else:
        if iFlag_type_in ==2: #polyline based
            iFlag_thickness = 1
            sField_thickness = 'dDrainageArea'
            sTitle = 'Flow direction'
            #only flow direction is supported
            map_vector_polyline_data(sFilename,
                                     sFilename_output,
                                     iFlag_thickness_in= iFlag_thickness,
                                     sTitle_in=sTitle,
                                     sField_thickness_in = sField_thickness,
                                     aExtent_in = aExtent_in,
                                     pProjection_map_in = pProjection_map_in)
            pass
        else:
            if iFlag_type_in == 3:#polygon based

                self._plot_mesh_with_variable( sVariable_in,
                                               sFilename_mesh_in = sFilename_mesh_in,
                                               sFilename_output_in=sFilename_output_in,
                                               aExtent_in = aExtent_in,
                                               pProjection_map_in = pProjection_map_in)

                pass
            else:
                if iFlag_type_in == 4:#mixed

                    sFilename = self.sFilename_flow_direction #this can be either domain wide or subbasin level

                    aFiletype_in = [3, 2]

                    aFilename_in = [sFilename_mesh, sFilename]
                    map_multiple_vector_data(aFiletype_in,
                                             aFilename_in,
                                             sFilename_output_in=sFilename_output_in,
                                             sTitle_in= 'Mesh with flowline',
                                             aFlag_color_in=[0, 1])
                    pass
                else:
                    #unsupported
                    pass

    return

def _animate(self, sFilename_in,
             iFlag_type_in = None,
             iFigwidth_in=None, iFigheight_in=None,
             aExtent_in = None,
             pProjection_map_in = None):

    #this function is under update

    return

def _plot_mesh_with_flow_direction_and_river_network(self, sFilename_in, aExtent_in = None,  iFigwidth_in=None, iFigheight_in=None, pProjection_map_in = None):



    return
