"""
main.py

Entry point for the NLHE Analysis Package.
"""

from pathlib import Path
from src.project_controller import ProjectController


def main():

    data_folder = Path("data")

    dat_files = list(data_folder.glob("*.dat"))

    if not dat_files:
        raise FileNotFoundError("No .dat files found in the data folder.")

    controller = ProjectController(
        data_file=str(dat_files[0]),
        current_amplitude=2.0,
        f1=1000,
        f2=1200,
    )

    controller.run()


if __name__ == "__main__":
    main()