
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file global.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file the global class
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once
#include <string>
using namespace std;

//50==================================================
// the global constant file for all the modules
// some constants or variables are written cross-platfrom
//50==================================================
// math
//to reduce float point error, we used different level of thresholds to 
//remove some values

extern const double small_value; //small, from Latex
extern const double tiny_value; //extreme small, from Latex
extern const double near_zero; //the smallest

//
extern const double pi;
//extern const double missing_value;
// time
extern const double minute_2_second;
extern const double day_2_second;
extern const double day_2_minute;
extern const double hour_2_second;
extern const double dTimestep_eco3d; // unit: second
extern const double dTimestep_eco3d_minute; // unit: minutes
extern const double dTimestep_eco3d_hour; // unit: second
extern const double dTimestep_eco3d_day; // unit: minutes

extern const double dTimestep_eco3d_stream_minute; // unit: minutes

// length

extern const double meter_2_millimeter;
extern const double meter_2_foot; // conversion
extern const double millimeter_2_meter;
extern const double inch_2_meter;
extern const double inch_2_centimeter;
// area
extern const double square_meter_2_square_centimeter;
extern const double hpa_2_pa;

// mass
extern const double gram_2_kilogram;
extern const double milligram_2_kilogram;
// temperature
extern const double kelvin_2_celsius;
extern const double celsius_2_kelvin;
// conversion
extern const double cubic_meter_2_cubic_centimeter;
extern const double cubic_meter_2_cubic_liter;
extern const double cubic_centimeter_2_cubic_meter;

extern const double kilogram_per_kilogram_2_milligram_per_gram;
extern const double milligram_per_gram_2_kilogram_per_kilogram;

extern const double kilogram_per_cubic_meter_2_gram_per_cubic_centimeter;
extern const double kilogram_per_cubic_meter_2_gram_per_liter;
extern const double kilogram_per_cubic_meter_2_milligram_per_liter;
extern const double milligram_per_liter_2_kilogram_per_cubic_meter;

extern const double kilogram_per_square_meter_2_gram_per_square_meter;

extern const double gram_per_square_meter_2_kilogram_per_square_meter;



extern const double joule_2_calorie;
extern const double joule_2_megajoule;
extern const double joule_2_langley; // convert from joulies  to langley

extern const double calorie_2_joule; // convert from calorie  to langley

extern const double langley_2_joule;



///50==================================================
// physical
extern const double dStefan_boltzmann;
extern const double dManning_roughness;
extern const double radian;
extern const double dEccentricy;
// revolution speed of the Earth, radians per day , this is very close to
// pi/180, but it is different.
extern const double dSolar_constant; // units: watt per square meter, look at
// wiki: https://en.wikipedia.org/wiki/Solar_constant
extern const double dFrozen_temperature; // unit: K
extern const double dDensity_water;      // density of water, unit:

extern const double dLatent_heat_water; // heat of fusion (latent heat) of
										// water. units: joule per kilogram
extern const double dSpecific_heat_water; // the specific heat of water, units:
										  // j / (kg * kelvin )
extern const double dSpecific_heat_ice;   //  units: j / (kg * kelvin )
extern const double tkwat; // thermal conductivity of water (w/m/kelvin)
extern const double tkice; // thermal conductivity of ice (w/m/kelvin)
extern const double cwat;  // specific heat capacity of water (j/m**3/kelvin)
extern const double cice;  // specific heat capacity of ice (j/m**3/kelvin)

  //50==================================================
// gis
extern const double dResolution; // unit: meter
extern const double dArea;
// modules
extern const double dTemperature_all_rain; // unit: kelvin
extern const double dTemperature_all_snow; // unit: kelvin
extern const double dFraction_sublimation; //
// system
extern const char slash;

extern std::string sError_file_missing ;
extern std::string sError_open_failed ;
extern std::string sError_data_missing ;

//log report
extern std::string sLog_data_quality ;
extern std::string sLog_open_success ;

extern std::string sModule_cascade;
extern std::string sModule_snow ;


