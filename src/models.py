"""
models.py

Data models used throughout the NLHE Analysis Package.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AnalysisResult:
    """
    Stores the complete analysis results for an NLHE dataset.
    """

    # -------------------------------------------------
    # Nonlinear Coefficients
    # -------------------------------------------------
    alpha1: float = 0.0
    alpha2: float = 0.0
    alpha3: float = 0.0

    # -------------------------------------------------
    # Goodness-of-Fit Metrics
    # -------------------------------------------------
    r2_first: float = 0.0
    r2_second: float = 0.0
    r2_third: float = 0.0

    rmse_first: float = 0.0
    rmse_second: float = 0.0
    rmse_third: float = 0.0

    # -------------------------------------------------
    # First Harmonic Data
    # -------------------------------------------------
    first_current: List[float] = field(default_factory=list)
    first_voltage: List[float] = field(default_factory=list)
    first_fit: List[float] = field(default_factory=list)

    # -------------------------------------------------
    # Second Harmonic Data
    # -------------------------------------------------
    second_current: List[float] = field(default_factory=list)
    second_voltage: List[float] = field(default_factory=list)
    second_fit: List[float] = field(default_factory=list)

    # -------------------------------------------------
    # Third Harmonic Data
    # -------------------------------------------------
    third_current: List[float] = field(default_factory=list)
    third_voltage: List[float] = field(default_factory=list)
    third_fit: List[float] = field(default_factory=list)

    # -------------------------------------------------
    # Residuals
    # -------------------------------------------------
    residuals_first: List[float] = field(default_factory=list)
    residuals_second: List[float] = field(default_factory=list)
    residuals_third: List[float] = field(default_factory=list)

    # -------------------------------------------------
    # Harmonic Response
    # -------------------------------------------------
    harmonic_response: Dict[str, float] = field(default_factory=dict)

    # -------------------------------------------------
    # Frequency Mixing Results
    # -------------------------------------------------
    mixing_products: Dict[str, float] = field(default_factory=dict)