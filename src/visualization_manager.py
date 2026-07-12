"""
visualization_manager.py

Creates all publication-quality figures for the
Nonlinear Hall Effect (NLHE) Analysis Package.

Author:
Aryan Yadav
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from src.models import AnalysisResult


class VisualizationManager:
    """
    Creates all figures used throughout the NLHE analysis.
    """

    def __init__(self, output_dir="results"):

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        plt.rcParams.update({
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "legend.fontsize": 10,
            "figure.dpi": 120
        })

    # -------------------------------------------------------------

    def _save(self, filename):

        plt.tight_layout()

        plt.savefig(
            os.path.join(self.output_dir, filename),
            dpi=400,
            bbox_inches="tight"
        )

        plt.close()

    # -------------------------------------------------------------

    def plot_raw_data(self, df):

        plt.figure(figsize=(8,6))

        plt.scatter(
            df.iloc[:,0],
            df.iloc[:,1],
            s=32,
            label="1ω",
            marker="o"
        )

        plt.scatter(
            df.iloc[:,2],
            df.iloc[:,3],
            s=32,
            label="2ω",
            marker="s"
        )

        plt.scatter(
            df.iloc[:,4],
            df.iloc[:,5],
            s=32,
            label="3ω",
            marker="^"
        )

        plt.xlabel("Current (A)")
        plt.ylabel("Voltage (V)")
        plt.title("Experimental Harmonic Data")

        plt.grid(True, alpha=0.3)

        plt.legend()

        self._save("raw_data.png")

    # -------------------------------------------------------------

    def plot_harmonic_fit(
            self,
            current,
            experimental,
            fitted,
            title,
            filename,
            xlabel,
            ylabel,
            equation="",
            r2=None,
            rmse=None,
    ):

        current = np.asarray(current)
        experimental = np.asarray(experimental)
        fitted = np.asarray(fitted)

        order = np.argsort(current)

        plt.figure(figsize=(8,6))

        plt.scatter(
            current,
            experimental,
            color="royalblue",
            s=40,
            label="Experimental",
            zorder=3
        )

        plt.plot(
            current[order],
            fitted[order],
            color="crimson",
            linewidth=2.5,
            label="Model Fit",
            zorder=4
        )

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.title(
            title,
            fontweight="bold"
        )

        plt.grid(
            True,
            linestyle="--",
            alpha=0.35
        )

        plt.legend()

        text = ""

        if equation != "":
            text += equation + "\n"

        if r2 is not None:
            text += f"R² = {r2:.5f}\n"

        if rmse is not None:
            text += f"RMSE = {rmse:.3e}"

        if text:

            plt.text(
                0.03,
                0.97,
                text,
                transform=plt.gca().transAxes,
                verticalalignment="top",
                fontsize=10,
                bbox=dict(
                    facecolor="white",
                    edgecolor="black",
                    alpha=0.85
                )
            )

        self._save(filename)

    # ---------------------------------------------------------

    # def plot_harmonic_fit(
    #     self,
    #     current,
    #     experimental,
    #     fitted,
    #     title,
    #     filename,
    #     xlabel,
    #     ylabel,
    # ):

           # -------------------------------------------------------------

    def plot_residuals(
        self,
        residuals,
        title,
        filename,
    ):

        residuals = np.asarray(residuals)

        plt.figure(figsize=(8, 4.5))

        plt.scatter(
            np.arange(len(residuals)),
            residuals,
            color="darkorange",
            s=32,
        )

        plt.axhline(
            0,
            color="black",
            linestyle="--",
            linewidth=1.2,
        )

        plt.xlabel("Sample Index")
        plt.ylabel("Residual")
        plt.title(title, fontweight="bold")

        plt.grid(True, linestyle="--", alpha=0.35)

        self._save(filename)

    # -------------------------------------------------------------

    def plot_harmonic_response(
        self,
        result: AnalysisResult,
    ):

        labels = list(result.harmonic_response.keys())

        values = np.abs(
            np.asarray(
                list(result.harmonic_response.values()),
                dtype=float,
            )
        )

        plt.figure(figsize=(8, 5))

        bars = plt.bar(
            labels,
            values,
            edgecolor="black",
            linewidth=1.0,
        )

        for bar, value in zip(bars, values):

            plt.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.2e}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        if values.max() / max(values.min(), 1e-15) > 100:
            plt.yscale("log")

        plt.ylabel("Voltage Amplitude (V)")
        plt.title("Computed Harmonic Response", fontweight="bold")

        plt.grid(True, axis="y", linestyle="--", alpha=0.35)

        self._save("harmonic_response.png")

    # -------------------------------------------------------------

    def plot_frequency_mixing(
        self,
        result: AnalysisResult,
    ):

        spectrum = result.mixing_products

        labels = []
        frequencies = []
        amplitudes = []

        for name, item in spectrum.items():

            labels.append(name)
            frequencies.append(item["frequency"])
            amplitudes.append(item["amplitude"])

        frequencies = np.asarray(frequencies)
        amplitudes = np.asarray(amplitudes)

        plt.figure(figsize=(11, 5))

        markerline, stemlines, baseline = plt.stem(
            frequencies,
            amplitudes,
            basefmt="k-",
        )

        plt.setp(stemlines, linewidth=2)
        plt.setp(markerline, markersize=7)

        ymax = amplitudes.max()

        for x, y, label in zip(
            frequencies,
            amplitudes,
            labels,
        ):

            plt.text(
                x,
                y + 0.03 * ymax,
                label,
                rotation=90,
                fontsize=8,
                ha="center",
                va="bottom",
            )

        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Relative Amplitude")
        plt.title(
            "Frequency Mixing Spectrum",
            fontweight="bold",
        )

        plt.grid(True, linestyle="--", alpha=0.35)

        self._save("frequency_mixing.png")

    # -------------------------------------------------------------

    def plot_coefficients(
        self,
        result: AnalysisResult,
    ):

        labels = [
            "α₁",
            "α₂",
            "α₃",
        ]

        values = np.abs([
            result.alpha1,
            result.alpha2,
            result.alpha3,
        ])

        plt.figure(figsize=(6.5, 5))

        bars = plt.bar(
            labels,
            values,
            edgecolor="black",
            linewidth=1,
        )

        for bar, value in zip(bars, values):

            plt.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.2e}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        if max(values) / max(min(values), 1e-15) > 100:
            plt.yscale("log")

        plt.ylabel("Coefficient Magnitude")
        plt.title(
            "Extracted Nonlinear Coefficients",
            fontweight="bold",
        )

        plt.grid(True, axis="y", linestyle="--", alpha=0.35)

        self._save("coefficients.png")