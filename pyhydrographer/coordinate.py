def get_dims_deg(x1, y1, x2, y2):

    width = int(x2 - x1)
    height = int(y1 - y2)

    return height, width

def get_rows_cols(rect, tile_size=(20, 20)):

    x1, y1, x2, y2 = rect

    rows = int(y1 - y2) // tile_size[1]
    cols = int(x2 - x1) // tile_size[0]

    return rows, cols
