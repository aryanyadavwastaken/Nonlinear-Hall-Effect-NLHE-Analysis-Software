"""
harmonic_analyzer.py

Computes the DC and harmonic voltage components of the
Nonlinear Hall Effect (NLHE) device.

Model:
    V(I) = α₁I + α₂I² + α₃I³
    I(t) = I₀ cos(ωt)

Using trigonometric identities,

cos²(θ) = (1 + cos(2θ)) / 2
cos³(θ) = (3cos(θ) + cos(3θ)) / 4
"""

from __future__ import annotations

import numpy as np

from src.models import AnalysisResult


class HarmonicAnalyzer:
    """
    Computes the DC, first, second and third harmonic
    voltages from the extracted nonlinear coefficients.
    """

    def __init__(self, result: AnalysisResult):
        self.result = result

    # -----------------------------------------------------

    def analyze(self, current_amplitude):
        """
        Compute harmonic voltage amplitudes.

        Parameters
        ----------
        current_amplitude : float or ndarray
            Peak current (I₀).

        Returns
        -------
        dict
            Dictionary containing:
                DC
                Vω
                V2ω
                V3ω
        """

        I0 = np.asarray(current_amplitude, dtype=float)

        a1 = self.result.alpha1
        a2 = self.result.alpha2
        a3 = self.result.alpha3

        # DC component
        dc = 0.5 * a2 * I0**2

        # First harmonic (ω)
        v1 = (
            a1 * I0
            + 0.75 * a3 * I0**3
        )

        # Second harmonic (2ω)
        v2 = 0.5 * a2 * I0**2

        # Third harmonic (3ω)
        v3 = 0.25 * a3 * I0**3

        harmonics = {
            "DC": dc,
            "Vω": v1,
            "V2ω": v2,
            "V3ω": v3,
        }

        self.result.harmonic_response = harmonics

        return harmonics