import pandas as pd
import numpy as np

from pyhydrographer.regional_units import get_regional_units_bounds

from pyhydrographer.globals import TILE_SIZE

BASE_URL = "https://public.igb-berlin.de/index.php/s/agciopgzXjWswF4/download?path=%2F"


def get_tile_list(file_path):
    # https://gitlab.com/selvaje74/hydrography.org/-/raw/main/images/hydrography90m/tiles20d/tile_list.txt
    return pd.read_csv(file_path, header=None, names=["Tile Id"])


def get_tile_ids(rows, cols, multiplier=2, step=2, offset=0, startx=0, starty=0):

    y = np.arange(starty, (cols + offset) * multiplier, step)
    x = np.arange(startx, (rows + offset) * multiplier, step)

    yv, xv = np.meshgrid(y, x)

    tile_ids = np.char.add(
        np.char.add("h", np.char.mod("%02d", yv)),
        np.char.add("v", np.char.mod("%02d", xv)),
    )

    return tile_ids


def get_tile_xy(lon, lat, tile_size=(20, 20)):

    x1, y1, x2, y2 = get_regional_units_bounds()

    x = int((lon - x1) / tile_size[0])
    y = int((y1 - lat) / tile_size[1])

    return x, y


def get_tile_id(tile_ids, lon, lat):

    x, y = get_tile_xy(lon, lat)

    return tile_ids[y][x]


def get_tile_bounds_deg(x, y, rect, tile_size=(20, 20)):

    x1, y1, _, _ = rect

    x_deg = x * tile_size[0] + x1
    y_deg = -(y * tile_size[1] - y1)

    return x_deg, y_deg


def get_tile_for_point(lon, lat, rect, tile_size=(20, 20)):

    x, y = get_tile_xy(lon, lat)

    x1_deg, y1_deg = get_tile_bounds_deg(x, y, rect, tile_size)
    x2_deg, y2_deg = get_tile_bounds_deg(x + 1, y + 1, rect, tile_size)

    return (x1_deg, y1_deg, x2_deg, y2_deg)


def get_tile_urls(tile_ids, layer, band=1):

    if layer in [
        "basin",
        "sub_catchment",
        "accumulation",
        "direction",
        "segment",
        "outlet",
    ]:
        variable = "r.watershed"
    elif layer in [
        "slope_curv_min_dw_cel",
        "slope_curv_max_dw_cel",
        "slope_elv_dw_cel",
        "slope_grad_dw_cel",
    ]:
        variable = "r.stream.slope"
    elif layer in [
        "stream_dist_up_near",
        "stream_dist_up_farth",
        "stream_dist_dw_near",
        "outlet_dist_dw_basin",
        "outlet_dist_dw_scatch",
        "stream_dist_proximity",
        "stream_diff_up_near",
        "stream_diff_up_farth",
        "stream_diff_dw_near",
        "outlet_diff_dw_basin",
        "outlet_diff_dw_scatch",
    ]:
        variable = "r.stream.distance"
    elif layer in [
        "channel_grad_dw_seg",
        "channel_grad_up_seg",
        "channel_grad_up_cel",
        "channel_curv_cel",
        "channel_elv_dw_seg",
        "channel_elv_up_seg",
        "channel_elv_up_cel",
        "channel_elv_dw_cel",
        "channel_dist_dw_seg",
        "channel_dist_up_seg",
        "channel_dist_up_cel",
    ]:
        variable = "r.stream.channel"
    elif layer in [
        "order_strahler",
        "order_shreve",
        "order_horton",
        "order_hack",
        "order_topo",
        "order_vect_point",
    ]:
        variable = "r.stream.order"
    elif layer in ["spi", "sti", "cti"]:
        variable = "flow.index"
    else:
        print("Error")

    rasterpath = [
        f"{BASE_URL}{variable}%2F{layer}_tiles20d&files={layer}_{tile_id}.tif"
        for tile_id in tile_ids
    ]

    return rasterpath


def get_tile_id_row_col(tile_id):
    col_str, row_str = tile_id.split("h")[1].split("v")

    col = int(col_str)
    row = int(row_str)

    return row, col


def get_tile_ids_rect(tile_ids, min_lon, max_lon, min_lat, max_lat):

    min_tile_id = get_tile_id(tile_ids, min_lon, min_lat)
    max_tile_id = get_tile_id(tile_ids, max_lon, max_lat)

    min_row, min_col = get_tile_id_row_col(min_tile_id)
    max_row, max_col = get_tile_id_row_col(max_tile_id)

    tile_ids_rect = get_tile_ids(
        max_row, max_col, multiplier=1, step=2, offset=1, startx=min_row, starty=min_col
    )

    return tile_ids_rect
