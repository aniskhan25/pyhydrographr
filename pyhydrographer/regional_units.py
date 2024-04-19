from pyhydrographer.utils import check_file_exists
from pyhydrographer.raster import get_bounds_deg


def get_regional_units_bounds():

    raster_name = "regional_unit_ovr.tif"

    filepath = check_file_exists(rastername=raster_name)

    tile_map_rect = get_bounds_deg(filepath)

    return tile_map_rect
