import os

from dwca.read import DwCAReader

from pygbif import occurrences as occ


def get_species_occurrences(species_id):

    filepath = f"./data/input/{species_id}.zip"
    if os.path.exists(filepath):
        print("INFO:File already exists. Skipping download.")
    else:
        occ.download_get(species_id, path="./data/input")

    with DwCAReader(filepath) as dwca:

        print(
            "INFO:Core data file is: {}".format(dwca.descriptor.core.file_location)
        )  # => 'occurrence.txt'

        core_df = dwca.pd_read(dwca.descriptor.core.file_location, parse_dates=True)

        select_columns = [
            "id",
            "decimalLongitude",
            "decimalLatitude",
            "species",
            "year",
        ]
        df = core_df[select_columns]
        df = df.rename(
            columns={"decimalLongitude": "longitude", "decimalLatitude": "latitude"}
        )

    return df


def test_get_species_occurrences():

    df = get_species_occurrences("0004551-231002084531237")
    print(df.head())
