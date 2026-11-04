# PyHexWatershed Unified Workflow Configuration Guide

PyHexWatershed supports human-readable, comment-enabled YAML (`.yaml`, `.yml`) as the primary configuration format, along with full backwards compatibility for JSON (`.json`).

This follows the [Unified Configuration Architecture Pattern Guide](../../pyflowline/docs/unified_configuration_pattern_guide.md) established across `pyflowline`, `pyearthmesh`, and `pyhexwatershed`.

---

## 1. Fast Track Example

```python
from pyhexwatershed.configuration import load_configuration, create_workflow

# 1. Load configuration and initialize simulation case engine
case = load_configuration("pyhexwatershed_susquehanna_hexagon.yaml")

# 2. Setup domain and mesh
case.setup()

# 3. Execute PyFlowline simplification and mesh intersection
aCell_origin = case.run_pyflowline()
aCell_out = case.assign_elevation_to_cells()
aCell_new = case.update_outlet(aCell_origin)
case.pPyFlowline.export()

# 4. Export configuration in YAML (and internal JSON for C++ backend)
case.export_config_to_yaml()

# 5. Run HexWatershed backend simulation
case.run_hexwatershed()
case.analyze()
case.export()
```

---

## 2. In-Memory Runtime Parameter Overrides

Never mutate configuration files on disk. Pass runtime overrides directly:

```python
case = load_configuration(
    "pyhexwatershed_susquehanna_hexagon.yaml",
    case_index=2,
    resolution_meter=2500.0,
    workspace_output="./custom_output",
)
```

---

## 3. Configuration File Structure (Tier 1 YAML)

```yaml
# ==============================================================================
# Simulation Case Specification (YAML)
# ==============================================================================
workflow:
  model: pyhexwatershed
  mesh_type: hexagon                            # hexagon, square, latlon, mpas, dggrid
  case_index: 1
  date: "20220801"
  job: pyhexwatershed

resolutions:
  degree: 0.5
  meter: 5000.0                                 # Mesh resolution (m)
  accumulation_threshold: 100000.0              # Upstream accumulation threshold
  small_river: 0.0

region:
  name: susquehanna
  bbox:
    left: -180.0
    right: 180.0
    bottom: -90.0
    top: 90.0

flags:
  create_mesh: true
  save_mesh: true
  simplification: true
  intersect: true
  flowline: true
  resample_method: 2
  global: false
  multiple_outlet: false
  elevation_profile: false
  stream_burning_topology: true
  save_elevation: true
  use_mesh_dem: false

paths:
  workspace_input:
    Darwin: ../../data/susquehanna/input
    Linux: /qfs/people/liao313/workspace/python/pyhexwatershed/data/susquehanna/input
    default: ../../data/susquehanna/input
  workspace_output:
    Darwin: ../../data/susquehanna/output
    Linux: /compyfs/liao313/04model/pyhexwatershed/susquehanna
    default: ../../data/susquehanna/output
  dem:
    Darwin: ../../data/susquehanna/input/dem_ext.tif
    Linux: /qfs/people/liao313/data/hexwatershed/susquehanna/raster/dem/dem_ext.tif
    default: ../../data/susquehanna/input/dem_ext.tif
  spatial_reference:
    Darwin: ../../data/susquehanna/input/boundary_proj.shp
    Linux: /qfs/people/liao313/workspace/python/pyhexwatershed/data/susquehanna/input/boundary_proj.shp
    default: ../../data/susquehanna/input/boundary_proj.shp
  mesh_netcdf:
    Darwin: ../../data/susquehanna/input/lnd_cull_mesh.nc
    Linux: /qfs/people/liao313/workspace/python/pyhexwatershed/data/susquehanna/input/lnd_cull_mesh.nc
    default: ../../data/susquehanna/input/lnd_cull_mesh.nc
  basins: ./pyhexwatershed_susquehanna_basins.yaml
```
