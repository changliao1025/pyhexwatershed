import os
from pathlib import Path

from pyearth.toolbox.reader.text_reader_string import text_reader_string
try:
    from pyearthviz.map.vector.map_vector_polygon_file import map_vector_polygon_file
    from pyearthviz.map.vector.map_vector_polyline_file import map_vector_polyline_file
    from pyearthviz.map.vector.map_multiple_vector_files import map_multiple_vector_files
    from pyearthviz.animate.animate_polygon_file import animate_vector_polygon_data
except ImportError:
    try:
        from pyearth.visual.animate.animate_vector_polygon_data import animate_vector_polygon_data
        from pyearth.visual.map.vector.map_multiple_vector_data import map_multiple_vector_data as map_multiple_vector_files
        from pyearth.visual.map.vector.map_vector_polygon_data import map_vector_polygon_data as map_vector_polygon_file
        from pyearth.visual.map.vector.map_vector_polyline_data import map_vector_polyline_data as map_vector_polyline_file
    except ImportError:
        map_vector_polygon_file = None
        map_vector_polyline_file = None
        map_multiple_vector_files = None
        animate_vector_polygon_data = None


def plot(self,
         iFlag_type_in=None,
         sVariable_in=None,
         sFilename_boundary_in=None,
         **kwargs):

    aPolyline = ['flow_direction', 'stream_segment', 'stream_order', 'flowline_filter']
    aPolygon = ['area', 'elevation', 'drainage_area', 'slope', 'travel_distance', 'hillslope', 'subbasin', 'area_of_difference']
    aMixed = ['flow_direction_with_mesh', 'flow_direction_with_observation', 'hillslope_with_flow_direction']

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
        sText = 'Mesh type: ' + self.sMesh_type.upper()
        aLegend.append(sText)
        if self.iMesh_type == 4:
            sResolution = 'Variable resolution'
        else:
            if self.dResolution_meter > 1000:
                sResolution = f"Resolution: {int(self.dResolution_meter / 1000):0d} km"
            else:
                sResolution = f"Resolution: {int(self.dResolution_meter):0d} m"

        aLegend.append(sResolution)
        if self.iFlag_stream_burning_topology == 1:
            sText = 'Stream topology: on'
        else:
            sText = 'Stream topology: off'
        aLegend.append(sText)
        kwargs['aLegend_in'] = aLegend
    else:
        aLegend = aLegend_in

    if iFlag_type_in == 1:  # point based
        pass
    else:
        if iFlag_type_in == 2:  # polyline based
            if sVariable_in == 'flow_direction':
                self._plot_flow_direction(**kwargs)
            else:
                if sVariable_in == 'stream_segment':
                    self._plot_stream_segment(**kwargs)
                else:
                    if sVariable_in == 'stream_order':
                        self._plot_stream_order(**kwargs)
                    else:
                        if sVariable_in == 'flowline_filter':
                            self._plot_flowline_filter(**kwargs)
        else:
            if iFlag_type_in == 3:  # polygon based
                if sVariable_in == 'area':
                    self._plot_area(**kwargs)
                else:
                    if sVariable_in == 'elevation':
                        self._plot_elevation(**kwargs)
                    else:
                        if sVariable_in == 'slope':
                            self._plot_slope(**kwargs)
                        else:
                            if sVariable_in == 'drainage_area':
                                self._plot_drainage_area(**kwargs)
                            else:
                                if sVariable_in == 'travel_distance':
                                    self._plot_travel_distance(**kwargs)
                                else:
                                    if sVariable_in == 'hillslope':
                                        self._plot_hillslope(**kwargs)
                                    else:
                                        if sVariable_in == 'subbasin':
                                            self._plot_subbasin(**kwargs)
            else:
                if iFlag_type_in == 4:  # mixed based
                    if sVariable_in == 'flow_direction_with_mesh':
                        self._plot_mesh_with_flow_direction(**kwargs)
                    else:
                        if sVariable_in == 'flow_direction_with_observation':
                            self._plot_mesh_with_flow_direction_and_observation(**kwargs)
                        else:
                            if sVariable_in == 'hillslope_with_flow_direction':
                                self._plot_hillslope_with_flow_direction(**kwargs)
                else:
                    self._plot_mesh_with_flow_direction_and_river_network(**kwargs)

    print('Finished plotting!')
    return


def _plot_flow_direction(self, **kwargs):
    sFilename_json = self.sFilename_flow_direction
    map_vector_polyline_file(1, sFilename_json, iFlag_zebra_in=1, **kwargs)
    return


def _plot_mesh_with_flow_direction(self,
                                   iFigwidth_in=None,
                                   iFigheight_in=None,
                                   sMesh_type_in=None,
                                   sFilename_mesh_in=None,
                                   sFilename_output_in=None,
                                   aExtent_in=None,
                                   pProjection_map_in=None,
                                   pProjection_data_in=None,
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
        sFilename_output = os.path.join(self.sWorkspace_output, f"mesh_with_flowline_{sMesh_type}.png")
    else:
        sFilename_output = sFilename_output_in

    sFilename = self.sFilename_flow_direction
    aFiletype_in = [3, 2]
    aFilename_in = [sFilename_mesh, sFilename]
    map_multiple_vector_files(aFiletype_in,
                             aFilename_in,
                             sFilename_output_in=sFilename_output,
                             sTitle_in='Mesh with flowline',
                             aFlag_color_in=[0, 1],
                             **kwargs)
    return


def _animate(self, sFilename_in,
             iFlag_type_in=None,
             iFigwidth_in=None,
             iFigheight_in=None,
             iFont_size_in=None,
             sTitle_in=None,
             aExtent_in=None,
             pProjection_map_in=None):

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
        sTitle_in=sTitle_in,
        pProjection_map_in=pProjection_map_in)

    return
