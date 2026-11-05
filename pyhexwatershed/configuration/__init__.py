"""Configuration management for PyHexWatershed.

Supports YAML (primary, comment-enabled, user-friendly) and JSON (programmatic,
backward-compatible) configuration files for case and basin setups.

All configuration management, path discovery, workflow compilation, and model
loading functions are centralized in ``config_manager.py`` (matching the pyflowline
and pyearthmesh architecture).
"""

from __future__ import annotations

import sys

from pyhexwatershed.configuration import config_manager
from pyhexwatershed.configuration.config_manager import (
    DEFAULT_BASIN_CONFIG,
    DEFAULT_HEXWATERSHED_CONFIG,
    BasinConfigManager,
    HexwatershedConfigManager,
    WorkflowSpec,
    change_config_key_value,
    change_json_key_value,
    compile_workflow,
    create_basin_template_configuration_file,
    create_hexwatershed_template_configuration_file,
    create_model_configuration,
    create_workflow,
    dump_pyhexwatershed_config,
    dump_workflow_config,
    join_project_path,
    load_configuration,
    load_pyhexwatershed_config,
    load_workflow_config,
    package_root,
    path_manager,
    project_root,
    pyhexwatershed_create_template_configuration_file,
    pyhexwatershed_package_root,
    pyhexwatershed_project_root,
    pyhexwatershed_read_configuration_file,
    pyhexwatershed_read_model_configuration_file,
    root_path_from_path_manager_location,
    root_path_from_pyhexwatershed_package_root,
    root_path_from_setup_file,
)

# Backwards-compatibility module shims for legacy submodule imports
sys.modules.setdefault("pyhexwatershed.configuration.config_manager", config_manager)
sys.modules.setdefault("pyhexwatershed.configuration.path_manager", config_manager)
sys.modules.setdefault("pyhexwatershed.configuration.read_configuration_file", config_manager)
sys.modules.setdefault("pyhexwatershed.configuration.change_config_key_value", config_manager)
sys.modules.setdefault("pyhexwatershed.configuration.change_json_key_value", config_manager)
sys.modules.setdefault(
    "pyhexwatershed.configuration.create_template_configuration_file", config_manager
)

__all__ = [
    "BasinConfigManager",
    "HexwatershedConfigManager",
    "WorkflowSpec",
    "compile_workflow",
    "create_workflow",
    "load_configuration",
    "load_pyhexwatershed_config",
    "load_workflow_config",
    "dump_pyhexwatershed_config",
    "dump_workflow_config",
    "pyhexwatershed_read_configuration_file",
    "pyhexwatershed_read_model_configuration_file",
    "create_basin_template_configuration_file",
    "create_hexwatershed_template_configuration_file",
    "create_model_configuration",
    "pyhexwatershed_create_template_configuration_file",
    "change_json_key_value",
    "change_config_key_value",
    "DEFAULT_BASIN_CONFIG",
    "DEFAULT_HEXWATERSHED_CONFIG",
    "config_manager",
    "path_manager",
    "join_project_path",
    "package_root",
    "project_root",
    "pyhexwatershed_project_root",
    "pyhexwatershed_package_root",
    "root_path_from_setup_file",
    "root_path_from_pyhexwatershed_package_root",
    "root_path_from_path_manager_location",
]
