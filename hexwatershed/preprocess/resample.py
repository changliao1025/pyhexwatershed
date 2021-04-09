# -*- coding: utf-8 -*-

# SUMMARY:      HexResample.py
# USAGE:        Resample between DEM and Hexagon
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Zhuoran Duan
# E-MAIL:       zhuoran.duan@pnnl.gov
# ORIG-DATE:    Sept. 2020
# DESCRIPTION:  
# DESCRIP-END.
# COMMENTS:     This python script is to resample between DEM and
#               hexagons
#
# Last Change:  09-18-2020 
# -------------------------------------------------------------
#	Import system modules
# -------------------------------------------------------------

import arcpy
from arcpy import env
from arcpy.sa import *
import arcgisscripting
import sys
import os
import math
import numpy as np
import csv 

#-------------------------------------------------------------------#
#--------------------------- WorkSpace  ----------------------------#    
#-------------------------------------------------------------------#
env.workspace = "c:\\projects\\hexresample"   
path = "c:/projects/hexresample/"  # output path

#-------------------------------------------------------------------#
###########           Setup Input          
#-------------------------------------------------------------------#
elev = "dem"                  # name of DEM GRID, square based 
hexagon = "hexagon.shp"                   # name of hexagon shape file
output = path + "output.shp"             # name of output shape file/table
resample_methods = 'AREA_WEIGHTED'              # resample methods "NEAREST", "AREA_WEIGHTED", or "BILINEAR"

#-------------------------------------------------------------------#
#------------------------   End of Edits ---------------------------#
#---------------  Spatial Analysis License Required   --------------# 
#-------------------------------------------------------------------#

#Check if inputs are valid
if not arcpy.Exists(elev):
    sys.exit("DEM Grid input not valid, exit program")


if not arcpy.Exists(hexagon):
    sys.exit("hexagon shapefile input not valid, exit program")

# Set the cell size environment using a raster dataset.
env.outputCoordinateSystem = elev
#env.extent = elev

env.cellSize = elev
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("Spatial")

# Create DEM center
dem_center = path + "grid_dem_center.shp"
if arcpy.Exists(dem_center):
    arcpy.Delete_management(dem_center)
    
arcpy.RasterToPoint_conversion(in_raster=elev, out_point_features=dem_center, raster_field="Value")

out_hexa = path + "out.shp"   
if arcpy.Exists(out_hexa):
    arcpy.Delete_management(out_hexa)
arcpy.Copy_management(hexagon, out_hexa)

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        #raise ValueError('points do not form a rectangle')
        return (points[0][2])
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        #raise ValueError('(x, y) not within the rectangle')
        return (points[0][2])
    else:
        return (q11 * (x2 - x) * (y2 - y) +
                q21 * (x - x1) * (y2 - y) +
                q12 * (x2 - x) * (y - y1) +
                q22 * (x - x1) * (y - y1)
               ) / ((x2 - x1) * (y2 - y1) + 0.0)


if resample_methods == 'NEAREST':
    print 'resampling DEM using nearest method'
    
    # Create hexagon center
    hexa_center = path + "hexa_center.shp"
    if arcpy.Exists(hexa_center):
        arcpy.Delete_management(hexa_center)
        
    arcpy.FeatureToPoint_management(in_features=out_hexa, out_feature_class=hexa_center, point_location="INSIDE")

    print 'Find nearest grid center'
    # Find nearest grid center
    nearest_table = path + "nearest_table"
    if arcpy.Exists(nearest_table):
        arcpy.Delete_management(nearest_table)
    
    arcpy.GenerateNearTable_analysis(in_features=hexa_center, near_features=dem_center, out_table=nearest_table,
                                 search_radius="", location="LOCATION", angle="NO_ANGLE", closest="CLOSEST", closest_count="0", method="PLANAR")
    
    print 'Join field'
    #Join field
    arcpy.JoinField_management(in_data=out_hexa, in_field="FID", join_table=nearest_table, join_field="IN_FID", fields="NEAR_FID;NEAR_DIST")
    # Add DEM elevation information
    arcpy.JoinField_management(in_data=out_hexa, in_field = "NEAR_FID", join_table = dem_center,join_field = "FID",fields=["grid_code"])

elif resample_methods == 'AREA_WEIGHTED':

    # Creat Grid Polygon using fishnet
    grid_poly =  path + "grid_poly.shp"
    if arcpy.Exists(grid_poly):
        arcpy.Delete_management(grid_poly)
    elevRaster = arcpy.sa.Raster(elev)
    DEMExtent = elevRaster.extent
    dem_coords = str(DEMExtent.XMin) + " " + str(DEMExtent.YMin)
    y_coords = str(DEMExtent.XMin) + " " + str(DEMExtent.YMin + 10)
    corner = str(DEMExtent.XMax) + " " + str(DEMExtent.YMax)
    arcpy.CreateFishnet_management(out_feature_class=grid_poly, origin_coord=dem_coords, y_axis_coord=y_coords, cell_width=env.cellSize, cell_height=env.cellSize,
                                   number_rows="", number_columns="", corner_coord=corner,
                                   labels="LABELS", template=elev, geometry_type="POLYGON")
    
    # Pass grid cell elevation information to fishnet grid via spatial join of DEM grid center and fishnet
    grid_w_dem  = path + "grid_w_dem.shp"
    arcpy.SpatialJoin_analysis(target_features=grid_poly, join_features=dem_center, out_feature_class=grid_w_dem,
                               join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="",
                               match_option="INTERSECT", search_radius="", distance_field_name="")
    
    # Intersect two polygons
    intersect_poly = path + "intersected_poly.shp"
    arcpy.Intersect_analysis([out_hexa,grid_w_dem], intersect_poly, "", "", "")

    # For each hexagon, calculate the elevation using area-fraction weight

    # First - caluclate area
    arcpy.AddField_management(intersect_poly,'area','DOUBLE')
    arcpy.CalculateField_management(intersect_poly,'area','!shape.area!','PYTHON')
    
    # Then calculate portion
    #arcpy.AddField_management(intersect_poly, "weighted_dem", "DOUBLE")
    arr = arcpy.da.FeatureClassToNumPyArray(intersect_poly, ('FID_out', 'FID_grid_w', 'grid_code', 'area'))

    hexagon_id = []
    weighted_elev = []

    out_arr = np.zeros(len(np.unique(arr['FID_out'])), dtype=[('hexagon_id', 'i8'), ('w_elev', 'f4')])
    count = 0
    for id_num in np.unique(arr['FID_out']):
        out_arr['hexagon_id'][count] = id_num
        total_area = arr['area'][arr['FID_out'] == id_num].sum()
        fraction = arr['area'][arr['FID_out'] == id_num]/total_area
        #weighted_elev.append(np.sum(arr['grid_code'][arr['FID_out'] == id_num] * fraction))
        out_arr['w_elev'][count] = np.sum(arr['grid_code'][arr['FID_out'] == id_num] * fraction)
        count += 1 

    # Append the array to an existing table    
    arcpy.AddField_management(out_hexa,'w_elev','DOUBLE')
    arcpy.da.ExtendTable(out_hexa,  "FID", out_arr, "hexagon_id", append_only=False)
        
elif resample_methods == 'BILINEAR':
    
    # Create hexagon center
    hexa_center = path + "hexa_center.shp"
    if arcpy.Exists(hexa_center):
        arcpy.Delete_management(hexa_center)
        
    arcpy.FeatureToPoint_management(in_features=out_hexa, out_feature_class=hexa_center, point_location="INSIDE")

    print 'Find nearest grid center'
    # Find nearest grid center
    near4_table = path + "near4_table"
    if arcpy.Exists(near4_table):
        arcpy.Delete_management(near4_table)
    
    arcpy.GenerateNearTable_analysis(in_features=hexa_center, near_features=dem_center, out_table=near4_table,
                                 search_radius="", location="LOCATION", angle="NO_ANGLE", closest="ALL", closest_count="4", method="PLANAR")

    arr = arcpy.da.TableToNumPyArray(near4_table, ('IN_FID', 'NEAR_FID', 'NEAR_DIST', 'NEAR_RANK', 'FROM_X', 'FROM_Y', 'NEAR_X', 'NEAR_Y'))
    dem_arr = arcpy.da.TableToNumPyArray(dem_center, ('FID', 'grid_code'))

    out_arr = np.zeros(len(np.unique(arr['IN_FID'])), dtype=[('hexagon_id', 'i8'), ('bl_elev', 'f4')])
    count = 0
    for id_num in np.unique(arr['IN_FID']):
        
        out_arr['hexagon_id'][count] = id_num
        subset = arr[arr['IN_FID'] == id_num]       

        x_a = subset['NEAR_X']['NEAR_RANK'==1]
        y_a = subset['NEAR_Y']['NEAR_RANK'==1]
        z_a = dem_arr['grid_code'][dem_arr['FID'] ==subset['NEAR_FID']['NEAR_RANK'==1]]

        x_b = subset['NEAR_X']['NEAR_RANK'==2]
        y_b = subset['NEAR_Y']['NEAR_RANK'==2]
        z_b = dem_arr['grid_code'][dem_arr['FID'] ==subset['NEAR_FID']['NEAR_RANK'==2]]
        
        x_c = subset['NEAR_X']['NEAR_RANK'==3]
        y_c = subset['NEAR_Y']['NEAR_RANK'==3]
        z_c = dem_arr['grid_code'][dem_arr['FID'] ==subset['NEAR_FID']['NEAR_RANK'==3]]

        x_d = subset['NEAR_X']['NEAR_RANK'==4]
        y_d = subset['NEAR_Y']['NEAR_RANK'==4]
        z_d = dem_arr['grid_code'][dem_arr['FID'] ==subset['NEAR_FID']['NEAR_RANK'==4]]

        points=[(x_a,y_a,z_a),(x_b, y_b,z_b),(x_c,y_c,z_c),(x_d,y_d,z_d)]

        x_p = subset['FROM_X']['NEAR_RANK'==1]
        y_p = subset['FROM_Y']['NEAR_RANK'==1]
        
        # Point B has the same Y coord as point A
        B = subset[subset['NEAR_Y'] == y_a]
        C = subset[subset['NEAR_X'] == x_a]

        if len(B) < 2 or len(C) < 2:
            z_p= z_a
        else:
            z_p = bilinear_interpolation(x_p, y_p, points)
            
        out_arr['bl_elev'][count] = z_p
        if z_p ==0:
            raise ValueError('points do not form a rectangle')
        count +=1

    # Append the array to an existing table
    arcpy.AddField_management(out_hexa,'bl_elev','DOUBLE')
    arcpy.da.ExtendTable(out_hexa,  "FID", out_arr, "hexagon_id", append_only=False)
    
    
else:
    print 'not yet'



#arcpy.Rename_management(out_hexa, output)