/**
 * @file system.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief file and path operation functions
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#include "system.h"

/**
   * @brief test the existence of a file. not the most efficient, but easy to understand for now
   * 
   * @param sFilename_in 
   * @return int 
   */
int file_test(std::string sFilename_in)
{

#ifdef _WIN32
	//define something for Windows (32-bit and 64-bit, this part is common)
	DWORD attribs = GetFileAttributesA(sFilename_in.c_str());
	if (attribs != INVALID_FILE_ATTRIBUTES)
	{
		if (attribs != FILE_ATTRIBUTE_DIRECTORY)
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		return 0;
	}
#ifdef _WIN64
	//define something for Windows (64-bit only)
#else
	//define something for Windows (32-bit only)
#endif
#elif __APPLE__
	struct stat sStat;
	if (stat(sFilename_in.c_str(), &sStat) == 0)
	{
		if (S_ISREG(sStat.st_mode))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		return 0;
	}
#if TARGET_IPHONE_SIMULATOR
	// iOS Simulator
#elif TARGET_OS_IPHONE
	// iOS device
#elif TARGET_OS_MAC
	// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
	// linux
	struct stat sStat;
	if (stat(sFilename_in.c_str(), &sStat) == 0)
	{
		if (S_ISREG(sStat.st_mode))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		return 0;
	}
#elif __unix__ // all unices not caught above
	// Unix
#elif defined(_POSIX_VERSION)
	// POSIX
#else
#error "Unknown compiler"
#endif
}

/**
   * @brief recursive mkdir when it does not exist
   * 
   * @param sDirectory_in 
   * @return int 
   */
int make_directory(std::string sDirectory_in)
{

	//the maximum length for current setting
	int dir_err;

#ifdef _WIN32
	//define something for Windows (32-bit and 64-bit, this part is common)
	char tmp[MAX_PATH];
	char *p = NULL;
	size_t len;
	//50==================================================
	//convert char * to cstring
	//50==================================================
	snprintf(tmp, sizeof(tmp), "%s", sDirectory_in.c_str());
	//50==================================================
	len = strlen(tmp);
	//50==================================================
	//remove the last slash
	//50==================================================
	if (tmp[len - 1] == slash)
	{
		tmp[len - 1] = 0;
	}
	//50==================================================
	for (p = tmp + 1; *p; p++)
	{
		if (*p == slash)
		{
			//50==================================================
			// Temporarily truncate
			//50==================================================
			*p = 0;

			std::string temp(tmp);
			if (path_test(temp) == false)
			{

				dir_err = _mkdir(tmp);
			}
			//50==================================================
			//recover the slash
			//50==================================================
			*p = slash;
		}
	}
	//50==================================================
	//final step
	//50==================================================

	dir_err = _mkdir(tmp);

	if (-1 == dir_err)
	{
		cout << "Error creating directory!" << tmp << endl;
		return 0;
	}
	else
	{
		return 1;
	}
#ifdef _WIN64
	//define something for Windows (64-bit only)
#else
	//define something for Windows (32-bit only)
#endif
#elif __APPLE__

	char tmp[PATH_MAX];
	char *p = NULL;
	size_t len;
	//50==================================================
	//convert char * to cstring
	//50==================================================
	snprintf(tmp, sizeof(tmp), "%s", sDirectory_in.c_str());
	//50==================================================
	len = strlen(tmp);
	//50==================================================
	//remove the last slash
	//50==================================================
	if (tmp[len - 1] == slash)
	{
		tmp[len - 1] = 0;
	}
	//50==================================================
	for (p = tmp + 1; *p; p++)
	{
		if (*p == slash)
		{
			//50==================================================
			// Temporarily truncate
			//50==================================================
			*p = 0;

			std::string temp(tmp);
			if (path_test(temp) == false)
			{

				mkdir(tmp, S_IRWXU);
			}
			//50==================================================
			//recover the slash
			//50==================================================
			*p = slash;
		}
	}
	//50==================================================
	//final step
	//50==================================================

	dir_err = mkdir(tmp, S_IRWXU);

	if (-1 == dir_err)
	{
		cout << "Error creating directory!" << tmp << endl;
		return 0;
	}
	else
	{
		return 1;
	}
#if TARGET_IPHONE_SIMULATOR
	// iOS Simulator
#elif TARGET_OS_IPHONE
	// iOS device
#elif TARGET_OS_MAC
	// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
	// linux
	char tmp[PATH_MAX];
	char *p = NULL;
	size_t len;
	//50==================================================
	//convert char * to cstring
	//50==================================================
	snprintf(tmp, sizeof(tmp), "%s", sDirectory_in.c_str());
	//50==================================================
	len = strlen(tmp);
	//50==================================================
	//remove the last slash
	//50==================================================
	if (tmp[len - 1] == slash)
	{
		tmp[len - 1] = 0;
	}
	//50==================================================
	for (p = tmp + 1; *p; p++)
	{
		if (*p == slash)
		{
			//50==================================================
			// Temporarily truncate
			//50==================================================
			*p = 0;

			std::string temp(tmp);
			if (path_test(temp) == false)
			{

				mkdir(tmp, S_IRWXU);
			}
			//50==================================================
			//recover the slash
			//50==================================================
			*p = slash;
		}
	}
	//50==================================================
	//final step
	//50==================================================

	dir_err = mkdir(tmp, S_IRWXU);

	if (-1 == dir_err)
	{
		cout << "Error creating directory!" << tmp << endl;
		return 0;
	}
	else
	{
		return 1;
	}
#elif __unix__ // all unices not caught above
	// Unix
#elif defined(_POSIX_VERSION)
	// POSIX
#else
#error "Unknown compiler"
#endif
}

/**
 * @brief test the existence of a path, use the stat header file
 * 
 * @param sPath_in 
 * @return int 
 */
int path_test(std::string sPath_in)
{
#ifdef _WIN32
	DWORD attribs = GetFileAttributesA(sPath_in.c_str());
	if (attribs == FILE_ATTRIBUTE_DIRECTORY)
	{
		return 1;
	}
	else
	{
		return 0;
	}
	//define something for Windows (32-bit and 64-bit, this part is common)
#ifdef _WIN64
	//define something for Windows (64-bit only)
#else
	//define something for Windows (32-bit only)
#endif
#elif __APPLE__

	struct stat sStat;
	if (stat(sPath_in.c_str(), &sStat) == 0)
	{
		if (S_ISDIR(sStat.st_mode))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		return 0;
	}
#if TARGET_IPHONE_SIMULATOR
	// iOS Simulator
#elif TARGET_OS_IPHONE
	// iOS device
#elif TARGET_OS_MAC
	// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
	// linux
	struct stat sStat;
	if (stat(sPath_in.c_str(), &sStat) == 0)
	{
		if (S_ISDIR(sStat.st_mode))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	else
	{
		return 0;
	}
#elif __unix__ // all unices not caught above
	// Unix
#elif defined(_POSIX_VERSION)
	// POSIX
#else
#error "Unknown compiler"
#endif
}

/**
 * @brief 
 * 
 * @param sCommand_in 
 * @return int 
 */
int run_command(std::string sCommand_in)
{
	int error_code = 1;

#ifdef _WIN32
	//define something for Windows (32-bit and 64-bit, this part is common)
#ifdef _WIN64
	//define something for Windows (64-bit only)
#else
	//define something for Windows (32-bit only)
#endif
#elif __APPLE__

	FILE *pFile;
	char buffer[512];
	if (!(pFile = popen(sCommand_in.c_str(), "r")))
	{
		error_code = 0; //failed to submit job
	}
	else
	{
		//get the output
		while (fgets(buffer, sizeof(buffer), pFile) != NULL)
		{
			//prpFilet the output
			std::cout << buffer << std::endl;
		}
		//close the output
		pclose(pFile);
	}
#if TARGET_IPHONE_SIMULATOR
	// iOS Simulator
#elif TARGET_OS_IPHONE
	// iOS device
#elif TARGET_OS_MAC
	// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
	// linux
	FILE *pFile;
	char buffer[512];
	if (!(pFile = popen(sCommand_in.c_str(), "r")))
	{
		error_code = 0; //failed to submit job
	}
	else
	{
		//get the output
		while (fgets(buffer, sizeof(buffer), pFile) != NULL)
		{
			//prpFilet the output
			std::cout << buffer << std::endl;
		}
		//close the output
		pclose(pFile);
	}
#elif __unix__ // all unices not caught above
	// Unix
#elif defined(_POSIX_VERSION)
	// POSIX
#else
#error "Unknown compiler"
#endif

	return error_code;
}

/**
 * @brief Get the file size object
 * 
 * @param sFilename_in 
 * @return long 
 */
long get_file_size(std::string sFilename_in)
{
	std::ifstream ifs;
	std::streampos fsize;
	long lfsize;
	ifs.open(sFilename_in, std::ifstream::ate | std::ifstream::binary);
	if (ifs.good())
	{
		fsize = ifs.tellg();
		//convert the type to long, be careful with this operation!!!
		lfsize = long(fsize);
	}
	else
	{
		lfsize = -1;
	}
	//close the file
	ifs.close();
	return lfsize;
}
