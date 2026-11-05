"""Unified Configuration Manager for PyHexWatershed.

Single-source configuration, path resolution, two-tier compiler,
and workflow factory supporting both YAML (primary, comment-enabled)
and JSON (programmatic, backward-compatible) configuration formats.

Standardized following the Unified Configuration Architecture Pattern Guide.
"""

from __future__ import annotations

import datetime
import importlib.resources as importlib_resources
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

try:
    import yaml

    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# ==============================================================================
# 1. Project & Package Path Resolution (formerly path_manager)
# ==============================================================================


def pyhexwatershed_package_root(package_name: str = "pyhexwatershed") -> Path:
    """Get the installation root directory of the package."""
    try:
        return Path(str(importlib_resources.files(package_name))).resolve()
    except Exception:
        return Path(__file__).resolve().parents[1]


def root_path_from_setup_file() -> Path:
    """Return top-level project root by searching upward for setup.py or pyproject.toml."""
    this_path = Path(__file__).resolve()
    for parent in this_path.parents:
        if (parent / "setup.py").exists() or (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Project root marker (setup.py or pyproject.toml) not found.")


def root_path_from_pyhexwatershed_package_root() -> Path:
    """Get parent directory of the pyhexwatershed package root."""
    return pyhexwatershed_package_root().parent


def root_path_from_path_manager_location() -> Path:
    """Return top-level root path assuming fixed directory layout:
    root_path/pyhexwatershed/configuration/config_manager.py
    """
    return Path(__file__).resolve().parents[2]


def pyhexwatershed_project_root() -> Path:
    """Find repository root by searching upward for project marker files."""
    try:
        return root_path_from_setup_file()
    except FileNotFoundError:
        return root_path_from_pyhexwatershed_package_root()
    except Exception as exc:
        raise RuntimeError(
            f"An unexpected error occurred while locating the project root: {exc}"
        ) from exc


package_root = pyhexwatershed_package_root
project_root = pyhexwatershed_project_root


def join_project_path(*args: str) -> Path:
    """Join components of a path relative to the project root."""
    return pyhexwatershed_project_root().joinpath(*args)


class _PathManagerNamespace:
    """Backwards-compatible path_manager namespace object."""

    pyhexwatershed_project_root = staticmethod(pyhexwatershed_project_root)
    pyhexwatershed_package_root = staticmethod(pyhexwatershed_package_root)
    join_project_path = staticmethod(join_project_path)
    root_path_from_setup_file = staticmethod(root_path_from_setup_file)
    root_path_from_pyhexwatershed_package_root = staticmethod(
        root_path_from_pyhexwatershed_package_root
    )
    root_path_from_path_manager_location = staticmethod(root_path_from_path_manager_location)


path_manager = _PathManagerNamespace()


# ==============================================================================
# 2. Default Configuration Dictionaries
# ==============================================================================

DEFAULT_BASIN_CONFIG: dict[str, Any] = {
    "lBasinID": 1,
    "dLatitude_outlet_degree": -180.0,
    "dLongitude_outlet_degree": 180.0,
    "dAccumulation_threshold": 100000.0,
    "dThreshold_small_river": 10000.0,
    "iFlag_dam": 0,
    "iFlag_debug": 0,
    "iFlag_disconnected": 0,
    "sFilename_dam": "ICoM_dams.csv",
    "sFilename_flowline_filter": "streamord7above.shp",
    "sFilename_flowline_raw": "allflowline.shp",
    "sFilename_flowline_topo": "flowline.csv",
    "sWorkspace_output_basin": "",
}

DEFAULT_HEXWATERSHED_CONFIG: dict[str, Any] = {
    "iFlag_profile": 0,
    "iFlag_resample_method": 2,
    "iFlag_flowline": 1,
    "iFlag_global": 0,
    "iFlag_antarctic": 0,
    "iFlag_multiple_outlet": 0,
    "iFlag_elevation_profile": 0,
    "iFlag_stream_burning_topology": 1,
    "iFlag_create_mesh": 1,
    "iFlag_mesh_boundary": 0,
    "iFlag_force_watershed_boundary": 0,
    "iFlag_simplification": 1,
    "iFlag_intersect": 1,
    "iFlag_merge_reach": 1,
    "iMesh_type": 1,
    "iFlag_save_mesh": 1,
    "iFlag_use_mesh_dem": 0,
    "iFlag_user_provided_binary": 0,
    "iFlag_slurm": 0,
    "iFlag_rotation": 0,
    "iFlag_save_elevation": 1,
    "iFlag_use_shapefile_extent": 0,
    "nOutlet": 1,
    "iCase_index": 1,
    "iResolution_index": 10,
    "dResolution_degree": 0.5,
    "dResolution_meter": 50000.0,
    "dThreshold_small_river": 0.0,
    "dAccumulation_threshold": 100000.0,
    "dMissing_value_dem": -9999.0,
    "dBreach_threshold": 10.0,
    "dLongitude_left": -180.0,
    "dLongitude_right": 180.0,
    "dLatitude_bot": -90.0,
    "dLatitude_top": 90.0,
    "sRegion": "susquehanna",
    "sModel": "pyhexwatershed",
    "sMesh_type": "hexagon",
    "sJob": "hexwatershed",
    "sDate": "20220202",
    "sDggrid_type": "ISEA3H",
    "flowline_info": "flowline_info.json",
    "sFilename_mesh_info": "mesh_info.json",
    "sFilename_elevation": "elevation.geojson",
    "sWorkspace_input": "",
    "sWorkspace_output": "./output",
    "sWorkspace_data": "",
    "sWorkspace_project": "",
    "sWorkspace_bin": "",
    "sFilename_model_configuration": "",
    "sFilename_spatial_reference": "",
    "sFilename_dem": "",
    "sFilename_mesh_netcdf": "",
    "sFilename_mesh_boundary": "",
    "sFilename_basins": "",
    "sFilename_hexwatershed": "hexwatershed",
    "sFilename_hexwatershed_bin": "",
}


# ==============================================================================
# 3. Path Resolution & Discovery Helpers
# ==============================================================================


def _select_platform_path(value: Any) -> str:
    """Resolve platform-specific dictionary or string path."""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        raise ValueError("Path values must be strings or platform-specific mappings")

    current_platform = platform.system()  # 'Darwin', 'Linux', 'Windows'
    selected = value.get(current_platform, value.get("default", ""))
    if not isinstance(selected, str):
        raise ValueError(f"Path for {current_platform} must be a string")
    return selected


def _resolve_config_path(
    filename: str | Path,
    candidates: tuple[str, ...] = (
        "pyhexwatershed_config.yaml",
        "pyhexwatershed_config.yml",
        "workflow_config.yaml",
        "workflow_config.yml",
        "configuration.yaml",
        "configuration.yml",
        "pyhexwatershed_config.json",
        "workflow_config.json",
        "configuration.json",
    ),
) -> Path:
    """Resolve configuration file path handling directories and missing extensions."""
    path = Path(filename).expanduser().resolve()
    if path.is_dir():
        for candidate_name in candidates:
            candidate = path / candidate_name
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(
            f"No configuration file found in directory: {path}. Candidates checked: {candidates}"
        )
    if not path.is_file():
        for ext in (".yaml", ".yml", ".json"):
            candidate = path.with_suffix(ext)
            if candidate.is_file():
                return candidate
    return path


def _parse_config_file(path: Path) -> Any:
    """Parse YAML or JSON configuration file, seamlessly allowing comments."""
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    ext = path.suffix.lower()
    if ext in (".yaml", ".yml"):
        if not HAVE_YAML:
            raise ImportError(
                "PyYAML is required to parse YAML configuration files. "
                "Please install pyyaml with `pip install pyyaml` or `conda install pyyaml`."
            )
        with path.open(encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    elif ext == ".json":
        with path.open(encoding="utf-8") as f:
            raw = json.load(f)
    else:
        # Fallback: attempt YAML first (accepts JSON syntax and comments), then JSON
        try:
            if HAVE_YAML:
                with path.open(encoding="utf-8") as f:
                    raw = yaml.safe_load(f)
            else:
                with path.open(encoding="utf-8") as f:
                    raw = json.load(f)
        except Exception:
            with path.open(encoding="utf-8") as f:
                raw = json.load(f)

    if raw is None:
        raw = {}
    return raw


def _clean_for_export(obj: Any) -> Any:
    """Recursively convert Path/numpy objects to strings/scalars and exclude internal objects."""
    import numpy as np

    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {
            k: _clean_for_export(v)
            for k, v in obj.items()
            if k
            not in (
                "config_file",
                "pPyFlowline",
                "aBasin",
                "aFlowline_simplified",
                "aFlowline_conceptual",
                "aCellID_outlet",
                "aCell",
                "pRTree_mesh",
                "pRTree_flowline",
                "pRTree_edge",
            )
        }
    if isinstance(obj, list):
        return [_clean_for_export(v) for v in obj]
    return obj


def _dump_config_file(data: Any, path: Path, fmt: str | None = None) -> None:
    """Dump data to a YAML or JSON file."""
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    if fmt is None:
        ext = path.suffix.lower()
        if ext in (".yaml", ".yml"):
            fmt = "yaml"
        elif ext == ".json":
            fmt = "json"
        else:
            fmt = "yaml"
    else:
        fmt = fmt.lower()

    cleaned = _clean_for_export(data)

    if fmt in ("yaml", "yml"):
        if not HAVE_YAML:
            raise ImportError(
                "PyYAML is required to write YAML configuration files. "
                "Please install pyyaml with `pip install pyyaml`."
            )
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(cleaned, f, sort_keys=False, default_flow_style=False)
    elif fmt == "json":
        with path.open("w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=4)
    else:
        raise ValueError(f"Unsupported configuration format {fmt!r}. Expected 'yaml' or 'json'.")


def _normalize_basin_dict(basin: dict[str, Any]) -> dict[str, Any]:
    """Normalize a basin dictionary from either sectioned YAML or flat keys."""
    res = DEFAULT_BASIN_CONFIG.copy()

    # Direct flat keys if provided
    for key, val in basin.items():
        if key in res:
            res[key] = val

    # Sectioned / friendly aliases
    if "id" in basin:
        res["lBasinID"] = int(basin["id"])
    if "basin_id" in basin:
        res["lBasinID"] = int(basin["basin_id"])

    outlet = basin.get("outlet", {})
    if isinstance(outlet, dict):
        if "longitude" in outlet:
            res["dLongitude_outlet_degree"] = float(outlet["longitude"])
        if "latitude" in outlet:
            res["dLatitude_outlet_degree"] = float(outlet["latitude"])

    if "accumulation_threshold" in basin:
        res["dAccumulation_threshold"] = float(basin["accumulation_threshold"])
    if "small_river_threshold" in basin:
        res["dThreshold_small_river"] = float(basin["small_river_threshold"])
    if "small_river" in basin:
        res["dThreshold_small_river"] = float(basin["small_river"])

    flags = basin.get("flags", {})
    if isinstance(flags, dict):
        if "dam" in flags:
            res["iFlag_dam"] = int(flags["dam"])
        if "debug" in flags:
            res["iFlag_debug"] = int(flags["debug"])
        if "disconnected" in flags:
            res["iFlag_disconnected"] = int(flags["disconnected"])

    paths = basin.get("paths", {})
    if isinstance(paths, dict):
        if "dam" in paths:
            res["sFilename_dam"] = _select_platform_path(paths["dam"])
        if "flowline_filter" in paths:
            res["sFilename_flowline_filter"] = _select_platform_path(paths["flowline_filter"])
        if "flowline_raw" in paths:
            res["sFilename_flowline_raw"] = _select_platform_path(paths["flowline_raw"])
        if "flowline_topo" in paths:
            res["sFilename_flowline_topo"] = _select_platform_path(paths["flowline_topo"])
        if "output_basin" in paths:
            res["sWorkspace_output_basin"] = _select_platform_path(paths["output_basin"])

    return res


# ==============================================================================
# 4. Two-Tier Compiler Boundary (WorkflowSpec & compile_workflow)
# ==============================================================================


class WorkflowSpec:
    """Mesh-agnostic front-end specification for a pyhexwatershed run.

    Tier 1 of the Two-Tier Compiler Pattern: captures user intent in a clean,
    human-readable structure without requiring backend-internal parameter names.
    """

    def __init__(
        self,
        mesh_type: str = "hexagon",
        case_index: int = 1,
        date: str | None = None,
        model: str = "pyhexwatershed",
        job: str | None = None,
        region: dict[str, Any] | None = None,
        resolutions: dict[str, Any] | None = None,
        paths: dict[str, Any] | None = None,
        flags: dict[str, Any] | None = None,
        basins: list[dict[str, Any]] | None = None,
    ):
        self.mesh_type = str(mesh_type).lower()
        self.case_index = int(case_index)
        self.date = date
        self.model = model
        self.job = job or "hexwatershed"
        self.region = dict(region or {})
        self.resolutions = dict(resolutions or {})
        self.paths = dict(paths or {})
        self.flags = dict(flags or {})
        self.basins = list(basins or [])

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkflowSpec:
        workflow = data.get("workflow", {}) or {}
        return cls(
            mesh_type=workflow.get("mesh_type", data.get("sMesh_type", "hexagon")),
            case_index=workflow.get("case_index", data.get("iCase_index", 1)),
            date=workflow.get("date", data.get("sDate")),
            model=workflow.get("model", data.get("sModel", "pyhexwatershed")),
            job=workflow.get("job", data.get("sJob")),
            region=data.get("region", {}),
            resolutions=data.get("resolutions", {}),
            paths=data.get("paths", {}),
            flags=data.get("flags", {}),
            basins=data.get("basins", []),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow": {
                "mesh_type": self.mesh_type,
                "case_index": self.case_index,
                "date": self.date,
                "model": self.model,
                "job": self.job,
            },
            "resolutions": self.resolutions,
            "region": self.region,
            "paths": self.paths,
            "flags": self.flags,
            "basins": self.basins,
        }


def compile_workflow(spec_or_config: dict[str, Any] | WorkflowSpec) -> dict[str, Any]:
    """Compile Tier 1 workflow specification into backend-native pyhexwatershed configuration.

    Supports both sectioned Tier 1 configurations ('workflow', 'resolutions',
    'region', 'paths', 'flags', 'basins') and flat native dictionaries.
    """
    if isinstance(spec_or_config, WorkflowSpec):
        raw = spec_or_config.to_dict()
    elif isinstance(spec_or_config, dict):
        raw = spec_or_config
    else:
        raise TypeError("spec_or_config must be a dictionary or WorkflowSpec")

    # Start with default configuration
    native = DEFAULT_HEXWATERSHED_CONFIG.copy()

    # Pass through any existing top-level native keys (for backward compatibility)
    for k, v in raw.items():
        if k in native:
            native[k] = v

    # Section 1: workflow
    workflow = raw.get("workflow", {})
    if isinstance(workflow, dict) and workflow:
        if "mesh_type" in workflow:
            native["sMesh_type"] = str(workflow["mesh_type"]).lower()
        if "case_index" in workflow:
            native["iCase_index"] = int(workflow["case_index"])
        if "date" in workflow and workflow["date"]:
            native["sDate"] = str(workflow["date"])
        if "model" in workflow:
            native["sModel"] = str(workflow["model"])
        if "job" in workflow:
            native["sJob"] = str(workflow["job"])
        elif "sJob" not in native or not native["sJob"]:
            native["sJob"] = "hexwatershed"
        if "region" in workflow:
            native["sRegion"] = str(workflow["region"])
        if "dggrid_type" in workflow:
            native["sDggrid_type"] = str(workflow["dggrid_type"])
        if "outlets" in workflow:
            native["nOutlet"] = int(workflow["outlets"])
        elif "nOutlet" in workflow:
            native["nOutlet"] = int(workflow["nOutlet"])

    # Section 2: resolutions
    resolutions = raw.get("resolutions", {})
    if isinstance(resolutions, dict) and resolutions:
        if "degree" in resolutions and resolutions["degree"] is not None:
            native["dResolution_degree"] = float(resolutions["degree"])
        if "meter" in resolutions and resolutions["meter"] is not None:
            native["dResolution_meter"] = float(resolutions["meter"])
        if "resolution_index" in resolutions and resolutions["resolution_index"] is not None:
            native["iResolution_index"] = int(resolutions["resolution_index"])
        if (
            "accumulation_threshold" in resolutions
            and resolutions["accumulation_threshold"] is not None
        ):
            native["dAccumulation_threshold"] = float(resolutions["accumulation_threshold"])
        if (
            "small_river_threshold" in resolutions
            and resolutions["small_river_threshold"] is not None
        ):
            native["dThreshold_small_river"] = float(resolutions["small_river_threshold"])
        elif "small_river" in resolutions and resolutions["small_river"] is not None:
            native["dThreshold_small_river"] = float(resolutions["small_river"])
        if "missing_value_dem" in resolutions and resolutions["missing_value_dem"] is not None:
            native["dMissing_value_dem"] = float(resolutions["missing_value_dem"])
        if "breach_threshold" in resolutions and resolutions["breach_threshold"] is not None:
            native["dBreach_threshold"] = float(resolutions["breach_threshold"])

    # Section 3: region
    region = raw.get("region", {})
    if isinstance(region, dict) and region:
        if "name" in region and region["name"]:
            native["sRegion"] = str(region["name"])

        bbox = region.get("bbox", {})
        if isinstance(bbox, dict):
            if "left" in bbox:
                native["dLongitude_left"] = float(bbox["left"])
            if "right" in bbox:
                native["dLongitude_right"] = float(bbox["right"])
            if "bottom" in bbox:
                native["dLatitude_bot"] = float(bbox["bottom"])
            if "top" in bbox:
                native["dLatitude_top"] = float(bbox["top"])

        for k_src, k_dst in (
            ("longitude_left", "dLongitude_left"),
            ("longitude_right", "dLongitude_right"),
            ("latitude_bot", "dLatitude_bot"),
            ("latitude_bottom", "dLatitude_bot"),
            ("latitude_top", "dLatitude_top"),
        ):
            if k_src in region and region[k_src] is not None:
                native[k_dst] = float(region[k_src])

        outlet = region.get("outlet", {})
        if isinstance(outlet, dict):
            if "longitude" in outlet:
                native["dLongitude_outlet_degree"] = float(outlet["longitude"])
            if "latitude" in outlet:
                native["dLatitude_outlet_degree"] = float(outlet["latitude"])
        elif "dLongitude_outlet_degree" in region:
            native["dLongitude_outlet_degree"] = float(region["dLongitude_outlet_degree"])
            native["dLatitude_outlet_degree"] = float(region["dLatitude_outlet_degree"])

    # Section 4: flags
    flags = raw.get("flags", {})
    if isinstance(flags, dict) and flags:
        flag_map = {
            "create_mesh": "iFlag_create_mesh",
            "save_mesh": "iFlag_save_mesh",
            "simplification": "iFlag_simplification",
            "intersect": "iFlag_intersect",
            "flowline": "iFlag_flowline",
            "use_mesh_dem": "iFlag_use_mesh_dem",
            "rotation": "iFlag_rotation",
            "stream_burning_topology": "iFlag_stream_burning_topology",
            "resample_method": "iFlag_resample_method",
            "global": "iFlag_global",
            "multiple_outlet": "iFlag_multiple_outlet",
            "elevation_profile": "iFlag_elevation_profile",
            "save_elevation": "iFlag_save_elevation",
            "profile": "iFlag_profile",
            "antarctic": "iFlag_antarctic",
            "mesh_boundary": "iFlag_mesh_boundary",
            "force_watershed_boundary": "iFlag_force_watershed_boundary",
            "merge_reach": "iFlag_merge_reach",
            "user_provided_binary": "iFlag_user_provided_binary",
            "slurm": "iFlag_slurm",
            "use_shapefile_extent": "iFlag_use_shapefile_extent",
        }
        for flag_k, native_k in flag_map.items():
            if flag_k in flags and flags[flag_k] is not None:
                native[native_k] = int(flags[flag_k])

    # Section 5: paths
    paths = raw.get("paths", {})
    if isinstance(paths, dict) and paths:
        path_map = {
            "workspace_input": "sWorkspace_input",
            "workspace_output": "sWorkspace_output",
            "workspace_data": "sWorkspace_data",
            "workspace_project": "sWorkspace_project",
            "workspace_bin": "sWorkspace_bin",
            "spatial_reference": "sFilename_spatial_reference",
            "dem": "sFilename_dem",
            "mesh_netcdf": "sFilename_mesh_netcdf",
            "mesh_boundary": "sFilename_mesh_boundary",
            "basins": "sFilename_basins",
            "hexwatershed": "sFilename_hexwatershed",
            "hexwatershed_bin": "sFilename_hexwatershed_bin",
            "flowline_info": "flowline_info",
            "mesh_info": "sFilename_mesh_info",
            "elevation": "sFilename_elevation",
            "model_configuration": "sFilename_model_configuration",
        }
        for path_k, native_k in path_map.items():
            if path_k in paths and paths[path_k] is not None:
                native[native_k] = _select_platform_path(paths[path_k])

        for k, v in paths.items():
            if k.startswith("sFilename_") or k.startswith("sWorkspace_"):
                native[k] = _select_platform_path(v)

        # If hexwatershed was provided as a path to a binary and hexwatershed_bin wasn't given
        if ("hexwatershed" in paths and paths["hexwatershed"] is not None) and (
            "hexwatershed_bin" not in paths or paths["hexwatershed_bin"] is None
        ):
            hw_val = native.get("sFilename_hexwatershed", "")
            if "/" in hw_val or "\\" in hw_val or os.path.isabs(hw_val):
                native["sFilename_hexwatershed_bin"] = hw_val

        # Automatically enable user_provided_binary when a binary path is configured
        if native.get("sFilename_hexwatershed_bin"):
            if "user_provided_binary" not in flags and "iFlag_user_provided_binary" not in flags:
                native["iFlag_user_provided_binary"] = 1

    # Section 6: basins (inline list or single dict of basin specifications)
    basins = raw.get("basins") or raw.get("aBasin")
    if basins:
        if isinstance(basins, dict):
            basins = [basins]
        if isinstance(basins, list):
            compiled_basins = [_normalize_basin_dict(b) for b in basins if isinstance(b, dict)]
            native["aBasin"] = compiled_basins
            native["nOutlet"] = len(compiled_basins)
            if len(compiled_basins) > 1:
                native["iFlag_multiple_outlet"] = 1

    # Date normalization
    if not native.get("sDate"):
        pDate = datetime.datetime.today()
        native["sDate"] = f"{pDate.year:04d}{pDate.month:02d}{pDate.day:02d}"

    # Map mesh type string to mesh type integer code if needed
    mesh_type_str = str(native.get("sMesh_type", "hexagon")).lower()
    mesh_map = {
        "hexagon": 1,
        "square": 2,
        "latlon": 3,
        "mpas": 4,
        "dggrid": 5,
        "tin": 6,
    }
    native["iMesh_type"] = mesh_map.get(mesh_type_str, 1)

    # Carry forward config_file reference if present
    if "config_file" in raw:
        native["config_file"] = raw["config_file"]
        native["sFilename_model_configuration"] = str(raw["config_file"])

    return native


# ==============================================================================
# 5. Loader & Workflow Factory
# ==============================================================================


def load_pyhexwatershed_config(filename: str | Path) -> dict[str, Any]:
    """Load a workflow YAML or JSON file, apply defaults, and resolve paths.

    Features:
        - Primary format: YAML (.yaml, .yml) with inline/block comments (#)
        - Full backward compatibility with JSON (.json)
        - Directory discovery (checks for default configuration names)
        - Extensionless stem resolution (.yaml -> .yml -> .json)
        - Relative path resolution against config file location
        - Platform-specific path mapping resolution (Linux, Darwin, Windows, default)
    """
    resolved_path = _resolve_config_path(filename)
    raw_dict = _parse_config_file(resolved_path)

    if not isinstance(raw_dict, dict):
        raise ValueError(f"Configuration in {resolved_path} must be a dictionary / mapping object")

    raw_dict["config_file"] = resolved_path

    # Compile into native dictionary
    config = compile_workflow(raw_dict)

    # Resolve relative paths relative to configuration file directory
    base_dir = resolved_path.parent
    path_keys = [
        "sWorkspace_input",
        "sWorkspace_output",
        "sWorkspace_data",
        "sWorkspace_project",
        "sWorkspace_bin",
        "sFilename_spatial_reference",
        "sFilename_dem",
        "sFilename_mesh_netcdf",
        "sFilename_mesh_boundary",
        "sFilename_basins",
        "sFilename_hexwatershed_bin",
    ]

    for key in path_keys:
        val = config.get(key)
        if val and isinstance(val, str) and not os.path.isabs(val):
            config[key] = str((base_dir / val).resolve())

    # If inline basins are present, resolve relative paths inside each basin
    if "aBasin" in config and isinstance(config["aBasin"], list):
        basin_path_keys = [
            "sFilename_dam",
            "sFilename_flowline_filter",
            "sFilename_flowline_raw",
            "sFilename_flowline_topo",
            "sWorkspace_output_basin",
        ]
        for b in config["aBasin"]:
            if isinstance(b, dict):
                for bk in basin_path_keys:
                    b_val = b.get(bk)
                    if b_val and isinstance(b_val, str) and not os.path.isabs(b_val):
                        b[bk] = str((base_dir / b_val).resolve())

    # If external basins file is referenced and nOutlet wasn't explicitly configured, inspect basin count
    workflow_raw = (
        raw_dict.get("workflow", {}) if isinstance(raw_dict.get("workflow"), dict) else {}
    )
    if (
        config.get("sFilename_basins")
        and not workflow_raw.get("outlets")
        and not workflow_raw.get("nOutlet")
    ):
        try:
            basin_file = Path(config["sFilename_basins"])
            if basin_file.is_file():
                basin_records = BasinConfigManager.load_config(basin_file)
                if isinstance(basin_records, list) and len(basin_records) > 0:
                    config["nOutlet"] = len(basin_records)
                    if len(basin_records) > 1:
                        config["iFlag_multiple_outlet"] = 1
        except Exception:
            pass

    return config


# Unified aliases
load_workflow_config = load_pyhexwatershed_config


def dump_pyhexwatershed_config(
    config: dict[str, Any],
    filename: str | Path,
    fmt: str | None = None,
) -> None:
    """Dump a configuration dictionary to a YAML or JSON file."""
    _dump_config_file(config, Path(filename), fmt=fmt)


dump_workflow_config = dump_pyhexwatershed_config


def pyhexwatershed_read_configuration_file(
    sFilename_configuration_in: str | Path,
    iCase_index_in: int | None = None,
    iFlag_stream_burning_topology_in: int | None = None,
    iFlag_elevation_profile_in: int | None = None,
    iFlag_use_mesh_dem_in: int | None = None,
    iFlag_force_watershed_boundary_in: int | None = None,
    iResolution_index_in: int | None = None,
    dResolution_degree_in: float | None = None,
    dResolution_meter_in: float | None = None,
    sDate_in: str | None = None,
    sDggrid_type_in: str | None = None,
    sMesh_type_in: str | None = None,
    sModel_in: str | None = None,
    sWorkspace_output_in: str | Path | None = None,
    **kwargs: Any,
) -> Any:
    """Read a PyHexWatershed model configuration from YAML or JSON.

    Supports:
        - YAML (.yaml / .yml) with comments (#)
        - JSON (.json) for backward compatibility
        - Extensionless file paths and directory paths
        - Two-tier sectioned specification or legacy flat dictionary
        - Runtime parameter overrides (both legacy *_in arguments and general kwargs)

    Returns:
        hexwatershedcase: Instantiated and configured hexwatershedcase object.
    """
    from pyflowline.classes.basin import pybasin
    from pyflowline.classes.pycase import flowlinecase

    from pyhexwatershed.classes.pycase import hexwatershedcase

    resolved_path = _resolve_config_path(sFilename_configuration_in)

    if not resolved_path.is_file():
        raise FileNotFoundError(f"Configuration file does not exist: {sFilename_configuration_in}")

    aConfig: dict[str, Any] = load_pyhexwatershed_config(resolved_path)

    # Runtime argument overrides (legacy named arguments)
    if iCase_index_in is not None:
        aConfig["iCase_index"] = int(iCase_index_in)
    if iFlag_stream_burning_topology_in is not None:
        aConfig["iFlag_stream_burning_topology"] = int(iFlag_stream_burning_topology_in)
    if iFlag_elevation_profile_in is not None:
        aConfig["iFlag_elevation_profile"] = int(iFlag_elevation_profile_in)
    if iFlag_use_mesh_dem_in is not None:
        aConfig["iFlag_use_mesh_dem"] = int(iFlag_use_mesh_dem_in)
    if iFlag_force_watershed_boundary_in is not None:
        aConfig["iFlag_force_watershed_boundary"] = int(iFlag_force_watershed_boundary_in)
    if iResolution_index_in is not None:
        aConfig["iResolution_index"] = int(iResolution_index_in)
    if dResolution_degree_in is not None:
        aConfig["dResolution_degree"] = float(dResolution_degree_in)
    if dResolution_meter_in is not None:
        aConfig["dResolution_meter"] = float(dResolution_meter_in)
    if sDate_in is not None:
        aConfig["sDate"] = str(sDate_in)
    if sDggrid_type_in is not None:
        aConfig["sDggrid_type"] = str(sDggrid_type_in)
    if sMesh_type_in is not None:
        aConfig["sMesh_type"] = str(sMesh_type_in).lower()
    if sModel_in is not None:
        aConfig["sModel"] = str(sModel_in)
    if sWorkspace_output_in is not None:
        aConfig["sWorkspace_output"] = str(sWorkspace_output_in)

    # General kwargs overrides (allowing modern parameter names)
    alias_map = {
        "mesh_type": "sMesh_type",
        "case_index": "iCase_index",
        "date": "sDate",
        "resolution_meter": "dResolution_meter",
        "resolution": "dResolution_meter",
        "resolution_degree": "dResolution_degree",
        "workspace_output": "sWorkspace_output",
        "workspace_input": "sWorkspace_input",
        "force_watershed_boundary": "iFlag_force_watershed_boundary",
    }
    for k, v in kwargs.items():
        if v is not None:
            target_key = alias_map.get(k, k)
            if target_key.endswith("_in"):
                target_key = target_key[:-3]
            aConfig[target_key] = v

    sWorkspace_output = aConfig.get("sWorkspace_output", "./output")
    try:
        Path(sWorkspace_output).mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print(f"Warning: Could not create output workspace {sWorkspace_output}: {exc}")

    aConfig["sFilename_model_configuration"] = str(resolved_path)

    # Instantiate case objects
    oPyhexwatershed = hexwatershedcase(aConfig)
    oPyflowline = flowlinecase(
        aConfig,
        iFlag_standalone_in=0,
        sModel_in="pyflowline",
        sWorkspace_output_in=oPyhexwatershed.sWorkspace_output_pyflowline,
    )

    oPyhexwatershed.dResolution_meter = oPyflowline.dResolution_meter
    oPyhexwatershed.pPyFlowline = oPyflowline
    oPyhexwatershed.aBasin.clear()

    # Load basins (supports inline list, external YAML, external JSON, or fallback)
    basins_data: list[dict[str, Any]] | None = None
    if "aBasin" in aConfig and isinstance(aConfig["aBasin"], list) and len(aConfig["aBasin"]) > 0:
        basins_data = aConfig["aBasin"]
    elif (
        oPyhexwatershed.iFlag_flowline == 1
        and oPyhexwatershed.sFilename_basins
        and os.path.exists(oPyhexwatershed.sFilename_basins)
    ):
        raw_basins = BasinConfigManager.load_config(oPyhexwatershed.sFilename_basins)
        if isinstance(raw_basins, list):
            basins_data = raw_basins
        elif isinstance(raw_basins, dict):
            basins_data = [raw_basins]

    #hexwatershed model has it own basin workspace output path
    if basins_data:
        n_outlets = oPyhexwatershed.nOutlet if oPyhexwatershed.nOutlet > 0 else len(basins_data)
        n_basins = min(len(basins_data), n_outlets)
        for i in range(n_basins):
            sBasin = f"{i + 1:08d}"
            dummy_basin = dict(basins_data[i])
            dummy_basin["sWorkspace_output_basin"] = str(
                Path(oPyhexwatershed.sWorkspace_output_hexwatershed) / sBasin
            )
            pBasin = pybasin(dummy_basin)
            oPyhexwatershed.aBasin.append(pBasin)
    else:
        # Fallback to single default basin
        sBasin = f"{1:08d}"
        dummy_basin = dict()
        dummy_basin["sWorkspace_output_basin"] = str(
            Path(oPyhexwatershed.sWorkspace_output_hexwatershed) / sBasin
        )
        pBasin = pybasin(dummy_basin)
        oPyhexwatershed.aBasin.append(pBasin)


    oPyflowline.nOutlet = len(oPyhexwatershed.aBasin)

    return oPyhexwatershed


# Unified cross-project aliases
load_configuration = pyhexwatershed_read_configuration_file
pyhexwatershed_read_model_configuration_file = pyhexwatershed_read_configuration_file


def create_workflow(config_or_path: str | Path | dict[str, Any], **kwargs: Any) -> Any:
    """Factory function: load configuration and return instantiated hexwatershedcase."""
    if isinstance(config_or_path, (str, Path)):
        return load_configuration(config_or_path, **kwargs)
    elif isinstance(config_or_path, WorkflowSpec):
        config = compile_workflow(config_or_path)
    elif isinstance(config_or_path, dict):
        if "workflow" in config_or_path or "resolutions" in config_or_path:
            config = compile_workflow(config_or_path)
        else:
            config = config_or_path.copy()
    else:
        raise TypeError("config_or_path must be a path string, Path, dict, or WorkflowSpec")

    # Apply any kwargs overrides
    for k, v in kwargs.items():
        if v is not None:
            config[k] = v

    # Pass in-memory config through load_configuration by temporary export or direct construction
    from pyflowline.classes.basin import pybasin
    from pyflowline.classes.pycase import flowlinecase

    from pyhexwatershed.classes.pycase import hexwatershedcase

    sWorkspace_output = config.get("sWorkspace_output", "./output")
    Path(sWorkspace_output).mkdir(parents=True, exist_ok=True)

    oPyhexwatershed = hexwatershedcase(config)
    oPyflowline = flowlinecase(
        config,
        iFlag_standalone_in=0,
        sModel_in="pyflowline",
        sWorkspace_output_in=oPyhexwatershed.sWorkspace_output_pyflowline,
    )
    oPyhexwatershed.dResolution_meter = oPyflowline.dResolution_meter
    oPyhexwatershed.pPyFlowline = oPyflowline
    oPyhexwatershed.aBasin.clear()

    #hexwatershed model has it own basin workspace output path
    basins_data = config.get("aBasin")
    if basins_data and isinstance(basins_data, list):
        for i, b in enumerate(basins_data):
            sBasin = f"{i + 1:08d}"
            dummy_basin = dict(b)
            dummy_basin["sWorkspace_output_basin"] = str(
                Path(oPyhexwatershed.sWorkspace_output_hexwatershed) / sBasin
            )
            pBasin = pybasin(dummy_basin)
            oPyhexwatershed.aBasin.append(pBasin)
    else:
        sBasin = f"{1:08d}"
        dummy_basin = dict()
        dummy_basin["sWorkspace_output_basin"] = str(
            Path(oPyhexwatershed.sWorkspace_output_hexwatershed) / sBasin
        )
        pBasin = pybasin(dummy_basin)
        oPyhexwatershed.aBasin.append(pBasin)

    oPyflowline.nOutlet = len(oPyhexwatershed.aBasin)
    return oPyhexwatershed


# ==============================================================================
# 6. Basin & Hexwatershed Configuration Managers
# ==============================================================================


class BasinConfigManager:
    """Configuration manager for basin objects supporting YAML and JSON."""

    @staticmethod
    def get_default_config() -> dict[str, Any]:
        """Returns a dictionary with all default basin configuration values."""
        return DEFAULT_BASIN_CONFIG.copy()

    @staticmethod
    def create_template_config(
        basin_id: int = 1, custom_values: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Create a configuration dictionary for a basin with default values."""
        config = BasinConfigManager.get_default_config()
        config["lBasinID"] = int(basin_id)

        sWorkspace_input = Path.cwd()
        config["sFilename_dam"] = str(sWorkspace_input / config["sFilename_dam"])
        config["sFilename_flowline_filter"] = str(
            sWorkspace_input / config["sFilename_flowline_filter"]
        )
        config["sFilename_flowline_raw"] = str(sWorkspace_input / config["sFilename_flowline_raw"])
        config["sFilename_flowline_topo"] = str(
            sWorkspace_input / config["sFilename_flowline_topo"]
        )

        sWorkspace_output = Path.cwd()
        basin_folder = f"{basin_id:08d}"
        config["sWorkspace_output_basin"] = str(sWorkspace_output / basin_folder)

        if custom_values:
            for key, value in custom_values.items():
                if isinstance(value, Path):
                    value = str(value)
                config[key] = value

        return config

    @staticmethod
    def create_multiple_basins(
        sFilename_basins: str | Path,
        nBasin: int = 1,
        custom_values: dict[str, Any] | None = None,
    ) -> list[Any]:
        """Generate configuration for multiple basins and save to YAML or JSON."""
        from pyflowline.classes.basin import pybasin

        sFilename_basins_path = Path(sFilename_basins).expanduser().resolve()
        sFilename_basins_path.parent.mkdir(parents=True, exist_ok=True)

        aBasin_out = []
        basin_dicts = []
        for i in range(nBasin):
            aConfig_basin = BasinConfigManager.create_template_config(
                basin_id=i + 1, custom_values=custom_values
            )
            pBasin = pybasin(aConfig_basin, iFlag_create_directory_in=0)
            aBasin_out.append(pBasin)
            basin_dicts.append(json.loads(pBasin.tojson()))

        ext = sFilename_basins_path.suffix.lower()
        fmt = "json" if ext == ".json" else "yaml"
        _dump_config_file(basin_dicts, sFilename_basins_path, fmt=fmt)

        return aBasin_out

    @staticmethod
    def load_config(filename: str | Path) -> list[dict[str, Any]] | dict[str, Any]:
        """Load basin configuration from YAML or JSON file."""
        resolved = _resolve_config_path(
            filename,
            candidates=("basins.yaml", "basins.yml", "basins.json"),
        )
        data = _parse_config_file(resolved)
        if isinstance(data, list):
            return [_normalize_basin_dict(b) for b in data]
        if isinstance(data, dict):
            return _normalize_basin_dict(data)
        return data

    @staticmethod
    def dump_config(config: Any, filename: str | Path, fmt: str | None = None) -> None:
        """Dump basin configuration to YAML or JSON file."""
        _dump_config_file(config, Path(filename), fmt=fmt)


class HexwatershedConfigManager:
    """Configuration manager for PyHexWatershed supporting YAML and JSON."""

    @staticmethod
    def get_default_config() -> dict[str, Any]:
        """Returns a dictionary with all default configuration values."""
        return DEFAULT_HEXWATERSHED_CONFIG.copy()

    @staticmethod
    def create_template_config(
        output_filename: str | Path,
        custom_values: dict[str, Any] | None = None,
        fmt: str | None = None,
    ) -> dict[str, Any]:
        """Create a configuration file with default values, optionally customized."""
        config = HexwatershedConfigManager.get_default_config()
        config["sWorkspace_input"] = str(Path.cwd() / "input")
        config["sWorkspace_output"] = str(Path.cwd() / "output")
        config["sFilename_model_configuration"] = str(output_filename)

        if custom_values:
            for key, value in custom_values.items():
                if isinstance(value, Path):
                    value = str(value)
                config[key] = value

        dest = Path(output_filename).expanduser().resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)

        if fmt is None:
            ext = dest.suffix.lower()
            fmt = "json" if ext == ".json" else "yaml"

        _dump_config_file(config, dest, fmt=fmt)
        return config

    @staticmethod
    def load_config(filename: str | Path) -> dict[str, Any]:
        """Load PyHexWatershed configuration from YAML or JSON file."""
        return load_pyhexwatershed_config(filename)

    @staticmethod
    def dump_config(config: dict[str, Any], filename: str | Path, fmt: str | None = None) -> None:
        """Dump PyHexWatershed configuration to YAML or JSON file."""
        dump_pyhexwatershed_config(config, filename, fmt=fmt)


# ==============================================================================
# 7. Backward-Compatibility Helper Functions
# ==============================================================================


def create_basin_template_configuration_file(
    sFilename_basins: str | Path, nBasin: int = 1
) -> list[Any]:
    """Generate basin configuration using BasinConfigManager."""
    return BasinConfigManager.create_multiple_basins(sFilename_basins, nBasin)


def create_model_configuration(
    filename: str | Path,
    mesh_type: str = "hexagon",
    case_index: int = 1,
    date: str | None = None,
    resolution_meter: float = 5000.0,
    resolution_degree: float = 0.5,
    region_name: str = "susquehanna",
    workspace_input: str | Path | None = None,
    workspace_output: str | Path | None = None,
    n_outlets: int = 1,
    fmt: str | None = None,
    sectioned: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """Generate a PyHexWatershed template configuration file in YAML or JSON.

    Supports:
        - YAML (.yaml / .yml): human-friendly, sectioned format with comments
        - JSON (.json): flat or sectioned format
        - Automatic creation of accompanying basin configuration file
    """
    dest_path = Path(filename).expanduser().resolve()
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt is None:
        ext = dest_path.suffix.lower()
        fmt = "json" if ext == ".json" else "yaml"
    else:
        fmt = fmt.lower()

    basin_ext = ".json" if fmt == "json" else ".yaml"
    sFilename_basins = str(dest_path.parent / f"{dest_path.stem}_basins{basin_ext}")
    create_basin_template_configuration_file(sFilename_basins, n_outlets)

    date_str = date or datetime.datetime.today().strftime("%Y%m%d")
    ws_in = str(workspace_input) if workspace_input else str(dest_path.parent / "input")
    ws_out = str(workspace_output) if workspace_output else str(dest_path.parent / "output")

    if fmt in ("yaml", "yml") and sectioned:
        config_data: dict[str, Any] = {
            "workflow": {
                "model": "pyhexwatershed",
                "mesh_type": mesh_type.lower(),
                "case_index": int(case_index),
                "date": date_str,
                "job": kwargs.get("sJob", "pyhexwatershed"),
            },
            "resolutions": {
                "degree": float(resolution_degree),
                "meter": float(resolution_meter),
                "accumulation_threshold": float(kwargs.get("dAccumulation_threshold", 100000.0)),
                "small_river": float(kwargs.get("dThreshold_small_river", 0.0)),
            },
            "region": {
                "name": region_name,
                "bbox": {
                    "left": float(kwargs.get("dLongitude_left", -180.0)),
                    "right": float(kwargs.get("dLongitude_right", 180.0)),
                    "bottom": float(kwargs.get("dLatitude_bot", -90.0)),
                    "top": float(kwargs.get("dLatitude_top", 90.0)),
                },
            },
            "flags": {
                "create_mesh": bool(kwargs.get("iFlag_create_mesh", 1)),
                "save_mesh": bool(kwargs.get("iFlag_save_mesh", 1)),
                "simplification": bool(kwargs.get("iFlag_simplification", 1)),
                "intersect": bool(kwargs.get("iFlag_intersect", 1)),
                "flowline": bool(kwargs.get("iFlag_flowline", 1)),
                "resample_method": int(kwargs.get("iFlag_resample_method", 2)),
                "global": bool(kwargs.get("iFlag_global", 0)),
                "multiple_outlet": bool(kwargs.get("iFlag_multiple_outlet", 0)),
                "elevation_profile": bool(kwargs.get("iFlag_elevation_profile", 0)),
                "stream_burning_topology": bool(kwargs.get("iFlag_stream_burning_topology", 1)),
                "save_elevation": bool(kwargs.get("iFlag_save_elevation", 1)),
                "use_mesh_dem": bool(kwargs.get("iFlag_use_mesh_dem", 0)),
                "force_watershed_boundary": bool(kwargs.get("iFlag_force_watershed_boundary", 0)),
            },
            "paths": {
                "workspace_input": ws_in,
                "workspace_output": ws_out,
                "dem": str(kwargs.get("sFilename_dem", ws_in + "/dem_ext.tif")),
                "spatial_reference": str(
                    kwargs.get("sFilename_spatial_reference", ws_in + "/boundary_proj.shp")
                ),
                "mesh_netcdf": str(
                    kwargs.get("sFilename_mesh_netcdf", ws_in + "/lnd_cull_mesh.nc")
                ),
                "basins": sFilename_basins,
            },
        }
        if "hexwatershed_bin" in kwargs or "sFilename_hexwatershed_bin" in kwargs:
            bin_path = str(
                kwargs.get("hexwatershed_bin") or kwargs.get("sFilename_hexwatershed_bin")
            )
            config_data["paths"]["hexwatershed_bin"] = bin_path
            config_data["flags"]["user_provided_binary"] = True
    else:
        config_data = HexwatershedConfigManager.get_default_config()
        config_data["sWorkspace_input"] = ws_in
        config_data["sWorkspace_output"] = ws_out
        config_data["sFilename_model_configuration"] = str(dest_path)
        config_data["sFilename_basins"] = sFilename_basins
        config_data["sMesh_type"] = mesh_type
        config_data["iCase_index"] = case_index
        config_data["sDate"] = date_str
        config_data["dResolution_meter"] = resolution_meter
        config_data["dResolution_degree"] = resolution_degree
        config_data["sRegion"] = region_name
        config_data["nOutlet"] = n_outlets
        for k, v in kwargs.items():
            config_data[k] = v
        if "hexwatershed_bin" in kwargs:
            config_data["sFilename_hexwatershed_bin"] = str(kwargs["hexwatershed_bin"])
            config_data["iFlag_user_provided_binary"] = 1

    _dump_config_file(config_data, dest_path, fmt=fmt)
    return config_data


create_hexwatershed_template_configuration_file = create_model_configuration


def pyhexwatershed_create_template_configuration_file(
    sFilename_json: str | Path,
    sWorkspace_input: str | Path,
    sWorkspace_output: str | Path,
    iFlag_use_mesh_dem_in: int | None = None,
    iFlag_use_shapefile_extent_in: int | None = None,
    iCase_index_in: int | None = None,
    dResolution_degree_in: float | None = None,
    dResolution_meter_in: float | None = None,
    sDate_in: str | None = None,
    sMesh_type_in: str | None = None,
    sModel_in: str | None = None,
    sWorkspace_output_in: str | Path | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Legacy helper: generate template configuration file in YAML or JSON."""
    dest = Path(sFilename_json)
    ext = dest.suffix.lower()
    fmt = "json" if ext == ".json" else "yaml"

    custom: dict[str, Any] = {}
    if iFlag_use_mesh_dem_in is not None:
        custom["iFlag_use_mesh_dem"] = iFlag_use_mesh_dem_in
    if iFlag_use_shapefile_extent_in is not None:
        custom["iFlag_use_shapefile_extent"] = iFlag_use_shapefile_extent_in
    if sModel_in is not None:
        custom["sModel"] = sModel_in
    custom.update(kwargs)

    return create_model_configuration(
        filename=sFilename_json,
        mesh_type=sMesh_type_in or "hexagon",
        case_index=iCase_index_in or 1,
        date=sDate_in,
        resolution_meter=dResolution_meter_in or 5000.0,
        resolution_degree=dResolution_degree_in or 0.5,
        workspace_input=sWorkspace_input,
        workspace_output=sWorkspace_output_in or sWorkspace_output,
        fmt=fmt,
        **custom,
    )


def change_json_key_value(
    sFilename_json_in: str | Path,
    sKey: str,
    new_value: Any,
    iFlag_basin_in: Any = None,
) -> None:
    """Safely update a key value in a JSON or YAML file (legacy helper)."""
    target = Path(sFilename_json_in).expanduser().resolve()
    data = _parse_config_file(target)

    if isinstance(new_value, Path):
        new_value = str(new_value)

    if iFlag_basin_in is None:
        if isinstance(data, dict):
            data[sKey] = new_value
        elif isinstance(data, list) and len(data) > 0:
            data[0][sKey] = new_value
    else:
        if isinstance(data, list) and len(data) > 0:
            data[0][sKey] = new_value
        elif isinstance(data, dict):
            data[sKey] = new_value

    ext = target.suffix.lower()
    fmt = "json" if ext == ".json" else "yaml"
    _dump_config_file(data, target, fmt=fmt)


change_config_key_value = change_json_key_value
change_config_keys_values = change_config_key_value
change_json_keys_values = change_json_key_value


__all__ = [
    "DEFAULT_BASIN_CONFIG",
    "DEFAULT_HEXWATERSHED_CONFIG",
    "BasinConfigManager",
    "HexwatershedConfigManager",
    "WorkflowSpec",
    "compile_workflow",
    "create_basin_template_configuration_file",
    "create_hexwatershed_template_configuration_file",
    "create_model_configuration",
    "create_workflow",
    "dump_pyhexwatershed_config",
    "dump_workflow_config",
    "join_project_path",
    "load_configuration",
    "load_pyhexwatershed_config",
    "load_workflow_config",
    "package_root",
    "path_manager",
    "project_root",
    "pyhexwatershed_create_template_configuration_file",
    "pyhexwatershed_package_root",
    "pyhexwatershed_project_root",
    "pyhexwatershed_read_configuration_file",
    "pyhexwatershed_read_model_configuration_file",
    "root_path_from_path_manager_location",
    "root_path_from_pyhexwatershed_package_root",
    "root_path_from_setup_file",
    "change_json_key_value",
    "change_config_key_value",
]
