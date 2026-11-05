"""Unit tests for PyHexWatershed unified configuration manager.

Tests path discovery, YAML/JSON parsing, two-tier workflow compilation,
cross-platform path mapping, and backward-compatible module shims.
"""

from __future__ import annotations

import json
import os
import platform
import tempfile
import unittest
from pathlib import Path
from typing import Any

import pyhexwatershed
from pyhexwatershed import config, configuration
from pyhexwatershed.configuration import (
    DEFAULT_BASIN_CONFIG,
    DEFAULT_HEXWATERSHED_CONFIG,
    BasinConfigManager,
    HexwatershedConfigManager,
    WorkflowSpec,
    change_json_key_value,
    compile_workflow,
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
    pyhexwatershed_package_root,
    pyhexwatershed_project_root,
    pyhexwatershed_read_configuration_file,
    pyhexwatershed_read_model_configuration_file,
)
from pyhexwatershed.configuration.config_manager import (
    _dump_config_file,
    _normalize_basin_dict,
    _parse_config_file,
    _resolve_config_path,
    _select_platform_path,
)


class TestConfigManager(unittest.TestCase):
    def test_package_and_project_roots(self):
        pkg = package_root()
        self.assertIsInstance(pkg, Path)
        self.assertTrue(pkg.is_dir())

        proj = project_root()
        self.assertIsInstance(proj, Path)
        self.assertTrue(proj.is_dir())

        joined = join_project_path("pyhexwatershed", "configuration")
        self.assertIsInstance(joined, Path)
        self.assertTrue(joined.exists())

        # Legacy path_manager namespace
        self.assertEqual(path_manager.pyhexwatershed_project_root(), proj)
        self.assertEqual(path_manager.pyhexwatershed_package_root(), pkg)

    def test_select_platform_path(self):
        mapping = {
            "Darwin": "/Users/test/data",
            "Linux": "/home/test/data",
            "Windows": "C:\\data",
            "default": "./data",
        }
        resolved = _select_platform_path(mapping)
        system = platform.system()
        expected = mapping.get(system, mapping["default"])
        self.assertEqual(resolved, expected)

        # Plain string and Path passthrough
        self.assertEqual(_select_platform_path("/my/path"), "/my/path")
        self.assertEqual(_select_platform_path(Path("/my/path")), "/my/path")

    def test_workflow_spec_and_compile(self):
        spec = WorkflowSpec(
            mesh_type="MPAS",
            case_index=2,
            date="20261104",
            resolutions={"meter": 3000.0, "degree": 0.05, "accumulation_threshold": 50000.0},
            region={
                "name": "test_domain",
                "bbox": {"left": -80, "right": -75, "bottom": 39, "top": 43},
            },
            flags={"create_mesh": True, "elevation_profile": True, "use_mesh_dem": True},
            paths={"dem": "./dem.tif", "workspace_output": "./output"},
        )

        compiled = compile_workflow(spec)
        self.assertEqual(compiled["sMesh_type"], "mpas")
        self.assertEqual(compiled["iMesh_type"], 4)
        self.assertEqual(compiled["iCase_index"], 2)
        self.assertEqual(compiled["sDate"], "20261104")
        self.assertEqual(compiled["dResolution_meter"], 3000.0)
        self.assertEqual(compiled["dResolution_degree"], 0.05)
        self.assertEqual(compiled["dAccumulation_threshold"], 50000.0)
        self.assertEqual(compiled["dLongitude_left"], -80.0)
        self.assertEqual(compiled["dLongitude_right"], -75.0)
        self.assertEqual(compiled["dLatitude_bot"], 39.0)
        self.assertEqual(compiled["dLatitude_top"], 43.0)
        self.assertEqual(compiled["iFlag_create_mesh"], 1)
        self.assertEqual(compiled["iFlag_elevation_profile"], 1)
        self.assertEqual(compiled["iFlag_use_mesh_dem"], 1)
        self.assertEqual(compiled["sFilename_dem"], "./dem.tif")
        self.assertEqual(compiled["sWorkspace_output"], "./output")

    def test_yaml_and_json_parsing_and_dumping(self):
        data = {
            "workflow": {
                "model": "pyhexwatershed",
                "mesh_type": "hexagon",
                "case_index": 1,
                "date": "20220801",
            },
            "resolutions": {"meter": 5000.0},
            "flags": {"create_mesh": 1},
            "paths": {"dem": "dem.tif"},
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Test YAML
            yaml_file = tmp_path / "config.yaml"
            _dump_config_file(data, yaml_file, fmt="yaml")
            self.assertTrue(yaml_file.exists())
            loaded_yaml = _parse_config_file(yaml_file)
            self.assertEqual(loaded_yaml["workflow"]["mesh_type"], "hexagon")

            # Test JSON
            json_file = tmp_path / "config.json"
            _dump_config_file(data, json_file, fmt="json")
            self.assertTrue(json_file.exists())
            loaded_json = _parse_config_file(json_file)
            self.assertEqual(loaded_json["workflow"]["mesh_type"], "hexagon")

    def test_load_workflow_config_with_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            yaml_file = tmp_path / "test_config.yaml"

            yaml_content = """# Test Config
workflow:
  mesh_type: square
  case_index: 3
  date: "20261104"

resolutions:
  meter: 10000.0

paths:
  workspace_input: ./input_dir
  workspace_output: ./output_dir
  dem: ./elevation.tif
"""
            yaml_file.write_text(yaml_content, encoding="utf-8")

            config_dict = load_workflow_config(yaml_file)
            self.assertEqual(config_dict["sMesh_type"], "square")
            self.assertEqual(config_dict["iMesh_type"], 2)
            self.assertEqual(config_dict["iCase_index"], 3)
            self.assertEqual(config_dict["dResolution_meter"], 10000.0)

            # Verify relative path resolution
            self.assertEqual(
                config_dict["sWorkspace_input"], str((tmp_path / "input_dir").resolve())
            )
            self.assertEqual(
                config_dict["sWorkspace_output"], str((tmp_path / "output_dir").resolve())
            )
            self.assertEqual(
                config_dict["sFilename_dem"], str((tmp_path / "elevation.tif").resolve())
            )

    def test_basin_config_manager(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            basins_yaml = tmp_path / "basins.yaml"

            aBasin = BasinConfigManager.create_multiple_basins(
                basins_yaml, nBasin=2, custom_values={"dAccumulation_threshold": 80000.0}
            )
            self.assertEqual(len(aBasin), 2)
            self.assertTrue(basins_yaml.exists())

            loaded = BasinConfigManager.load_config(basins_yaml)
            self.assertIsInstance(loaded, list)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["dAccumulation_threshold"], 80000.0)
            self.assertEqual(loaded[0]["lBasinID"], 1)
            self.assertEqual(loaded[1]["lBasinID"], 2)

    def test_backward_compatibility_module_shims(self):
        import pyhexwatershed.configuration.config_manager as cm
        import pyhexwatershed.configuration.path_manager as pm
        import pyhexwatershed.configuration.read_configuration_file as rcf

        self.assertIs(cm.load_configuration, load_configuration)
        self.assertIs(pm.join_project_path, join_project_path)
        self.assertIs(
            rcf.pyhexwatershed_read_configuration_file, pyhexwatershed_read_configuration_file
        )

        self.assertIs(pyhexwatershed.config.load_configuration, load_configuration)
        self.assertIs(pyhexwatershed.configuration.load_configuration, load_configuration)
        self.assertIs(pyhexwatershed.create_workflow, create_workflow)

    def test_load_example_yamls(self):
        # Verify that all converted YAML files parse and compile cleanly
        example_dir = project_root() / "examples"
        susq_dir = example_dir / "susquehanna"

        for yaml_stem in [
            "pyhexwatershed_susquehanna_hexagon",
            "pyhexwatershed_susquehanna_mpas",
            "pyhexwatershed_susquehanna_latlon",
            "pyhexwatershed_susquehanna_square",
        ]:
            yaml_path = susq_dir / f"{yaml_stem}.yaml"
            self.assertTrue(yaml_path.exists(), f"{yaml_path} does not exist")
            cfg = load_workflow_config(yaml_path)
            self.assertIn("sMesh_type", cfg)
            self.assertIn("sWorkspace_output", cfg)
            self.assertIn("dResolution_meter", cfg)

        # Test Huanghe example YAML
        huanghe_yaml = example_dir / "huanghe" / "pyhexwatershed_huanghe_mpas.yaml"
        self.assertTrue(huanghe_yaml.exists(), f"{huanghe_yaml} does not exist")
        cfg_hh = load_workflow_config(huanghe_yaml)
        self.assertEqual(cfg_hh["sRegion"], "huanghe")
        self.assertEqual(cfg_hh["sMesh_type"], "mpas")
        self.assertEqual(cfg_hh["dResolution_meter"], 3000.0)

    def test_load_configuration_with_overrides(self):
        example_dir = project_root() / "examples"
        susq_hexagon_yaml = example_dir / "susquehanna" / "pyhexwatershed_susquehanna_hexagon.yaml"

        with tempfile.TemporaryDirectory() as tmp_dir:
            case = load_configuration(
                susq_hexagon_yaml,
                workspace_output=tmp_dir,
                resolution_meter=7500.0,
                case_index=9,
            )
            self.assertEqual(case.iCase_index, 9)
            self.assertEqual(case.dResolution_meter, 7500.0)
            self.assertEqual(case.sMesh_type, "hexagon")
            self.assertIsNotNone(case.pPyFlowline)
            self.assertGreater(len(case.aBasin), 0)
            self.assertTrue(
                case.aBasin[0].sWorkspace_output_basin.startswith(case.sWorkspace_output_pyflowline)
            )
            self.assertFalse(
                case.aBasin[0].sWorkspace_output_basin.startswith(
                    case.sWorkspace_output_hexwatershed
                )
            )

            # Test exporting to YAML
            yaml_out = Path(tmp_dir) / "exported_case.yaml"
            case.export_config_to_yaml(yaml_out)
            self.assertTrue(yaml_out.exists())

            # Test internal configuration.json generated for C++ backend
            json_backend = Path(case.sWorkspace_output) / "configuration.json"
            self.assertTrue(json_backend.exists())

    def test_create_model_configuration_yaml_and_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Test creating YAML configuration template
            yaml_out = tmp_path / "test_template.yaml"
            cfg_yaml = create_model_configuration(
                yaml_out,
                mesh_type="hexagon",
                case_index=5,
                resolution_meter=10000.0,
                workspace_input=tmp_path / "input",
                workspace_output=tmp_path / "output",
            )
            self.assertTrue(yaml_out.exists())
            self.assertTrue((tmp_path / "test_template_basins.yaml").exists())
            self.assertIn("workflow", cfg_yaml)
            self.assertEqual(cfg_yaml["workflow"]["mesh_type"], "hexagon")
            self.assertEqual(cfg_yaml["resolutions"]["meter"], 10000.0)

            # Test creating JSON configuration template
            json_out = tmp_path / "test_template.json"
            cfg_json = create_model_configuration(
                json_out,
                mesh_type="mpas",
                case_index=2,
                resolution_meter=2500.0,
                workspace_input=tmp_path / "input",
                workspace_output=tmp_path / "output",
                hexwatershed_bin="/usr/local/bin/hexwatershed",
            )
            self.assertTrue(json_out.exists())
            self.assertTrue((tmp_path / "test_template_basins.json").exists())
            self.assertEqual(cfg_json["sMesh_type"], "mpas")
            self.assertEqual(cfg_json["dResolution_meter"], 2500.0)
            self.assertEqual(cfg_json["sFilename_hexwatershed_bin"], "/usr/local/bin/hexwatershed")

    def test_hexwatershed_binary_configuration(self):
        yaml_path = (
            Path(pyhexwatershed_project_root())
            / "examples"
            / "huanghe"
            / "pyhexwatershed_huanghe_mpas.yaml"
        )
        self.assertTrue(yaml_path.exists())
        config = load_workflow_config(yaml_path)
        self.assertIn("sFilename_hexwatershed_bin", config)
        if platform.system() == "Darwin":
            self.assertEqual(
                config["sFilename_hexwatershed_bin"],
                "/Users/changliao/workspace/cplus/hexwatershed/bin/hexwatershed",
            )
        self.assertEqual(config["iFlag_user_provided_binary"], 1)

    def test_force_watershed_boundary_flag(self):
        spec_dict = {
            "workflow": {"mesh_type": "mpas"},
            "flags": {"force_watershed_boundary": True},
        }
        cfg = compile_workflow(spec_dict)
        self.assertEqual(cfg["iFlag_force_watershed_boundary"], 1)

        case = create_workflow(spec_dict)
        self.assertEqual(case.iFlag_force_watershed_boundary, 1)
        self.assertEqual(case.pPyFlowline.iFlag_force_watershed_boundary, 1)


if __name__ == "__main__":
    unittest.main()
