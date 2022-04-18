/**
 * @file conversion.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The header file of the conversion source file
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
//50==================================================
//c++ library
//50==================================================
#include <string>
#include <iomanip>
#include <iterator>
#include <sstream>
#include <vector>
#include <algorithm>

//50==================================================
//local header
//50==================================================
#include "global.h"
using namespace std;
//50==================================================

const std::string WHITESPACE = " \n\r\t\f\v";

//50==================================================
//unit conversion
//50==================================================
float convert_from_kelvin_to_fahrenheit(float dTemperature_kelvin_in);
float convert_from_fahrenheit_to_kelvin(float dTemperature_fahrenheit_in);
float convert_from_joule_per_meter_to_calorie_per_centimeter(float dJoule_per_meter_in);
float convert_from_calorie_per_centimeter_to_joule_per_meter(float dCalorie_per_centimeter_in);

std::string convert_integer_to_string(int iNumber_in);
std::string convert_long_to_string(long iNumber_in);
std::string convert_integer_to_string(int iNumber_in,
	int iWidth_in);
std::string convert_double_to_string(double dNumber_in);
std::string convert_double_to_string(int iPrecision_in,
	int iWidth_in,
	double dNumber_in);

std::string convert_float_to_string(float dNumber_in);
std::string convert_float_to_string(int iPrecision_in,
	int iWidth_in,
	float dNumber_in);

float convert_degree_to_radian( float dAngle_degree);

std::vector<std::string> split_string_by_space(std::string sString_in);
std::vector<std::string> split_string_by_delimiter(std::string sString_in, char cDelimiter_in);

//string trim
std::string ltrim(const std::string& s);
std::string rtrim(const std::string& s);
std::string trim(const std::string& s);

