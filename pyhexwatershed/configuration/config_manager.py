import os, sys
#use this function to generate an initial json file for hexwatershed
import json
from pathlib import Path
import numpy as np
#once it's generated, you can modify it and use it for different simulations

from pyhexwatershed.classes.pycase import hexwatershedcase

from pyflowline.configuration.config_manager import create_basin_template_configuration_file
from pyflowline.classes.pycase import flowlinecase

class HexwatershedConfigManager:
    """Configuration manager for pyhexwatershed that handles defaults and serialization"""

    @staticmethod
    def get_default_config():
        """Returns a dictionary with all default configuration values"""
        return {
            # Mesh and processing flags
            "iFlag_use_mesh_dem": 0,
            "iFlag_save_mesh": 1,
            "iFlag_simplification": 1,
            "iFlag_create_mesh": 1,
            "iFlag_intersect": 1,
            "iFlag_resample_method": 2,  # Different default from pyflowline
            "iFlag_global": 0,
            "iFlag_multiple_outlet": 0,
            "iFlag_elevation_profile": 0,  # Different default from pyflowline
            "iFlag_rotation": 0,
            "iFlag_stream_burning_topology": 1,
            "iFlag_save_elevation": 1,

            # Hexwatershed-specific flags
            "iFlag_use_shapefile_extent": 0,
            "iFlag_flowline": 1,
            "iFlag_merge_reach": 1,

            # Basin and outlet configuration
            "nOutlet": 1,
            "dAccumulation_threshold": 100000,

            # Resolution and spatial parameters
            "dResolution_degree": 0.5,
            "dResolution_meter": 10000,  # Different default from pyflowline
            "dLongitude_left": -180,
            "dLongitude_right": 180,
            "dLatitude_bot": -90,
            "dLatitude_top": 90,

            # Model identification
            "sRegion": "susquehanna",
            "sModel": "pyhexwatershed",
            "iCase_index": 1,
            "sMesh_type": "hexagon",
            "sJob": "pyhexwatershed",
            "sDate": "20220202",

            # File naming conventions
            "flowline_info": "flowline_info.json",
            "sFilename_mesh_info": "mesh_info.json",
            "sFilename_elevation": "elevation.geojson",  # Different extension from pyflowline
            "sFilename_hexwatershed": "hexwatershed",

            # File paths (will be populated based on workspace)
            "sFilename_dem": None,
            "sFilename_mesh_netcdf": None,
            "sFilename_spatial_reference": None,
            "sFilename_pyflowline_config": None
        }

    @staticmethod
    def create_template_config(output_filename, custom_values=None):
        """Create a configuration file with default values, optionally customized

        Args:
            output_filename (str or Path): Path to save the configuration file
            custom_values (dict, optional): Dictionary of values to override defaults

        Returns:
            dict: The created configuration
        """
        # Get defaults
        config = HexwatershedConfigManager.get_default_config()

        # Handle workspace paths
        config["sWorkspace_input"] = str(Path.cwd())
        config["sWorkspace_output"] = str(Path.cwd())
        config["sFilename_model_configuration"] = str(output_filename)

        # Apply customizations first
        if custom_values:
            for key, value in custom_values.items():
                if isinstance(value, Path):
                    value = str(value)
                config[key] = value

        # Set up hexwatershed-specific file paths based on workspace_input
        sWorkspace_input = config["sWorkspace_input"]
        config["sFilename_dem"] = str(Path(sWorkspace_input) / "dem_ext.tif")
        config["sFilename_mesh_netcdf"] = str(Path(sWorkspace_input) / "lnd_cull_mesh.nc")
        config["sFilename_spatial_reference"] = str(Path(sWorkspace_input) / "boundary_proj.shp")
        config["sFilename_pyflowline_config"] = str(output_filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_filename)), exist_ok=True)

        # Write to file
        with open(output_filename, 'w') as f:
            json.dump(config, f, indent=4)

        return config

def create_pyhexwatershed_template_configuration_file(sFilename_json, **kwargs):
    """Generate pyhexwatershed config template file using parameter keywords

    Args:
        sFilename_json (str): Path to save the configuration file
        **kwargs: Keyword arguments to override default configuration values
            Supported keys include:
            - sWorkspace_input (str): Input workspace path
            - sWorkspace_output (str): Output workspace path
            - iFlag_use_mesh_dem (int): Flag to use mesh DEM
            - iFlag_use_shapefile_extent (int): Flag to use shapefile extent
            - iCase_index (int): Case index
            - dResolution_degree (float): Resolution in degrees
            - dResolution_meter (float): Resolution in meters
            - sDate (str): Date string
            - sMesh_type (str): Mesh type
            - sModel (str): Model name
            - nOutlet (int): Number of outlets
            - And any other configuration parameters

    Returns:
        hexwatershedcase: The initialized hexwatershed model object
    """

    # Create the configuration using the config manager
    config = HexwatershedConfigManager.create_template_config(sFilename_json, kwargs)

    # Initialize the hexwatershed model with the config
    oPyhexwatershed = hexwatershedcase(config, iFlag_create_directory_in = 0)

    # Initialize the pyflowline model
    oPyflowline = flowlinecase(config,
                              iFlag_standalone_in=0,
                              iFlag_create_directory_in = 0,
                              sModel_in='pyflowline',
                              sWorkspace_output_in=oPyhexwatershed.sWorkspace_output_pyflowline)

    # Generate basin config
    sDirname = os.path.dirname(sFilename_json)
    sFilename = Path(sFilename_json).stem + '_basins.json'
    sFilename_basins_json = os.path.join(sDirname, sFilename)

    aBasin = create_basin_template_configuration_file(
        sFilename_basins_json,
        config.get("nOutlet", 1))

    # Set up model relationships
    oPyflowline.sFilename_basins = sFilename_basins_json
    oPyflowline.aBasin = aBasin
    oPyhexwatershed.pPyFlowline = oPyflowline
    oPyhexwatershed.sFilename_basins = sFilename_basins_json

    # Export configuration
    oPyhexwatershed.pyhexwatershed_export_config_to_json(sFilename_json, iFlag_export_basin_in=0)

    return oPyhexwatershed

