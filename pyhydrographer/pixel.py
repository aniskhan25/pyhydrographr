import rasterio as rio


def get_pixel_coords(lon, lat, transform):

    inv_transform = ~transform

    x, y = tuple(map(int, inv_transform * (lon, lat)))

    return x, y


def get_pixel_value_at_lat_lon(raster_path, lon, lat):

    with rio.open(raster_path) as src:

        row, col = src.index(lon, lat)

        value = src.read(1, window=((row, row + 1), (col, col + 1)))

    return value[0][0]


def get_pixel_values_at_coords(raster_path, coords):
    pixel_values = []
    with rio.open(raster_path) as src:

        pixel_values = [x[0] for x in src.sample(coords)]

    return pixel_values
