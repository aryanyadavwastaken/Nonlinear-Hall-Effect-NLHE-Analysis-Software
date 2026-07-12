"""
report_generator.py

Generates a publication-quality PDF report for the
Nonlinear Hall Effect (NLHE) Analysis Package.

Author:
Aryan Yadav
"""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.models import AnalysisResult


class ReportGenerator:
    def __init__(self):

        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        self.report_dir = Path("results")
        self.plot_dir = Path("results")

        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Create styles FIRST
        self.styles = getSampleStyleSheet()

        # Register font
        font_path = r"C:\Windows\Fonts\arial.ttf"

        pdfmetrics.registerFont(
            TTFont("Arial", font_path)
        )

        # Apply font to every style
        for style in self.styles.byName.values():
            style.fontName = "Arial"
    # ---------------------------------------------------------

    def _create_table(self, data):

        table = Table(data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4053")),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("BOTTOMPADDING",(0,0),(-1,0),10),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

            ])
        )

        return table

    # ---------------------------------------------------------

    def _add_plot(
        self,
        story,
        filename,
        width=430,
        height=300
    ):

        image = self.plot_dir / filename

        if image.exists():

            story.append(

                Image(
                    str(image),
                    width=width,
                    height=height,
                )
            )

            story.append(
                Spacer(1,18)
            )

    # ---------------------------------------------------------

    def generate(
        self,
        result: AnalysisResult
    ):

        pdf = self.report_dir / "NLHE_Report.pdf"

        doc = SimpleDocTemplate(str(pdf))

        story = []

        # =====================================================
        # Title
        # =====================================================

        story.append(

            Paragraph(

                "Nonlinear Hall Effect Analysis Report",

                self.styles["Title"]

            )

        )

        story.append(
            Spacer(1,24)
        )

        # =====================================================
        # Coefficients
        # =====================================================

        story.append(

            Paragraph(

                "<b>Extracted Nonlinear Coefficients</b>",

                self.styles["Heading2"]

            )

        )

        coefficient_table = [

            ["Coefficient","Value"],

            ["α1",f"{result.alpha1:.6e}"],

            ["α2",f"{result.alpha2:.6e}"],

            ["α3",f"{result.alpha3:.6e}"],

        ]

        story.append(
            self._create_table(
                coefficient_table
            )
        )

        story.append(
            Spacer(1,22)
        )

        # =====================================================
        # Fit Metrics
        # =====================================================

        story.append(

            Paragraph(

                "<b>Goodness of Fit</b>",

                self.styles["Heading2"]

            )

        )

        fit_table = [

            ["Metric","α1","α2","α3"],

            [

                "R²",

                f"{result.r2_first:.5f}",

                f"{result.r2_second:.5f}",

                f"{result.r2_third:.5f}"

            ],

            [

                "RMSE",

                f"{result.rmse_first:.3e}",

                f"{result.rmse_second:.3e}",

                f"{result.rmse_third:.3e}"

            ]

        ]

        story.append(
            self._create_table(
                fit_table
            )
        )

        story.append(
            Spacer(1,24)
        )

        # =====================================================
        # Harmonic Response
        # =====================================================

        story.append(

            Paragraph(

                "<b>Computed Harmonic Response</b>",

                self.styles["Heading2"]

            )

        )

        harmonic_table = [

            ["Component","Voltage (V)"]

        ]

        for name,value in result.harmonic_response.items():

            harmonic_table.append(

                [

                    name,

                    f"{float(value):.6e}"

                ]

            )

        story.append(

            self._create_table(

                harmonic_table

            )

        )

        story.append(
            Spacer(1,24)
        )

        # =====================================================
        # Frequency Mixing
        # =====================================================

        story.append(

            Paragraph(

                "<b>Frequency Mixing Products</b>",

                self.styles["Heading2"]

            )

        )

        mixing_table = [

            [

                "Component",

                "Frequency (Hz)",

                "Amplitude"

            ]

        ]

        for key,item in result.mixing_products.items():

            mixing_table.append(

                [

                    key,

                    f"{item['frequency']:.2f}",

                    f"{item['amplitude']:.6e}"

                ]

            )

        story.append(

            self._create_table(

                mixing_table

            )

        )
        # =====================================================
        # FIGURES START HERE
        # =====================================================
        story.append(
            Paragraph(
                "<b>Generated Figures</b>",
                self.styles["Heading1"]
            )
        )

        story.append(Spacer(1, 12))

        # =====================================================
        # Raw Experimental Data
        # =====================================================

        story.append(
            Paragraph(
                "<b>Experimental Harmonic Data</b>",
                self.styles["Heading2"]
            )
        )

        self._add_plot(
            story,
            "raw_data.png"
        )

        # =====================================================
        # Alpha 1
        # =====================================================

        story.append(
            Paragraph(
                "<b>First Harmonic Fit (α1)</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "Linear response obtained from the first harmonic experimental measurements.",
                self.styles["BodyText"]
            )
        )

        self._add_plot(
            story,
            "alpha1_fit.png"
        )

        # =====================================================
        # Alpha 2
        # =====================================================

        story.append(
            Paragraph(
                "<b>Second Harmonic Fit (α2)</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "Quadratic nonlinear contribution extracted from the second harmonic measurements.",
                self.styles["BodyText"]
            )
        )

        self._add_plot(
            story,
            "alpha2_fit.png"
        )

        # =====================================================
        # Alpha 3
        # =====================================================

        story.append(
            Paragraph(
                "<b>Third Harmonic Fit (α3)</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "Third-order nonlinear response extracted from the third harmonic measurements.",
                self.styles["BodyText"]
            )
        )

        self._add_plot(
            story,
            "alpha3_fit.png"
        )          

        # =====================================================
        # Complete Polynomial
        # =====================================================

        story.append(
            Paragraph(
                "<b>Complete Nonlinear Polynomial Model</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "Prediction obtained using the complete nonlinear model V = α1I + α2I² + α3I³.",
                self.styles["BodyText"]
            )
        )

        self._add_plot(
            story,
            "model_prediction.png"
        )

        # =====================================================
        # Coefficients
        # =====================================================

        story.append(
            Paragraph(
                "<b>Extracted Nonlinear Coefficients</b>",
                self.styles["Heading2"]
            )
        )

        self._add_plot(
            story,
            "coefficients.png"
        )

        # =====================================================
        # Harmonic Response
        # =====================================================

        story.append(
            Paragraph(
                "<b>Computed Harmonic Response</b>",
                self.styles["Heading2"]
            )
        )

        self._add_plot(
            story,
            "harmonic_response.png"
        )

        # =====================================================
        # Frequency Mixing
        # =====================================================

        story.append(
            Paragraph(
                "<b>Frequency Mixing Spectrum</b>",
                self.styles["Heading2"]
            )
        )

        self._add_plot(
            story,
            "frequency_mixing.png"
        )

        # =====================================================
        # Summary
        # =====================================================

        story.append(
            Spacer(1, 20)
        )

        story.append(
            Paragraph(
                "<b>Summary</b>",
                self.styles["Heading2"]
            )
        )

        summary = f"""
        The nonlinear coefficients extracted from the experimental
        measurements are α1 = {result.alpha1:.6e},
        α2 = {result.alpha2:.6e},
        and α3 = {result.alpha3:.6e}.

        Independent regression analyses were performed for the first,
        second and third harmonic datasets. The extracted coefficients
        were subsequently used to construct the nonlinear Hall Effect
        polynomial model, compute the harmonic voltage response and
        predict the frequency-mixing products generated under
        dual-frequency excitation.

        The excellent goodness-of-fit metrics indicate strong agreement
        between the theoretical model and the experimental data.
        """

        story.append(
            Paragraph(
                summary,
                self.styles["BodyText"]
            )
        )

        # =====================================================

        doc.build(story)

        print(f"Report saved to {pdf}")