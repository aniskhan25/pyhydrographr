import os

import rasterio as rio

from pyhydrographer.gpkg import crop_and_save_gpkg
from pyhydrographer.pixel import (
    get_pixel_coords,
    get_pixel_values_at_coords,
    get_pixel_value_at_lat_lon,
)
from pyhydrographer.regional_units import get_regional_units_bounds
from pyhydrographer.raster import merge_rasters, crop_raster
from pyhydrographer.block import get_block_url, get_block_bounds, get_block_window
from pyhydrographer.utils import (
    check_file_exists,
    get_rows_cols,
    extract_hv_from_url,
    extract_hv_from_urls,
    get_dims_deg,
)
from pyhydrographer.tile import (
    get_tile_id,
    get_tile_ids,
    get_tile_for_point,
    get_tile_ids_rect,
    get_tile_urls,
    get_tile_list,
)
from pyhydrographer.globals import TILE_SIZE, DATA_PATH


def test_crop_and_save_gpkg():

    input_file = "/Users/anisjyu/Downloads/order_vect_point_h18v02.gpkg"
    output_folder = "/Users/anisjyu/Downloads"

    bb = [0.256, 20, 45, 55.4325]  # (lon lon lat lat)
    # bb = [19.0, 19.5, 48, 50] # (lon lon lat lat)
    min_lon, max_lon, max_lat, min_lat = bb

    cropped_file = crop_and_save_gpkg(
        input_file, output_folder, min_lon, max_lon, min_lat, max_lat
    )
    if cropped_file is not None:
        print(f"Cropped file saved to: {cropped_file}")


def test_get_pixel_coords():
    lat = 42.5
    lon = -120.0

    raster_name = "regional_unit_ovr.tif"

    filepath = check_file_exists(raster_name)

    with rio.open(filepath) as src:
        x, y = get_pixel_coords(lon, lat, src.transform)

        print("Pixel coordinates:", x, y)


def test_extract_raster_name():
    url = "https://public.igb-berlin.de/index.php/s/agciopgzXjWswF4/download?path=%2Fr.watershed%2Faccumulation_tiles20d&files=accumulation_h18v02.tif"
    raster_name = test_extract_raster_name(url)
    print(raster_name)


def test_get_regional_units_bounds():

    x1, y1, x2, y2 = get_regional_units_bounds()

    print(f"({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")


def test_get_dims_deg():
    x1, y1, x2, y2 = get_regional_units_bounds()

    print(f"({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")
    height, width = get_dims_deg(x1, y1, x2, y2)

    print("Tile Map Height:", height)
    print("Tile Map Width:", width)


def test_get_rows_cols():

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect)

    print("Tile Map Rows:", rows)
    print("Tile Map Cols:", cols)


def test_get_tile_ids():

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    print(tile_ids)


def test_get_tile_xy():

    lon = 13.2284
    lat = 52.570

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_id = get_tile_id(tile_ids, lon, lat)

    print("Tile Id:", tile_id)


def test_get_tile_for_point():

    lon = 13.2284
    lat = 52.570

    tile_map_rect = get_regional_units_bounds()

    tile_rect = get_tile_for_point(lon, lat, tile_map_rect)

    x1_deg, y1_deg, x2_deg, y2_deg = tile_rect

    print(f"({x1_deg:.2f}, {y1_deg:.2f}, {x2_deg:.2f}, {y2_deg:.2f})")


def test_get_block_window(rasterpath, lon, lat, tile_ids, layer, band=1):
    lon = 13.2284
    lat = 52.570

    layer = "accumulation"

    rasterpath = get_block_url(lon, lat, tile_ids, layer)

    block_window = get_block_window(rasterpath, lon, lat, tile_ids, layer)

    print("Block Width:", block_window.width)
    print("Block Height:", block_window.height)


def test_get_block_bounds():
    lon = 13.2284
    lat = 52.570

    layer = "accumulation"

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    rasterpath = get_block_url(lon, lat, tile_ids, layer)

    block_rect = get_block_bounds(rasterpath, lon, lat, tile_ids, layer)

    print(
        f"({block_rect[0]:.2f}, {block_rect[1]:.2f}, {block_rect[2]:.2f}, {block_rect[3]:.2f})"
    )


def test_get_block_data():
    lon = 13.2284
    lat = 52.570

    layer = "accumulation"

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_id = get_tile_id(tile_ids, lon, lat)

    rasterurl = get_block_url(tile_id, layer)

    rasterpath = check_file_exists(rasterurl=rasterurl)

    # block_data = get_block_data(rasterpath, lon, lat, tile_ids, layer)
    # block_data


def test_get_block_url():
    lon = 13.2284
    lat = 52.570

    layer = "accumulation"

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_id = get_tile_id(tile_ids, lon, lat)

    rasterpath = get_block_url(tile_id, layer)

    print("Raster path:", rasterpath)


def test_get_tile_ids_rect():
    # bb = [0.256, 40, 45, 5.4325] # (lon lon lat lat)
    bb = [0.256, 20, 45, 55.4325]  # (lon lon lat lat)

    min_lon, max_lon, min_lat, max_lat = bb

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_ids_rect = get_tile_ids_rect(tile_ids, min_lon, max_lon, min_lat, max_lat)

    print(tile_ids_rect[0, :])


def test_extract_hv_from_urls():

    urls = [
        "https://public.igb-berlin.de/index.php/s/agciopgzXjWswF4/download?path=%2Fr.watershed%2Faccumulation_tiles20d&files=accumulation_h18v02.tif",
        "https://example.com/another-url/accumulation_h20v05.tif",
    ]

    print(extract_hv_from_url(urls[0]))
    print(extract_hv_from_urls(urls))

    # get_tile_urls(tile_ids_rect, "accumulation")


def test_merge_rasters():

    bb = [19, 21, 48, 50]  # (lon lon lat lat)

    min_lon, max_lon, min_lat, max_lat = bb

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_ids_rect = get_tile_ids_rect(tile_ids, min_lon, max_lon, min_lat, max_lat)[
        0, :
    ]

    tile_ids_urls = get_tile_urls(tile_ids_rect, "accumulation")

    output_dir = os.path.join(DATA_PATH, "output")

    merged_path = merge_rasters(tile_ids_urls, output_dir, layer="accumulation")

    print("Merged Raster Path:", merged_path)

    import rasterio


def test_crop_raster():

    layer = "accumulation"

    bb = [18, 19, 45, 47]  # (lon lon lat lat)

    min_lon, max_lon, min_lat, max_lat = bb

    tile_map_rect = get_regional_units_bounds()

    rows, cols = get_rows_cols(tile_map_rect, TILE_SIZE)

    tile_ids = get_tile_ids(rows, cols)

    tile_ids_rect = get_tile_ids_rect(tile_ids, min_lon, max_lon, min_lat, max_lat)[
        0, :
    ]

    rasterurl = get_tile_urls(tile_ids_rect, "accumulation")[0]

    output_dir = os.path.join(DATA_PATH, "output")
    bbox_latlon = (min_lon, min_lat, max_lon, max_lat)

    cropped_path = crop_raster(rasterurl, output_dir, bbox_latlon)

    print("Cropped Raster Path:", cropped_path)


def test_get_pixel_value_at_lat_lon():

    lon = 13.2284
    lat = 52.5709

    rasterurl = "https://public.igb-berlin.de/index.php/s/agciopgzXjWswF4/download?path=%2Fr.watershed%2Faccumulation_tiles20d&files=accumulation_h18v02.tif"

    raster_path = check_file_exists(rasterurl=rasterurl)

    pixel_value = get_pixel_value_at_lat_lon(raster_path, lon, lat)
    print("Pixel value at ({}, {}):".format(lon, lat), pixel_value)


def test_get_pixel_values_at_coords():

    coordinates = [(13.2284, 52.5709), (13.1564, 52.4147)]

    rasterurl = "https://public.igb-berlin.de/index.php/s/agciopgzXjWswF4/download?path=%2Fr.watershed%2Faccumulation_tiles20d&files=accumulation_h18v02.tif"

    raster_path = check_file_exists(rasterurl=rasterurl)

    pixel_values = get_pixel_values_at_coords(raster_path, coordinates)
    print("Pixel values at the given coordinates:", pixel_values)


def test_get_tile_ids():
    file_path = "/Users/anisjyu/Downloads/tile_list.txt"
    df = get_tile_list(file_path)
    print(df.head())
