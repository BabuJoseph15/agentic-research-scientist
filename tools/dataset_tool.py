from pathlib import Path
import pandas as pd


def load_dataset():

    file_path = (
        Path(__file__).parent.parent
        / "data"
        / "dengue.csv"
    )

    return pd.read_csv(file_path)