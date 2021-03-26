/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file global.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief  The source file of the global file.
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#include "global.h"

//50==================================================
//the global constant file for all the modules
//some constants or variables are written cross-platfrom
//50==================================================

const double small_value = 1.0E-4; //lai, denominator, etc, 
const double tiny_value = 1.0E-8; //intermediate
const double near_zero = 1.0E-12;  //for result

const double pi = 3.141592654;
//const double missing_value = -9999.0;
// time
const double day_2_second = 3600 * 24;
const double day_2_minute = 60 * 24;
const double minute_2_second = 60;
const double hour_2_second = 3600;
const double dTimestep_eco3d = day_2_second; // unit: second
const double dTimestep_eco3d_minute = day_2_minute; //minutes
const double dTimestep_eco3d_hour = 24.0; //hour
const double dTimestep_eco3d_day = 1.0; //day

const double dTimestep_eco3d_stream_minute = 1; //1.0 minute for stream routing
// length
const double meter_2_millimeter = 1.0E3;
const double meter_2_foot = 3.28084; // conversion
const double millimeter_2_meter = 1.0E-3;
const double inch_2_meter = 2.54 / 1.0E2;
const double inch_2_centimeter = 2.54;

// area
const double square_meter_2_square_centimeter = 1.0E4;
const double hpa_2_pa = 1.0E2;

// mass
const double gram_2_kilogram = 1.0E-3;
const double milligram_2_kilogram = 1.0E-6;
// temperature
const double kelvin_2_celsius = -273.15;
const double celsius_2_kelvin = 273.15;
// conversion
const double cubic_meter_2_cubic_centimeter = 1.0E6;
const double cubic_meter_2_cubic_liter = 1.0E3;
const double cubic_centimeter_2_cubic_meter = 1.0E-6;

const double kilogram_per_kilogram_2_milligram_per_gram = 1.0E3;
const double milligram_per_gram_2_kilogram_per_kilogram = 1.0E-3;

const double kilogram_per_cubic_meter_2_gram_per_cubic_centimeter =
        1.0E3 / 1.0E6;
const double kilogram_per_cubic_meter_2_gram_per_liter = 1.0;
const double kilogram_per_cubic_meter_2_milligram_per_liter = 1.0E3;
const double milligram_per_liter_2_kilogram_per_cubic_meter = 1.0E-3;

const double kilogram_per_square_meter_2_gram_per_square_meter = 1.0E3;
const double gram_per_square_meter_2_kilogram_per_square_meter = 1.0E-3;


const double joule_2_calorie = 1.0 / 4.1858;

const double joule_2_megajoule = 1.0E-6;
const double joule_2_langley = 1.0 / 41840.0; // convert from joule to langley

const double calorie_2_joule = 4.1858; // convert from calorie to langley


const double langley_2_joule = 41840.0;

// physical
const double dStefan_boltzmann = 5.670373E-8; // unit: w/m-2 K-4
const double dManning_roughness = 0.02;
const double radian = 0.0172;
const double dEccentricy = 0.0167;
// solar constant units: watt per square meter, look at wiki:
// https://en.wikipedia.org/wiki/Solar_ ant
const double dSolar_constant = 1368.0;
const double dFrozen_temperature = 273.15; // unit: K
const double dDensity_water = 1.0E3;      // density of water, unit:
const double dLatent_heat_water =
        333.55 *
                1.0E3; // heat of fusion (latent heat) of water. units: joule per kilogram
const double dSpecific_heat_water =
        4.179 * 1.0E3; // the specific heat of water, units: j / (kg * kelvin )
const double dSpecific_heat_ice =
        2.03 * 1.0E3;        // the specific heat of ice, units: j / (kg * kelvin )
const double tkwat = 1.0; // thermal conductivity of water (w/m/kelvin)
const double tkice = 1.0; // thermal conductivity of ice (w/m/kelvin)
const double cwat = 1.0;  // specific heat capacity of water (j/m**3/kelvin)
const double cice = 1.0;  // specific heat capacity of ice (j/m**3/kelvin)
// gis
const double dResolution = 500.0; // unit: meter
const double dArea = 500.0 * 500.0;
// modules
const double dTemperature_all_rain = 273.15; // unit: kelvin
const double dTemperature_all_snow = 273.15; // unit: kelvin
const double dFraction_sublimation = 0.5; // snow, this one should be in snow class
// system
const char slash = '/';

std::string sError_file_missing = "The following file does not exist: ";
std::string sError_open_failed = "Failed to open file: ";
std::string sError_data_missing = "Failed to read some data from: ";
std::string sLog_data_quality = "Data quality is low. ";
std::string sLog_open_success = "Succeed to open file: ";

