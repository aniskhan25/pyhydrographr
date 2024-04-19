"""Main module of pyhydrographer

Author(s): Anis Ur Rahman

This code is covered under the GNU General Public License v3.0.
Please refer to the LICENSE located in the root of this repository.
"""

from src.tile_utils import test_get_tile_ids
from src.species_utils import test_get_species_occurrences
from src.raster_utils import (
    test_get_regional_units_bounds,
    test_get_pixel_coords,
    test_get_dims_deg,
    test_get_rows_cols,
    test_get_tile_ids,
    test_get_tile_xy,
    test_get_tile_for_point,
    test_get_block_url,
    test_get_block_data,
    test_extract_hv_from_urls,
    test_get_tile_ids_rect,
    test_merge_rasters,
    test_extract_raster_name,
    test_crop_raster,
    test_get_pixel_value_at_lat_lon,
    test_get_pixel_values_at_coords,
)

if __name__ == "__main__":

    test_get_pixel_values_at_coords()
