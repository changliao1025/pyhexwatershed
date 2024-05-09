from pathlib import Path
from pkg_resources import resource_filename
"""
path_manager
All paths are created with Path and call resolve()
"""

def join_project_path(*args: str) -> Path:
    """
    Join components of a path relative to the project root.

    Args:
        *args: Variable number of string arguments representing path components.

    Returns:
        Path: Absolute path joined with the project root.
    """
    project_root = pyhexwatershed_project_root()
    return project_root.joinpath(*args)

def pyhexwatershed_project_root() -> Path:
    """
    Attempt to find the root path of the project, first by looking for a 'setup.py' file, and then using pkg_resources to find the installation path.
    """
    try:
        return root_path_from_setup_file()
    except FileNotFoundError:
        return root_path_from_pyhexwatershed_package_root()
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while locating the project root: {str(e)}")

def pyhexwatershed_package_root(package_name='pyhexwatershed') -> Path:
    """Get the installation root directory of the package."""
    return Path(resource_filename(package_name, '')).resolve()

def root_path_from_setup_file() -> Path:
    """Return the top-level (root) path of the pyhexwatershed project.
    This function navigates upwards from this file's path until it finds a directory
    with a specific marker (e.g., a setup.py file) indicating the root of the project.
    """
    this_path = Path(__file__).resolve()
    for parent in this_path.parents:
        if (parent / 'setup.py').exists():
            return parent
    raise FileNotFoundError("setup.py not found. Is this the right project structure?")

def root_path_from_pyhexwatershed_package_root() -> Path:
    """Get the installation root directory of the package."""
    return pyhexwatershed_package_root().parent

# Example additional function for getting root from this module's location, adjusted for best practice
def root_path_from_path_manager_location() -> Path:
    """Return the top-level (root) path of the pyhexwatershed project
    This function assumes the module is located at a fixed level:
        root_path/pyhexwatershed/configuration/path_manager
    """
    return Path(__file__).resolve().parents[2]
