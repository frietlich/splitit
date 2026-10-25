"""Reset the live database: copy every CSV from seed/ over data/.  Run it with:  uv run python seed.py"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.join(HERE, "seed")
DATA_DIR = os.path.join(HERE, "data")


def reset_data(seed_dir, data_dir):
    """Copy every .csv file from seed_dir into data_dir and return the names of the files copied."""
    os.makedirs(data_dir, exist_ok=True)
    copied = []
    for file_name in sorted(os.listdir(seed_dir)):
        if file_name.endswith(".csv"):
            shutil.copyfile(os.path.join(seed_dir, file_name), os.path.join(data_dir, file_name))
            copied.append(file_name)
    return copied


if __name__ == "__main__":
    for file_name in reset_data(SEED_DIR, DATA_DIR):
        print("restored data/" + file_name + " from seed/" + file_name)
    print("Done. The data is back to how it was on day one.")
