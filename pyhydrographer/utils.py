import os

from pyhydrographer.globals import BASE_URL, DATA_PATH
from pyhydrographer.utils import extract_raster_name


def generate_output_file(input_file, output_dir, suffix="crop"):
    """
    Generate the output file name based on the input file name and the output directory.

    Parameters:
        input_file (str): Input file name.
        output_dir (str): Output directory path.
        suffix (str): Suffix to append to the input file name.

    Returns:
        output_file (str): Output file path.
    """
    base_name, extension = os.path.splitext(os.path.basename(input_file))

    output_name = f"{base_name}_{suffix}{extension}"

    output_file = os.path.join(output_dir, output_name)

    return output_file


def extract_raster_name(url):
    url_parts = url.split("/")

    for part in url_parts:
        if part.startswith("download"):
            layer_name = part.split("=")[-1]
            return layer_name

    return None


def check_file_exists(rastername=None, rasterurl=None):

    if rastername is not None and rasterurl is not None:
        raise ValueError("Only one of raster name or url should be provided.")

    if rastername is None and rasterurl is None:
        raise ValueError("Either raster name or url must be provided.")

    if rasterurl is not None:
        rastername = extract_raster_name(rasterurl)

    filepath = os.path.join(DATA_PATH, "input", rastername)

    if os.path.exists(filepath):
        print("INFO:File already exists. Reading local file.")
    else:
        filepath = f"{BASE_URL}global&files={rastername}"

    return filepath


def extract_hv_from_url(url):

    parts = url.split("/")
    filename_part = next((part for part in parts if part.endswith(".tif")), None)

    if filename_part:
        h_v = filename_part.split("_")[-1].split(".")[0]
    else:
        h_v = None

    return h_v


def extract_hv_from_urls(urls):
    hv_list = []
    for url in urls:
        parts = url.split("/")
        filename_part = next((part for part in parts if part.endswith(".tif")), None)

        if filename_part:
            h_v = filename_part.split("_")[-1].split(".")[0]
            hv_list.append(h_v)
        else:
            hv_list.append(None)  # Append None if no TIFF file found in the URL

    return hv_list


def get_dims_deg(x1, y1, x2, y2):

    width = int(x2 - x1)
    height = int(y1 - y2)

    return height, width

def get_rows_cols(rect):

    x1, y1, x2, y2 = rect

    rows = int(y1 - y2) // TILE_SIZE[1]
    cols = int(x2 - x1) // TILE_SIZE[0]

    return rows, cols
