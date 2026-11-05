#!/usr/bin/env python3
"""Yellow River (Huanghe) MPAS mesh PyHexWatershed simulation workflow.

This example demonstrates loading the YAML configuration using load_configuration
and orchestrating the full PyHexWatershed simulation pipeline:
1. Model setup
2. PyFlowline simplification and mesh intersection
3. Elevation assignment and outlet update
4. Configuration export (JSON for HexWatershed backend)
5. HexWatershed flow direction model execution
6. Result analysis and GIS vector/raster export
"""

import argparse
import logging
import sys
from pathlib import Path

from pyhexwatershed.configuration import load_configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to workflow YAML configuration file (default: pyhexwatershed_huanghe_mpas.yaml)",
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        default=True,
        help="Run full simulation pipeline (default: True)",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Generate flowline/mesh visualization map if cartopy/matplotlib is available",
    )
    parser.add_argument(
        "--resolution-meter",
        type=float,
        default=None,
        help="Override mesh resolution in meters",
    )
    parser.add_argument(
        "--case-index",
        type=int,
        default=None,
        help="Override simulation case index",
    )
    args = parser.parse_args()

    # ── Step 1: Resolve configuration path ────────────────────────────────────
    if args.config:
        sFilename_workflow = Path(args.config).expanduser().resolve()
    else:
        sFilename_workflow = Path(__file__).with_name("pyhexwatershed_huanghe_mpas.yaml")

    logger.info("Step 1: Loading configuration from: %s", sFilename_workflow)

    overrides = {}
    if args.resolution_meter is not None:
        overrides["resolution_meter"] = args.resolution_meter
    if args.case_index is not None:
        overrides["case_index"] = args.case_index

    case = load_configuration(sFilename_workflow, **overrides)
    if case is None:
        logger.error("Failed to load configuration from: %s", sFilename_workflow)
        sys.exit(1)

    logger.info("   * Region: %s", case.sRegion)
    logger.info("   * Mesh type: %s (code %d)", case.sMesh_type, case.iMesh_type)
    logger.info("   * Case ID: %s", case.sCase)
    logger.info("   * Resolution: %s m", case.dResolution_meter)
    logger.info("   * Output workspace: %s", case.sWorkspace_output)
    if getattr(case, "sFilename_mesh_netcdf", None):
        logger.info("   * MPAS mesh NetCDF: %s", case.sFilename_mesh_netcdf)
    if getattr(case, "sFilename_mesh_boundary", None):
        logger.info("   * Mesh boundary: %s", case.sFilename_mesh_boundary)
    if getattr(case, "sFilename_dem", None):
        logger.info("   * DEM: %s", case.sFilename_dem)
    if getattr(case, "sFilename_hexwatershed_bin", None):
        logger.info("   * HexWatershed binary: %s", case.sFilename_hexwatershed_bin)

    # ── Step 2: Model setup ───────────────────────────────────────────────────
    logger.info("Step 2: Setting up PyHexWatershed model...")
    case.setup()

    # ── Step 3: Simulation Execution ──────────────────────────────────────────
    if args.simulate or getattr(case, "iFlag_simulation", 0) == 1:
        logger.info("Step 3: Running PyFlowline river simplification & mesh intersection...")
        #aCell_origin = case.run_pyflowline()

        # Step 4: Elevation assignment & outlet update
        if getattr(case, "iFlag_use_mesh_dem", 0) != 1:
            logger.info("Step 4: Sampling and assigning elevation to mesh cells...")
            #case.assign_elevation_to_cells()
            #case.update_outlet(aCell_origin)

        # Step 5: Export PyFlowline results and case configuration
        logger.info(
            "Step 5: Exporting PyFlowline results and JSON configuration for HexWatershed..."
        )
        #case.pPyFlowline.export()
        #case.export_config_to_json()

        # Step 6: HexWatershed model execution
        logger.info("Step 6: Running HexWatershed flow direction model...")
        #case.run_hexwatershed()

        # Step 7: Analyze and export HexWatershed results
        logger.info("Step 7: Analyzing and exporting watershed products...")
        case.analyze()
        case.export()

    # ── Step 8: Visualization (optional) ──────────────────────────────────────
    if args.visualize or getattr(case, "iFlag_visualization", 0) == 1:
        if hasattr(case, "plot") and callable(case.plot):
            logger.info("Step 8: Generating flow direction visualization...")
            try:
                case.plot(sVariable_in="flow_direction", sFilename_output_in="flow_direction.png")
            except Exception as exc:
                logger.warning("Visualization failed or skipped: %s", exc)

    logger.info("Finished successfully.")


if __name__ == "__main__":
    main()
