"""
project_controller.py

Coordinates the complete NLHE analysis pipeline.
"""

from __future__ import annotations

from src.coefficient_extractor import CoefficientExtractor
from src.data_loader import DataLoader
from src.frequency_mixer import FrequencyMixer
from src.harmonic_analyzer import HarmonicAnalyzer
from src.nonlinear_model import NonlinearModel
from src.report_generator import ReportGenerator
from src.visualization_manager import VisualizationManager


class ProjectController:
    """
    Controls the complete NLHE analysis workflow.
    """

    def __init__(
        self,
        data_file: str,
        current_amplitude: float = 2.0,
        f1: float = 1000.0,
        f2: float = 1200.0,
    ):
        self.data_file = data_file
        self.current_amplitude = current_amplitude
        self.f1 = f1
        self.f2 = f2

    # ---------------------------------------------------------

    def run(self):

        print("=" * 60)
        print("NLHE ANALYSIS STARTED")
        print("=" * 60)

        # -------------------------------------------------
        # Load Experimental Data
        # -------------------------------------------------

        loader = DataLoader(self.data_file)
        df = loader.load()

        print("✓ Experimental data loaded.")

        # -------------------------------------------------
        # Extract Coefficients
        # -------------------------------------------------

        extractor = CoefficientExtractor()
        result = extractor.extract(df)

        print("✓ Nonlinear coefficients extracted.")

        # -------------------------------------------------
        # Build Model
        # -------------------------------------------------

        model = NonlinearModel(result)

        print("✓ Nonlinear model created.")

        # -------------------------------------------------
        # Harmonic Analysis
        # -------------------------------------------------

        harmonic = HarmonicAnalyzer(result)

        harmonic.analyze(
            self.current_amplitude
        )

        print("✓ Harmonic response computed.")

        # -------------------------------------------------
        # Frequency Mixing
        # -------------------------------------------------

        mixer = FrequencyMixer(result)

        mixer.compute(
            self.f1,
            self.f2,
        )

        print("✓ Frequency mixing completed.")

        # -------------------------------------------------
        # Combined Nonlinear Prediction
        # -------------------------------------------------

        result.model_prediction = model.evaluate(
            result.first_current
        ).tolist()

        print("✓ Nonlinear model evaluated.")

        # -------------------------------------------------
        # Visualization
        # -------------------------------------------------

        visualizer = VisualizationManager()

        visualizer.plot_raw_data(df)

        # =================================================
        # Alpha 1
        # =================================================

        visualizer.plot_harmonic_fit(

            current=result.first_current,

            experimental=result.first_voltage,

            fitted=result.first_fit,

            title="First Harmonic (α₁)",

            filename="alpha1_fit.png",

            xlabel="Current (A)",

            ylabel="Voltage (V)",

            equation="Vω = α₁I",

            r2=result.r2_first,

            rmse=result.rmse_first,
        )

        # =================================================
        # Alpha 2
        # =================================================

        visualizer.plot_harmonic_fit(

            current=result.second_current,

            experimental=result.second_voltage,

            fitted=result.second_fit,

            title="Second Harmonic (α₂)",

            filename="alpha2_fit.png",

            xlabel="Current² (A²)",

            ylabel="Voltage (V)",

            equation="V₂ω = ½ α₂ I²",

            r2=result.r2_second,

            rmse=result.rmse_second,
        )

        # =================================================
        # Alpha 3
        # =================================================

        visualizer.plot_harmonic_fit(

            current=result.third_current,

            experimental=result.third_voltage,

            fitted=result.third_fit,

            title="Third Harmonic (α₃)",

            filename="alpha3_fit.png",

            xlabel="Current³ (A³)",

            ylabel="Voltage (V)",

            equation="V₃ω = ¼ α₃ I³",

            r2=result.r2_third,

            rmse=result.rmse_third,
        )

        # =================================================
        # Combined Polynomial Model
        # =================================================

        visualizer.plot_harmonic_fit(

            current=result.first_current,

            experimental=result.first_voltage,

            fitted=result.model_prediction,

            title="Complete Nonlinear Polynomial",

            filename="model_prediction.png",

            xlabel="Current (A)",

            ylabel="Voltage (V)",

            equation="V = α₁I + α₂I² + α₃I³",
        )

        # =================================================

        visualizer.plot_residuals(
            result.residuals_first,
            "First Harmonic Residuals",
            "residuals.png",
        )

        visualizer.plot_coefficients(result)

        visualizer.plot_harmonic_response(result)

        visualizer.plot_frequency_mixing(result)

        print("✓ Figures generated.")

        # -------------------------------------------------
        # Generate PDF Report
        # -------------------------------------------------

        report = ReportGenerator()

        report.generate(result)

        print("✓ PDF report generated.")

        print("=" * 60)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("=" * 60)

        return result