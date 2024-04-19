import os

import rasterio as rio

from rasterio.windows import Window
from rasterio.merge import merge
from rasterio.transform import from_origin

from pyhydrographer.utils import (
    check_file_exists,
    extract_hv_from_urls,
    extract_raster_name,
)


def get_bounds_deg(filepath):

    with rio.open(filepath) as src:

        x1, y1 = src.transform * (0, 0)
        x2, y2 = src.transform * (src.width, src.height)

    return (x1, y1, x2, y2)


def merge_rasters(
    raster_urls,
    output_dir,
    layer="accumulation",
    compress="lzw",
    tiled=True,
    blockxsize=512,
    blockysize=512,
):
    raster_to_mosiac = []

    for url in raster_urls:

        rasterpath = check_file_exists(rasterurl=url)

        print(rasterpath)

        raster = rio.open(rasterpath)
        raster_to_mosiac.append(raster)

    mosaic, output = merge(raster_to_mosiac)

    output_meta = raster.meta.copy()
    output_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": output,
            "compress": compress,  # Use LZW compression
            "tiled": tiled,  # Use tiled organization
            "blockxsize": blockxsize,  # Tile width
            "blockysize": blockysize,  # Tile height
        }
    )

    h_v_list = extract_hv_from_urls(raster_urls)

    mosaic_path = f"{output_dir}{layer}_{'_'.join(h_v_list)}.tif"

    with rio.open(mosaic_path, "w", **output_meta) as m:
        m.write(mosaic)

    return mosaic_path


def crop_raster(input_raster, output_dir, bbox_latlon):
    """
    Crop a raster using bounding boxes specified in latitude and longitude coordinates.

    Parameters:
        input_raster (str): Path to the input raster file.
        output_dir (str): Path to the output folder.
        bbox_latlon (tuple): Bounding box coordinates in (min_lon, min_lat, max_lon, max_lat) format.

    Returns:
        None
    """

    rasterpath = check_file_exists(rasterurl=input_raster)

    with rio.open(rasterpath) as src:

        transform = src.transform

        # Convert bounding box coordinates from lat/lon to pixel coordinates
        min_row, min_col = src.index(*bbox_latlon[:2])
        max_row, max_col = src.index(*bbox_latlon[2:])

        # Calculate the width and height of the output raster
        width = abs(max_col - min_col)
        height = abs(max_row - min_row)

        xmin, ymin = src.index(*bbox_latlon[:2])
        xmax, ymax = src.index(*bbox_latlon[2:])

        # Check if window dimensions are valid
        if min_row < 0 or min_col < 0 or max_row < 0 or max_col < 0:
            raise ValueError("Bounding box does not intersect with raster extent")

        # Define window for cropping
        window = Window(min_col, min_row, width, height)

        # Read and crop raster data
        data = src.read(window=window)

        # Update metadata for cropped raster
        # transform = src.window_transform(window)
        new_transform = from_origin(
            transform[2] + min_row * transform[0],
            transform[5] + min_col * transform[4],
            transform[0],
            transform[4],
        )

        profile = src.profile
        profile.update(
            {"width": window.width, "height": window.height, "transform": new_transform}
        )

        rastername = extract_raster_name(input_raster)

        cropped_path = os.path.join(output_dir, rastername.replace(".tif", "_crop.tif"))

        # Write cropped raster to output file
        with rio.open(cropped_path, "w", **profile) as dst:
            dst.write(data)

    return cropped_path
