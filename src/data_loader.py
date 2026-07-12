"""
data_loader.py

Loads and validates experimental NLHE data from a
whitespace-separated .dat file.
"""

from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def load(self) -> pd.DataFrame:

        if not self.filepath.exists():
            raise FileNotFoundError(
                f"Input file not found: {self.filepath}"
            )

        # Read whitespace-separated data
        df = pd.read_csv(
            self.filepath,
            sep=r"\s+",
            engine="python",
            skiprows=1,
            header=None,
            usecols=[0, 1, 2, 3, 4, 5],
        )

        df.columns = [
            "I1",
            "V1",
            "I2",
            "V2",
            "I3",
            "V3",
        ]

        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.dropna().reset_index(drop=True)

        return df