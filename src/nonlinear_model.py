"""
nonlinear_model.py

Implements the nonlinear polynomial model for the
Nonlinear Hall Effect (NLHE) device.

Model:
    V(I) = α₁I + α₂I² + α₃I³
"""

from __future__ import annotations

from typing import Union

import numpy as np

from src.models import AnalysisResult

Number = Union[int, float]


class NonlinearModel:
    """
    Mathematical model of the NLHE device.
    """

    def __init__(self, result: AnalysisResult):
        """
        Initialize the nonlinear model using the extracted
        nonlinear coefficients.
        """
        self.alpha1 = result.alpha1
        self.alpha2 = result.alpha2
        self.alpha3 = result.alpha3

    # -----------------------------------------------------

    def evaluate(self, current: Union[Number, np.ndarray]):
        """
        Evaluate the complete nonlinear polynomial.

        Parameters
        ----------
        current : float or ndarray
            Input current.

        Returns
        -------
        float or ndarray
            Predicted voltage.
        """
        current = np.asarray(current, dtype=float)

        return (
            self.alpha1 * current
            + self.alpha2 * current**2
            + self.alpha3 * current**3
        )

    # -----------------------------------------------------

    def first_order(self, current: Union[Number, np.ndarray]):
        """
        First-order contribution.
        """
        current = np.asarray(current, dtype=float)
        return self.alpha1 * current

    # -----------------------------------------------------

    def second_order(self, current: Union[Number, np.ndarray]):
        """
        Second-order contribution.
        """
        current = np.asarray(current, dtype=float)
        return self.alpha2 * current**2

    # -----------------------------------------------------

    def third_order(self, current: Union[Number, np.ndarray]):
        """
        Third-order contribution.
        """
        current = np.asarray(current, dtype=float)
        return self.alpha3 * current**3