import os
from pathlib import Path

from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.map.vector.map_vector_polygon_file import map_vector_polygon_file
from pyearth.visual.map.vector.map_vector_polyline_file import map_vector_polyline_file
from pyearth.visual.map.vector.map_multiple_vector_files import map_multiple_vector_files
from pyearth.visual.animate.animate_vector_polygon_data import animate_vector_polygon_data

def plot(self,
          iFlag_type_in = None,
          sVariable_in=None,
          sFilename_boundary_in = None,
          **kwargs):

    aPolyline = ['flow_direction', 'stream_segment', 'stream_order','flowline_filter' ]
    aPolygon = ['area','elevation', 'drainage_area', 'slope', 'travel_distance', 'hillslope', 'subbasin', 'area_of_difference']
    aMixed = ['flow_direction_with_mesh', 'flow_direction_with_observation','hillslope_with_flow_direction']

    if sVariable_in in aPolyline:
        iFlag_type_in = 2
    else:
        if sVariable_in in aPolygon:
            iFlag_type_in = 3
        else:
            if sVariable_in in aMixed:
                iFlag_type_in = 4

    aLegend_in = kwargs.get('aLegend_in', None)
    if aLegend_in is None:
        aLegend = list()
        #sText = 'Case: ' + "{:0d}".format( int(self.iCase_index) )
        #aLegend.append(sText)
        sText = 'Mesh type: ' + self.sMesh_type.upper()
        aLegend.append(sText)
        if self.iMesh_type == 4:
            sResolution =  'Variable resolution'
        else:
            if self.dResolution_meter > 1000:
                sResolution =  'Resolution: ' + "{:0d}".format( int(self.dResolution_meter/1000) ) + ' km'
            else:
                sResolution =  'Resolution: ' + "{:0d}".format( int(self.dResolution_meter) ) + ' m'

        aLegend.append(sResolution)
        if self.iFlag_stream_burning_topology ==1:
            sText = 'Stream topology: on'
        else:
            sText = 'Stream topology: off'
        aLegend.append(sText)
        kwargs.setdefault('aLegend_in', aLegend)
    else:
        aLegend = aLegend_in

    #remove aLegend_in from kwargs
    if 'aLegend_in' in kwargs:
        kwargs.setdefault('aLegend_in', aLegend)

    if iFlag_type_in == 1: #point based
        #not yet implemented
        pass
    else:
        if iFlag_type_in == 2: #polyline based
            if self.iFlag_global == 1:
                self.plot_flow_direction(iFlag_thickness_in = 1,
                                            sField_thickness_in = 'drainage_area',
                                             **kwargs)
                pass
            else:
                if self.iFlag_multiple_outlet == 1:
                    #remove the iFlag_title if
                    #check whether this is set
                    iFlag_title = kwargs.get('iFlag_title_in', None)
                    if iFlag_title is not None:
                        kwargs['sTitle_in'] = 'Flow Direction'
                        #remove the iFlag_title
                        kwargs.pop('iFlag_title_in')
                    else:
                        kwargs['sTitle_in'] = None
                    self.plot_flow_direction(iFlag_thickness_in = 1,
                                            sField_thickness_in = 'drainage_area', **kwargs)

                else:
                    #for each basin
                    for pBasin in self.aBasin:
                        pBasin.basin_plot(iFlag_type_in,
                                            self.sMesh_type,
                                          sVariable_in,
                                              **kwargs)


        else:
            if iFlag_type_in == 3: #polygon based
                if sVariable_in == 'mesh':
                    self._plot_mesh(**kwargs)
                else:
                    if self.iFlag_multiple_outlet == 1:
                        sFilename_mesh = self.sFilename_mesh
                        self._plot_mesh_with_variable( sVariable_in,
                                                       sFilename_mesh_in = sFilename_mesh,
                                                   **kwargs)

                    else:
                        #for each basin
                        #polygon based, only mesh
                        for pBasin in self.aBasin:
                            sFilename_mesh = pBasin.sFilename_variable_polygon
                            pBasin.basin_plot( iFlag_type_in,
                                              self.sMesh_type,
                                              sVariable_in,
                                              sFilename_mesh_in = sFilename_mesh,
                                              sFilename_boundary_in = sFilename_boundary_in,
                                              **kwargs)

                pass
            else: #mesh + point/polyline/polygon
                if iFlag_type_in == 4: #mixed
                    if self.iFlag_multiple_outlet == 1:
                        if sVariable_in == 'flow_direction_with_mesh':
                            self._plot_variable_with_flow_direction( **kwargs)
                        return
                    else:
                        for pBasin in self.aBasin:
                            sFilename_mesh = pBasin.sFilename_variable_polygon
                            pBasin.basin_plot(iFlag_type_in,
                                                  self.sMesh_type,
                                                  sVariable_in,
                                                  sFilename_mesh_in = sFilename_mesh,
                                                  sFilename_boundary_in = sFilename_boundary_in,
                                                  **kwargs)

                    pass
                else: #careful, this one only used for special case
                    self._plot_mesh_with_flow_direction_and_river_network(**kwargs)
                    pass

    print('Finished plotting!')
    return

def plot_flow_direction(self, **kwargs):

    sFilename_json = self.sFilename_flow_direction

    map_vector_polyline_file(1, sFilename_json,
                             iFlag_zebra_in=1,
                              **kwargs)
    return

def _plot_mesh_with_flow_direction(self,
                                   iFigwidth_in=None,
                                   iFigheight_in=None,
                                   sMesh_type_in = None,
                                   sFilename_mesh_in = None,
                                   sFilename_output_in = None,
                                   aExtent_in = None,
                                   pProjection_map_in = None,
                                   pProjection_data_in = None,
                                   **kwargs):
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
    map_multiple_vector_files(aFiletype_in,
                             aFilename_in,
                             sFilename_output_in=sFilename_output,
                             sTitle_in= 'Mesh with flowline',
                             aFlag_color_in=[0, 1],
                             **kwargs)
    return

def _animate(self, sFilename_in,
             iFlag_type_in = None,
             iFigwidth_in=None,
             iFigheight_in=None,
             iFont_size_in=None,
             sTitle_in=None,
             aExtent_in = None,
             pProjection_map_in = None):

    #this function is under update
    sFilename_mesh = self.sFilename_mesh
    sFilename_animation_json = self.sFilename_animation_json
    sFilename_animation_out = sFilename_in
    animate_vector_polygon_data(
        sFilename_mesh,
        sFilename_animation_json,
        sFilename_animation_out,
        iFlag_type_in=iFlag_type_in,
        iFigwidth_in=iFigwidth_in,
        iFigheight_in=iFigheight_in,
        aExtent_in=aExtent_in,
        sTitle_in= sTitle_in,
        pProjection_map_in=pProjection_map_in)

    return

