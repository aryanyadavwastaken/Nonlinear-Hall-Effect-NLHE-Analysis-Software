"""
coefficient_extractor.py

Extracts nonlinear coefficients
α1
α2
α3

from experimental harmonic measurements.

Author:
Aryan Yadav
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
)

from src.models import AnalysisResult


class CoefficientExtractor:
    """
    Extract nonlinear coefficients from
    harmonic measurements.
    """

    @staticmethod
    def linear_model(x, m):
        return m * x

    # -----------------------------------------------------

    def _fit(self, x, y):
        """
        Perform linear regression using curve_fit.
        """

        params, _ = curve_fit(
            self.linear_model,
            x,
            y
        )

        slope = params[0]

        prediction = self.linear_model(
            x,
            slope
        )

        residuals = y - prediction

        r2 = r2_score(
            y,
            prediction
        )

        rmse = np.sqrt(
            mean_squared_error(
                y,
                prediction
            )
        )

        return (
            slope,
            prediction,
            residuals,
            r2,
            rmse,
        )

    # -----------------------------------------------------

    def extract(
        self,
        df: pd.DataFrame
    ) -> AnalysisResult:
        """
        Extract α₁, α₂ and α₃ from
        experimental harmonic measurements.
        """

        result = AnalysisResult()

        # -------------------------------------------------
        # Experimental Data
        # -------------------------------------------------

        current1 = df.iloc[:, 0].to_numpy()
        voltage1 = df.iloc[:, 1].to_numpy()

        current2 = df.iloc[:, 2].to_numpy()
        voltage2 = df.iloc[:, 3].to_numpy()

        current3 = df.iloc[:, 4].to_numpy()
        voltage3 = df.iloc[:, 5].to_numpy()

        # -------------------------------------------------
        # First Harmonic
        # -------------------------------------------------

        slope1, pred1, res1, r21, rmse1 = self._fit(
            current1,
            voltage1
        )

        # -------------------------------------------------
        # Second Harmonic
        # -------------------------------------------------

        slope2, pred2, res2, r22, rmse2 = self._fit(
            current2 ** 2,
            voltage2
        )

        # -------------------------------------------------
        # Third Harmonic
        # -------------------------------------------------

        slope3, pred3, res3, r23, rmse3 = self._fit(
            current3 ** 3,
            voltage3
        )

        # -------------------------------------------------
        # Extracted Coefficients
        # -------------------------------------------------

        result.alpha1 = slope1
        result.alpha2 = 2 * slope2
        result.alpha3 = 4 * slope3

        # -------------------------------------------------
        # Goodness of Fit
        # -------------------------------------------------

        result.r2_first = r21
        result.r2_second = r22
        result.r2_third = r23

        result.rmse_first = rmse1
        result.rmse_second = rmse2
        result.rmse_third = rmse3

        # -------------------------------------------------
        # First Harmonic Dataset
        # -------------------------------------------------

        result.first_current = current1.tolist()
        result.first_voltage = voltage1.tolist()
        result.first_fit = pred1.tolist()

        # -------------------------------------------------
        # Second Harmonic Dataset
        # -------------------------------------------------

        result.second_current = current2.tolist()
        result.second_voltage = voltage2.tolist()
        result.second_fit = pred2.tolist()

        # -------------------------------------------------
        # Third Harmonic Dataset
        # -------------------------------------------------

        result.third_current = current3.tolist()
        result.third_voltage = voltage3.tolist()
        result.third_fit = pred3.tolist()

        # -------------------------------------------------
        # Residuals
        # -------------------------------------------------

        result.residuals_first = res1.tolist()
        result.residuals_second = res2.tolist()
        result.residuals_third = res3.tolist()

        return result