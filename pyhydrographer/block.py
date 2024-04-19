import rasterio as rio

from rasterio.windows import bounds

from pyhydrographer.globals import BASE_URL
from pyhydrographer.pixel import get_pixel_coords


def get_block_window(rasterpath, lon, lat, tile_ids, layer, band=1):

    with rio.open(rasterpath) as src:

        x, y = get_pixel_coords(lon, lat, src.transform)

        i = x / src.block_shapes[0][1]
        j = y / src.block_shapes[0][0]

        block_window = src.block_window(band, j, i)

    return block_window


def get_block_bounds(rasterpath, lon, lat, tile_ids, layer, band=1):

    with rio.open(rasterpath) as src:

        x, y = get_pixel_coords(lon, lat, src.transform)

        i = x / src.block_shapes[0][1]
        j = y / src.block_shapes[0][0]

        block_window = src.block_window(band, j, i)

        block_bounds = bounds(block_window, src.transform)

    return block_bounds


def get_block_data(rasterpath, lon, lat, tile_ids, layer, band=1):

    with rio.open(rasterpath) as src:

        x, y = get_pixel_coords(lon, lat, src.transform)

        i = int(x / src.block_shapes[0][1])
        j = int(y / src.block_shapes[0][0])

        block_window = src.block_window(band, j, i)

        block_data = src.read(window=block_window)

    return block_data


def get_block_url(tile_id, layer, band=1):

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
        print("Error: Unknown layer.")

    rasterpath = f"{BASE_URL}{variable}%2F{layer}_tiles20d&files={layer}_{tile_id}.tif"

    return rasterpath
