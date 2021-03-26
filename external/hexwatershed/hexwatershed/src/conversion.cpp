
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file conversion.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Conversion between data types
 * @version 0.1
 * @date 2019-06-11
 * 
 * @copyright Copyright (c) 2019
 * 
 */

#include "conversion.h"




/**
 * @brief it is used to convert integer to string since c++ 11 doesn't support well
 * 
 * @param iNumber_in : the integer number
 * @return std::string 
 */
std::string convert_integer_to_string(int iNumber_in)
{
	std::string str_out;
	std::stringstream ss;
	ss << iNumber_in;
	str_out = ss.str();
	return str_out;
}

/**
 * @brief convert an integer to a string with fixed length
 * 
 * @param iNumber_in 
 * @param iWidth_in 
 * @return std::string 
 */
std::string convert_integer_to_string(int iNumber_in, int iWidth_in)
{
	std::string str_out;
	std::stringstream ss;
	ss << setfill('0') << setw(iWidth_in) << iNumber_in;
	str_out = ss.str();
	return str_out;
}

/**
 * @brief convert a double data type to string
 * 
 * @param dNumber_in 
 * @return std::string 
 */
std::string convert_double_to_string(double dNumber_in)
{
	std::string str_out;
	std::stringstream ss;
	ss << dNumber_in;
	str_out = ss.str();
	return str_out;
}

/**
 * @brief convert a double data type to a string with fixed length
 * 
 * @param iPrecision_in 
 * @param iWidth_in 
 * @param dNumber_in 
 * @return std::string 
 */
std::string convert_double_to_string(int iPrecision_in,
									 int iWidth_in,
									 double dNumber_in)
{
	std::string str_out;
	std::stringstream ss;
	ss << std::fixed << std::setw(iWidth_in) << std::setprecision(iPrecision_in) << dNumber_in;
	str_out = ss.str();
	return str_out;
}

/**
 * @brief convert temperature from kelvin to fahrenheit
 * 
 * @param dTemperature_kelvin_in 
 * @return double 
 */
double convert_from_kelvin_to_fahrenheit(double dTemperature_kelvin_in)
{
	double dTemperature_celsius = dTemperature_kelvin_in + kelvin_2_celsius;
	double dTemperature_fahrenheit_out = dTemperature_celsius * 1.8 + 32.0;
	return dTemperature_fahrenheit_out;
}
/**
 * @brief convert temperature from fahrenheit to kelvin
 * 
 * @param dTemperature_fahrenheit_in 
 * @return double 
 */
double convert_from_fahrenheit_to_kelvin(double dTemperature_fahrenheit_in)
{
	double dTemperature_celsius = (dTemperature_fahrenheit_in - 32.0) / 1.8;
	double dTemperature_kelvin_out = dTemperature_celsius - 273.15;
	return dTemperature_kelvin_out;
}
/**
 * @brief convert energy unit
 * 
 * @param dJoule_per_meter_in 
 * @return double 
 */
double convert_from_joule_per_meter_to_calorie_per_centimeter(double dJoule_per_meter_in)
{
	double dCalorie_per_meter = dJoule_per_meter_in * joule_2_calorie;
	double dCalorie_per_centimeter_out = dCalorie_per_meter / 10000.0;
	return dCalorie_per_centimeter_out;
}
/**
 * @brief conver energy units
 * 
 * @param dCalorie_per_centimeter_in 
 * @return double 
 */
double convert_from_calorie_per_centimeter_to_joule_per_meter(double dCalorie_per_centimeter_in)
{
	double dCalorie_per_meter = dCalorie_per_centimeter_in * 10000;
	double dJoule_per_meter_out = dCalorie_per_meter * calorie_2_joule;
	return dJoule_per_meter_out;
}



/**
 * @brief split a string using space
 * 
 * @param sString_in 
 * @return std::vector<std::string> 
 */
std::vector<std::string> split_string_by_space(std::string sString_in)
{
	std::size_t lLength = sString_in.length();
	if (lLength > 0)
	{
		std::istringstream iss(sString_in);
		std::istream_iterator<std::string> iterator_begin(iss), iterator_end;
		std::vector<std::string> vTokens_out(iterator_begin, iterator_end); // done!
		return vTokens_out;
	}
	else
	{
		std::vector<std::string> nothing;
		return nothing;
	}
}



/**
 * @brief split a string using user provide delimiter
 * 
 * @param sString_in 
 * @param cDelimiter 
 * @return std::vector<std::string> 
 */
std::vector<std::string> split_string_by_delimiter(std::string sString_in,
												   char cDelimiter)
{
	std::size_t lLength = sString_in.length();
	std::vector<std::string> vTokens_out;
	if (lLength > 0)
	{
		std::stringstream ss;
		ss.str(sString_in);
		std::string dummy;
		while (std::getline(ss, dummy, cDelimiter))
		{
			vTokens_out.push_back(dummy);
		}
	}
	else
	{
	}
	return vTokens_out;
}

std::string ltrim(const std::string& s)
{
	size_t start = s.find_first_not_of(WHITESPACE);
	return (start == std::string::npos) ? "" : s.substr(start);
}

std::string rtrim(const std::string& s)
{
	size_t end = s.find_last_not_of(WHITESPACE);
	return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::string trim(const std::string& s)
{
	return rtrim(ltrim(s));
}