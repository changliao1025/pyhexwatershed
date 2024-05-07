import json
from pathlib import Path
import shutil
import tempfile

def change_json_key_value(sFilename_json_in, sKey, new_value, iFlag_basin_in=None):
    """
    Change the value associated with the specified key in a JSON file safely.

    Args:
        sFilename_json_in (str or Path): Path to the JSON file.
        sKey (str): Key whose value needs to be changed.
        new_value: New value to set for the specified key.
        iFlag_basin_in (bool, optional): Flag indicating if the key is for a basin configuration. Defaults to None.
    """
    # Ensure input filename is a string
    sFilename_json_in = str(sFilename_json_in)

    # Convert new_value to string if it's a Path object
    if isinstance(new_value, Path):
        new_value = str(new_value)

    # Read the original JSON data
    with open(sFilename_json_in, 'r') as file:
        data = json.load(file)

    # Update the value associated with the specified key
    if iFlag_basin_in is None:
        data[sKey] = new_value
    else:
        data[0][sKey] = new_value

    # Write the updated data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        json.dump(data, temp_file, indent=4)
        temp_path = temp_file.name

    # Replace the original file with the updated temporary file
    shutil.move(temp_path, sFilename_json_in)
