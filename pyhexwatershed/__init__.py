"""PyHexWatershed: A mesh-independent flow direction model for hydrologic models."""

from __future__ import annotations

import sys

from pyhexwatershed import configuration
from pyhexwatershed import configuration as config
from pyhexwatershed.configuration import (
    create_model_configuration,
    create_workflow,
    load_configuration,
    load_pyhexwatershed_config,
    load_workflow_config,
    pyhexwatershed_read_configuration_file,
    pyhexwatershed_read_model_configuration_file,
)

# Cross-project module aliases (matching pyearthmesh.config and pyflowline.config)
sys.modules.setdefault("pyhexwatershed.config", configuration)
sys.modules.setdefault("pyhexwatershed.config.config_manager", configuration.config_manager)

# Legacy submodule import compatibility
sys.modules.setdefault("pyhexwatershed.pyhexwatershed_read_model_configuration_file", configuration)
sys.modules.setdefault("pyhexwatershed.pyhexwatershed_read_configuration_file", configuration)

__all__ = [
    "configuration",
    "config",
    "load_configuration",
    "load_workflow_config",
    "load_pyhexwatershed_config",
    "create_model_configuration",
    "create_workflow",
    "pyhexwatershed_read_configuration_file",
    "pyhexwatershed_read_model_configuration_file",
]
