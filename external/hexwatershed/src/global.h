
/**
 * @file global.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief provide some constant across the program
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
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

extern const float small_value; //small, from Latex
extern const float tiny_value; //extreme small, from Latex
extern const float near_zero; //the smallest

extern const float dRadius_earth;
//
extern const float pi;
//extern const float missing_value;
// time
extern const float minute_2_second;
extern const float day_2_second;
extern const float day_2_minute;
extern const float hour_2_second;
extern const float dTimestep_eco3d; // unit: second
extern const float dTimestep_eco3d_minute; // unit: minutes
extern const float dTimestep_eco3d_hour; // unit: second
extern const float dTimestep_eco3d_day; // unit: minutes

extern const float dTimestep_eco3d_stream_minute; // unit: minutes

// length

extern const float meter_2_millimeter;
extern const float meter_2_foot; // conversion
extern const float millimeter_2_meter;
extern const float inch_2_meter;
extern const float inch_2_centimeter;
// area
extern const float square_meter_2_square_centimeter;
extern const float hpa_2_pa;

// mass
extern const float gram_2_kilogram;
extern const float milligram_2_kilogram;
// temperature
extern const float kelvin_2_celsius;
extern const float celsius_2_kelvin;
// conversion
extern const float cubic_meter_2_cubic_centimeter;
extern const float cubic_meter_2_cubic_liter;
extern const float cubic_centimeter_2_cubic_meter;

extern const float kilogram_per_kilogram_2_milligram_per_gram;
extern const float milligram_per_gram_2_kilogram_per_kilogram;

extern const float kilogram_per_cubic_meter_2_gram_per_cubic_centimeter;
extern const float kilogram_per_cubic_meter_2_gram_per_liter;
extern const float kilogram_per_cubic_meter_2_milligram_per_liter;
extern const float milligram_per_liter_2_kilogram_per_cubic_meter;

extern const float kilogram_per_square_meter_2_gram_per_square_meter;

extern const float gram_per_square_meter_2_kilogram_per_square_meter;

extern const float joule_2_calorie;
extern const float joule_2_megajoule;
extern const float joule_2_langley; // convert from joulies  to langley

extern const float calorie_2_joule; // convert from calorie  to langley

extern const float langley_2_joule;

extern const float dMissing_value_default;

///50==================================================
// physical
extern const float dStefan_boltzmann;
//extern const float dManning_roughness;
extern const float radian;
extern const float dEccentricity;
// revolution speed of the Earth, radians per day , this is very close to
// pi/180, but it is different.
extern const float dSolar_constant; // units: watt per square meter, look at
// wiki: https://en.wikipedia.org/wiki/Solar_constant
extern const float dFrozen_temperature; // unit: K
extern const float dDensity_water;      // density of water, unit:

extern const float dLatent_heat_water; // heat of fusion (latent heat) of
										// water. units: joule per kilogram
extern const float dSpecific_heat_water; // the specific heat of water, units:
										  // j / (kg * kelvin )
extern const float dSpecific_heat_ice;   //  units: j / (kg * kelvin )
extern const float tkwat; // thermal conductivity of water (w/m/kelvin)
extern const float tkice; // thermal conductivity of ice (w/m/kelvin)
extern const float cwat;  // specific heat capacity of water (j/m**3/kelvin)
extern const float cice;  // specific heat capacity of ice (j/m**3/kelvin)

  //50==================================================
// gis
//extern const float dResolution; // unit: meter
//extern const float dArea;
// modules
extern const float dTemperature_all_rain; // unit: kelvin
extern const float dTemperature_all_snow; // unit: kelvin
extern const float dFraction_sublimation; //
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

extern     std::string sExtension_header  ;
extern     std::string sExtension_envi     ;
extern     std::string sExtension_text     ;


