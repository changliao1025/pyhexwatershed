import os, stat
import json


from pyflowline.external.pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyflowline.external.pyearth.visual.map.map_vector_polygon_data import map_vector_polygon_data
from pyflowline.external.pyearth.visual.map.map_vector_polyline_data import map_vector_polyline_data
from pyflowline.external.pyearth.visual.map.map_multiple_vector_data import map_multiple_vector_data

def _plot(self, sFilename_in, 
        iFlag_type_in = None, 
        sVariable_in=None, 
        sFilename_output_in=None,
        
        iFigwidth_in=None,
          iFigheight_in=None,
          aExtent_in = None, 
        pProjection_map_in = None):

    if iFlag_type_in == 1: #polygon based   
        if sVariable_in == 'mesh':
            self._plot_mesh(sFilename_output_in=sFilename_output_in, 
                            aExtent_in = aExtent_in, 
                            pProjection_map_in = pProjection_map_in)
        else:
            self._plot_mesh_with_variable(   sVariable_in, 
                                          sFilename_output_in=sFilename_output_in
                                           iFigwidth_in=iFigwidth_in,
                                           iFigheight_in=iFigheight_in,
                                          aExtent_in= aExtent_in, 
                                          pProjection_map_in= pProjection_map_in)            
    else:
        if iFlag_type_in == 2: #polyline based
            self._plot_flow_direction(sFilename_in, 
                                      iFigwidth_in=iFigwidth_in,
                                      iFigheight_in=iFigheight_in, 
                                      aExtent_in= aExtent_in,
                                      pProjection_map_in= pProjection_map_in)
            pass
        else: #mesh + line
            if iFlag_type_in == 3: #mixed
                if sVariable_in == 'mesh_w_flow_direction':
                    self._plot_mesh(sFilename_output_in=sFilename_output_in, 
                                    aExtent_in = aExtent_in,
                                     pProjection_map_in= pProjection_map_in)
                else:
                    self._plot_variable_with_flow_direction(sFilename_in, 
                                                        iFigwidth_in=iFigwidth_in, 
                                                        iFigheight_in=iFigheight_in, 
                                                        aExtent_in= aExtent_in, 
                                                          pProjection_map_in= pProjection_map_in)
                pass
            else: #careful, this one only used for special case
                self._plot_mesh_with_flow_direction_and_river_network(sFilename_in,
                                                                      iFigwidth_in=iFigwidth_in, 
                                                                      iFigheight_in=iFigheight_in,
                                                                      aExtent_in= aExtent_in, 
                                                                        pProjection_map_in= pProjection_map_in)
                pass
    
    return

def _plot_mesh(self,
                sFilename_output_in=None, 
               aExtent_in=None,   
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
                             sFilename_output_in=None,
                              iFigwidth_in=None, 
                              iFigheight_in=None, 
                             aExtent_in=None, 
                              pProjection_map_in = None, 
    dData_min_in = None, 
    dData_max_in = None):

    sMesh_type = self.sMesh_type

    if self.iMesh_type !=4:
        if sVariable_in == 'elevation':
            sVariable='Elevation'
            sTitle = 'Surface elevation'
            sUnit = r'Unit: m'
            dData_min = dData_min_in
            dData_max = dData_max_in
            sFilename_in = 
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
                    sTitle = 'Travel distance'
                    sUnit = r'Unit: m'
                    dData_min = 0.0
                    dData_max = dData_max_in
                else:    
                    sVariable='dSlope_between'
                    sTitle = 'Surface slope'
                    sUnit = r'Unit: percent'
                    dData_min = dData_min_in
                    dData_max = dData_max_in
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
    
    map_vector_polygon_data(sFilename_in, 
                            sFilename_output_in=sFilename_output_in, 
                            sTitle_in= sMesh_type,
                             aExtent_in = aExtent_in, 
                            pProjection_map_in = pProjection_map_in )


     
    return
 
def _plot_flow_direction(self, sFilename_in, aExtent_in=None,  iFlag_antarctic_in=None, 
                          iFigwidth_in=None, iFigheight_in=None,pProjection_map_in = None):   
    
    map_vector_polyline_data(sFilename_json, 
                             sFilename_output_in,                       
                             iFlag_thickness_in=0  , 
                             sTitle_in=sTitle, 
                             iFlag_color_in= iFlag_color,
                             iFlag_label_in=iFlag_label, 
                             aExtent_in = aExtent_in, 
                             pProjection_map_in = pProjection_map_in) 
    return

def _plot_mesh_with_flow_direction(self,sFilename_in, aExtent_in = None,  iFlag_antarctic_in=None, 
                                    iFigwidth_in=None, iFigheight_in=None,pProjection_map_in = None):
    
    map_multiple_vector_data(aFiletype_in, aFilename_in, 
                             sFilename_output_in=sFilename_output_in, 
                             sTitle_in= 'Mesh with flowline',
                             aFlag_color_in=[0, 1])
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

