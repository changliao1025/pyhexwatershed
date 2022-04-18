/**
 * @file data.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Deal with data read and write operations.
 * @version 0.1
 * @date 2017-01-25
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#include "data.h"
data::data()
{

}
data::~data()
{
}


/**
 * @brief read_eco3d binary file (float type)
 * 
 * @param sFilename_in 
 * @return float* 
 */
float * data::read_binary(std::string sFilename_in)
{
	float * pData_out = nullptr;
	long lLength1, lLength2;
	float dummy;
	std::ifstream ifs;
	if (file_test(sFilename_in) == 1)
	{

		ifs.open(sFilename_in.c_str(), ios::in | ios::binary);
		if (ifs.good())
		{
			ifs.seekg(0, ios::end);
			lLength1 = long(ifs.tellg());
			ifs.seekg(0, ios::beg);
			lLength2 = lLength1 / sizeof(float);
			pData_out = new float[lLength2];
			for (long i = 0; i < lLength2; i++)
			{
				ifs.read(reinterpret_cast<char*>(&dummy), sizeof dummy);
				pData_out[i] = dummy;
			}
		}
		else
		{
			//std::cout << sError_open_failed << sFilename_in << std::endl;
		}


		ifs.close();
	}
	else
	{
		//file missing
		//std::cout << sError_file_missing << sFilename_in << std::endl;
	}


	return pData_out;
}


/**
 * @brief read_eco3d binary into a two dimension array pointer
 * 
 * @param sFilename_in 
 * @param lColumn_in 
 * @param lRow_in 
 * @return float** 
 */
float ** data::read_binary(string sFilename_in,
	long lColumn_in,
	long lRow_in
)
{
	float dummy;
	float * pdata_dummy = nullptr;
	float ** pData_out = nullptr;
	std::ifstream ifs;
	if (file_test(sFilename_in) == 1)
	{
		ifs.open(sFilename_in.c_str(), ios::in | ios::binary);
		if (ifs.good())
		{
			pdata_dummy = new float[lColumn_in*lRow_in];
			for (long i = 0; i < lColumn_in*lRow_in; i++)
			{
				ifs.read(reinterpret_cast<char*>(&dummy), sizeof dummy);
				pdata_dummy[i] = dummy;
			}
			pData_out = new float *[lRow_in];
			for (long i = 0; i < lRow_in; i++)
			{
				pData_out[i] = pdata_dummy + lColumn_in * i;
			}	

		}
		else
		{
			//std::cout << sError_open_failed << sFilename_in << std::endl;
		}
		ifs.close();

	}
	else
	{
		//file missing
		std::cout << sError_file_missing << sFilename_in << std::endl;
	}
//delete[] pdata_dummy;
	return pData_out;
}


/**
 * @brief read_eco3d binary and save to a vector
 * 
 * @param sFilename_in 
 * @return vector<float> 
 */
vector<float> data::read_binary_vector(std::string sFilename_in)
{
	long lLength1, lLength2;
	float dummy;
	std::ifstream ifs;
	std::vector<float> vData_out;
    vData_out.clear();
	if (file_test(sFilename_in) == 1)
	{
		ifs.open(sFilename_in.c_str(), ios::in | ios::binary);
		if (ifs.good())
		{
			ifs.seekg(0, ios::end);
			lLength1 = long(ifs.tellg());
			ifs.seekg(0, ios::beg);
			lLength2 = lLength1 / sizeof(float);

			for (long i = 0; i < lLength2; ++i)
			{
				ifs.read(reinterpret_cast<char*>(&dummy), sizeof dummy);
				vData_out.push_back(dummy);
			}
		}
		else
		{
			std::cout << sError_open_failed << sFilename_in << std::endl;
		}
		ifs.close();
	}
	else
	{
		//file missing
		std::cout << sError_file_missing << sFilename_in << std::endl;
	}
	return vData_out;
}



/**
 * @brief write vector to float binary file

 * 
 * @param sFilename_out 
 * @param vData_in 
 * @return int 
 */
int data::write_binary_vector(std::string sFilename_out, std::vector <float> vData_in)
{
	int error_code = 1;
	float dDummy0, dDummy1;
	//50==================================================
	//covert from float to float first
	//50==================================================
	//the old approach will cause loss data warning
	//std::vector<float> vData_float(vData_in.begin(), vData_in.end());	
	//the new approach
	//in the next developement, I will use template instead of explict conversion
	std::vector<float> vData_float;
	std::vector<float>::iterator iIterator_double;
	std::vector<float>::iterator iIterator_float;
	std::ofstream ofs;
	for (iIterator_double = vData_in.begin(); iIterator_double != vData_in.end(); iIterator_double++)
	{
		dDummy0 = float(*iIterator_double);
		vData_float.push_back(dDummy0);
	}
	//50==================================================
	//check the data quality
	//if all data are missing values, then we don't need it
	//50==================================================
	iIterator_float = std::max_element(vData_float.begin(),
		vData_float.end());

	dDummy1 = *iIterator_float;
	if (dDummy1 == -9999.00)  //we define -9999 as the missing value
	{
		std::cout << sLog_data_quality << std::endl;
		error_code = 0;
	}
	else
	{
		
		ofs.open(sFilename_out.c_str(), ios::out | ios::binary);
		if (ofs.good())
		{
			ofs.write(reinterpret_cast<char*>(&vData_float[0]), vData_float.size() * sizeof(float));
			error_code = 1;
		}
		else
		{
			std::cout << sError_open_failed << sFilename_out << std::endl;
			error_code = 0;
		}
		ofs.close();
	}
	return error_code;
}
