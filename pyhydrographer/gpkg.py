import os

import geopandas as gpd

from pyhydrographer.utils import generate_output_file


def crop_and_save_gpkg(input_file, output_dir, min_lon, max_lon, min_lat, max_lat):
    """
    Crop a GeoPackage file based on latitude and longitude coordinates and save the cropped GeoDataFrame to a new file.

    Parameters:
        input_file (str): Path to the input GeoPackage file.
        output_dir (str): Path to the output folder where the cropped file will be saved.
        min_lon (float): Minimum longitude coordinate for cropping.
        max_lon (float): Maximum longitude coordinate for cropping.
        min_lat (float): Minimum latitude coordinate for cropping.
        max_lat (float): Maximum latitude coordinate for cropping.

    Returns:
        cropped_file (str): Path to the cropped GeoPackage file.
    """
    try:
        gdf = gpd.read_file(input_file, bbox=(min_lon, min_lat, max_lon, max_lat))

        cropped_gdf = gdf.cx[min_lon:max_lon, min_lat:max_lat]

        cropped_file = generate_output_file(input_file, output_dir)

        cropped_gdf.to_file(cropped_file, driver="GPKG")

        return cropped_file

    except Exception as e:
        print(f"Error cropping and saving GeoPackage file: {e}")
        return None
