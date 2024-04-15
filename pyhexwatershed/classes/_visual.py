import os
from pathlib import Path

from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.map.vector.map_vector_polygon_data import map_vector_polygon_data
from pyearth.visual.map.vector.map_vector_polyline_data import map_vector_polyline_data
from pyearth.visual.map.vector.map_multiple_vector_data import map_multiple_vector_data

from pyearth.visual.animate.animate_vector_polygon_data import animate_vector_polygon_data

def plot(self,
          iFlag_type_in = None,
          iFlag_title_in = None,
          iFlag_colorbar_in = None,
          iFlag_openstreetmap_in = None,
          sVariable_in=None,
          sFilename_output_in=None,
          iFigwidth_in=None,
          iFigheight_in=None,
          iFont_size_in=None,
          iFlag_scientific_notation_colorbar_in=None,
          dData_min_in = None,
          dData_max_in = None,
          aExtent_in = None,
          pProjection_map_in = None):

    aPolyline = ['flow_direction', 'stream_segment', 'stream_order','flowline_filter' ]
    aPolygon = ['area','elevation', 'drainage_area', 'slope', 'travel_distance', 'hillslope']
    aMixed = ['flow_direction_with_mesh', 'flow_direction_with_observation','hillslope_with_flow_direction']
    

    if iFlag_title_in is None:
        iFlag_title_in = 0
    else:
        iFlag_title_in = iFlag_title_in
    
    if sVariable_in in aPolyline:
        iFlag_type_in = 2 
    else:
        if sVariable_in in aPolygon:
            iFlag_type_in = 3
        else:
            if sVariable_in in aMixed:
                iFlag_type_in = 4

    aLegend = list()
    #sText = 'Case: ' + "{:0d}".format( int(self.iCase_index) ) 
    #aLegend.append(sText)
    sText = 'Mesh type: ' + self.sMesh_type.upper()
    aLegend.append(sText)
    if self.iMesh_type == 4:
        sResolution =  'Resolution: 3 ~ 10 km'
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

                for pBasin in self.aBasin:                   
                    pBasin.basin_plot(iFlag_type_in,                                    
                                      self.sMesh_type,
                                      iFlag_title_in= iFlag_title_in,
                                      iFont_size_in =iFont_size_in,
                                      sVariable_in= sVariable_in,
                                      sFilename_output_in=sFilename_output_in,
                                      aExtent_in=aExtent_in,
                                      aLegend_in = aLegend,
                                      pProjection_map_in = pProjection_map_in)


        else:
            if iFlag_type_in == 3: #polygon based
                if sVariable_in == 'mesh':
                    self._plot_mesh(sFilename_output_in=sFilename_output_in,
                                    aExtent_in = aExtent_in,
                                    pProjection_map_in = pProjection_map_in)
                else:                    
                    if self.iFlag_multiple_outlet == 1:
                        sFilename_mesh = self.sFilename_mesh
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
                            sFilename_mesh = pBasin.sFilename_variable_polygon
                            pBasin.basin_plot( iFlag_type_in,                                            
                                              self.sMesh_type,      
                                              iFont_size_in = iFont_size_in,     
                                              iFlag_colorbar_in = iFlag_colorbar_in,                                   
                                              iFlag_title_in = iFlag_title_in,
                                              iFlag_scientific_notation_colorbar_in=iFlag_scientific_notation_colorbar_in,
                                              dData_min_in = dData_min_in,
                                              dData_max_in = dData_max_in,
                                              sVariable_in = sVariable_in,
                                              sFilename_mesh_in = sFilename_mesh,
                                              sFilename_output_in = sFilename_output_in,
                                              aExtent_in = aExtent_in,
                                              aLegend_in = aLegend,
                                              pProjection_map_in = pProjection_map_in)

                pass
            else: #mesh + point/polyline/polygon
                if iFlag_type_in == 4: #mixed
                    if self.iFlag_multiple_outlet == 1:
                        if sVariable_in == 'flow_direction_with_mesh':
                            self._plot_variable_with_flow_direction( sFilename_output_in=sFilename_output_in,
                                                                     iFigwidth_in = iFigwidth_in,
                                                                     iFigheight_in = iFigheight_in,
                                                                     aExtent_in = aExtent_in,
                                                                     pProjection_map_in = pProjection_map_in)
                        return
                    else:                        
                       
                        for pBasin in self.aBasin:
                            sFilename_mesh = pBasin.sFilename_variable_polygon
                            pBasin.basin_plot(iFlag_type_in,    
                                                  self.sMesh_type,
                                                  sFilename_mesh_in = sFilename_mesh,
                                                  iFont_size_in = iFont_size_in,
                                                  iFlag_title_in = iFlag_title_in,
                                                  iFlag_openstreetmap_in= iFlag_openstreetmap_in,
                                                  sVariable_in = sVariable_in,
                                                  sFilename_output_in=sFilename_output_in,
                                                  aExtent_in = aExtent_in,
                                                  aLegend_in = aLegend,
                                                  pProjection_map_in = pProjection_map_in)

                    pass
                else: #careful, this one only used for special case
                    self._plot_mesh_with_flow_direction_and_river_network(sFilename_output_in=sFilename_output_in,
                                                                          iFigwidth_in = iFigwidth_in,
                                                                          iFigheight_in = iFigheight_in,
                                                                          aExtent_in = aExtent_in,
                                                                          aLegend_in = aLegend,
                                                                          pProjection_map_in = pProjection_map_in)
                    pass

    print('Finished plotting!')
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
   

    sTitle = 'Flow direction'

    map_vector_polyline_data(sFilename_json,
                             sFilename_output_in,
                             iFlag_thickness_in= iFlag_thickness_in ,
                             sTitle_in=sTitle,
                             sField_thickness_in = sField_thickness_in, #use drainage area to scale the thickness
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

def _animate(self, sFilename_in,
             iFlag_type_in = None,
             iFigwidth_in=None, iFigheight_in=None,
             iFont_size_in=None,
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
    iFlag_type_in=None,
    iFigwidth_in=None,
    iFigheight_in=None,
    aExtent_in=None,
    sTitle_in= 'Hybrid stream burning and depression filling',
    pProjection_map_in=None)

    return

