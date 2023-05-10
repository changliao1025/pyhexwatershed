
 
 /**
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
const float dRadius_earth = 6378137.0;
const float small_value = 1.0E-4; //lai, denominator, etc, 
const float tiny_value = 1.0E-8; //intermediate
const float near_zero = 1.0E-12;  //for result

const float pi = 3.141592654;
//const float missing_value = -9999.0;
// time
const float day_2_second = 3600 * 24;
const float day_2_minute = 60 * 24;
const float minute_2_second = 60;
const float hour_2_second = 3600;
const float dTimestep_eco3d = day_2_second; // unit: second
const float dTimestep_eco3d_minute = day_2_minute; //minutes
const float dTimestep_eco3d_hour = 24.0; //hour
const float dTimestep_eco3d_day = 1.0; //day

const float dTimestep_eco3d_stream_minute = 1; //1.0 minute for stream routing
// length
const float meter_2_millimeter = 1.0E3;
const float meter_2_foot = 3.28084; // conversion
const float millimeter_2_meter = 1.0E-3;
const float inch_2_meter = 2.54 / 1.0E2;
const float inch_2_centimeter = 2.54;

// area
const float square_meter_2_square_centimeter = 1.0E4;
const float hpa_2_pa = 1.0E2;

// mass
const float gram_2_kilogram = 1.0E-3;
const float milligram_2_kilogram = 1.0E-6;
// temperature
const float kelvin_2_celsius = -273.15;
const float celsius_2_kelvin = 273.15;
// conversion
const float cubic_meter_2_cubic_centimeter = 1.0E6;
const float cubic_meter_2_cubic_liter = 1.0E3;
const float cubic_centimeter_2_cubic_meter = 1.0E-6;

const float kilogram_per_kilogram_2_milligram_per_gram = 1.0E3;
const float milligram_per_gram_2_kilogram_per_kilogram = 1.0E-3;

const float kilogram_per_cubic_meter_2_gram_per_cubic_centimeter =
        1.0E3 / 1.0E6;
const float kilogram_per_cubic_meter_2_gram_per_liter = 1.0;
const float kilogram_per_cubic_meter_2_milligram_per_liter = 1.0E3;
const float milligram_per_liter_2_kilogram_per_cubic_meter = 1.0E-3;

const float kilogram_per_square_meter_2_gram_per_square_meter = 1.0E3;
const float gram_per_square_meter_2_kilogram_per_square_meter = 1.0E-3;


const float joule_2_calorie = 1.0 / 4.1858;

const float joule_2_megajoule = 1.0E-6;
const float joule_2_langley = 1.0 / 41840.0; // convert from joule to langley

const float calorie_2_joule = 4.1858; // convert from calorie to langley


const float langley_2_joule = 41840.0;

// physical
const float dStefan_boltzmann = 5.670373E-8; // unit: w/m-2 K-4
//const float dManning_roughness = 0.02;
const float radian = 0.0172;
const float dEccentricity = 0.0167;

const float dMissing_value_default = -9999.0;
// solar constant units: watt per square meter, look at wiki:
// https://en.wikipedia.org/wiki/Solar_ ant
const float dSolar_constant = 1368.0;
const float dFrozen_temperature = 273.15; // unit: K
const float dDensity_water = 1.0E3;      // density of water, unit:
const float dLatent_heat_water =
        333.55 *
                1.0E3; // heat of fusion (latent heat) of water. units: joule per kilogram
const float dSpecific_heat_water =
        4.179 * 1.0E3; // the specific heat of water, units: j / (kg * kelvin )
const float dSpecific_heat_ice =
        2.03 * 1.0E3;        // the specific heat of ice, units: j / (kg * kelvin )
const float tkwat = 1.0; // thermal conductivity of water (w/m/kelvin)
const float tkice = 1.0; // thermal conductivity of ice (w/m/kelvin)
const float cwat = 1.0;  // specific heat capacity of water (j/m**3/kelvin)
const float cice = 1.0;  // specific heat capacity of ice (j/m**3/kelvin)
// gis
//const float dResolution = 500.0; // unit: meter
//const float dArea = 500.0 * 500.0;
// modules
const float dTemperature_all_rain = 273.15; // unit: kelvin
const float dTemperature_all_snow = 273.15; // unit: kelvin
const float dFraction_sublimation = 0.5; // snow, this one should be in snow class
// system
const char slash = '/';

std::string sError_file_missing = "The following file does not exist: ";
std::string sError_open_failed = "Failed to open file: ";
std::string sError_data_missing = "Failed to read some data from: ";
std::string sLog_data_quality = "Data quality is low. ";
std::string sLog_open_success = "Succeed to open file: ";

      std::string sExtension_header      = ".hdr";
      std::string sExtension_envi      = ".dat";
      std::string sExtension_text      = ".txt";



