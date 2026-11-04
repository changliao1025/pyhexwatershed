# Yellow River (Huanghe) Basin Example

This directory contains the PyHexWatershed configuration and simulation workflow for the Yellow River (Huanghe) basin using a variable-resolution MPAS Voronoi mesh.

---

## Configuration Files

- **`pyhexwatershed_huanghe_mpas.yaml`**: Domain specification defining workflow orchestration, target multi-scale resolutions, bounding box, execution flags, and paths across platforms (`Darwin`, `Linux`, `Windows`).
- **`pyhexwatershed_huanghe_basins.yaml`**: Basin specification with the main Yellow River outlet coordinate (at Dongying, Bohai Sea mouth: `119.1729°E, 37.7687°N`), upstream area thresholds, and cropped flowline vector paths.

---

## Running the Simulation

Execute the workflow script:
```bash
python run_workflow.py
```

### CLI Arguments & Overrides

```bash
# Run with a custom configuration file
python run_workflow.py --config ./pyhexwatershed_huanghe_mpas.yaml

# Override resolution on the fly (in memory, without mutating disk files)
python run_workflow.py --resolution-meter 5000.0 --case-index 2

# Enable visualization (requires cartopy / matplotlib)
python run_workflow.py --visualize
```

---

## Workflow Execution Stages

1. **Step 1: Configuration Loading**: Resolves platform-specific paths (macOS, Linux HPC, or default) and compiles sectioned YAML into engine data structures.
2. **Step 2: Model Setup**: Initializes directories and links the child PyFlowline instance.
3. **Step 3: PyFlowline Pipeline**: Simplifies braided river reaches and intersects river vectors with MPAS Voronoi cells.
4. **Step 4: Elevation Assignment**: Samples DEM elevation to mesh cells and aligns the outlet.
5. **Step 5: Export Configuration**: Dumps case configuration to YAML (human-readable) and backend JSON (for the C++ executable).
6. **Step 6: HexWatershed Execution**: Runs the flow direction modeling algorithm.
7. **Step 7: Product Export**: Writes flow directions, stream segments, and catchment polygons to GeoJSON / Parquet.
