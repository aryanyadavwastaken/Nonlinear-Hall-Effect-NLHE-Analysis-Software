# Nonlinear Hall Effect (NLHE) Analysis Software

A Python-based scientific software package developed during my research internship at **IIT Ropar** for automated analysis of **Nonlinear Hall Effect (NLHE)** experimental data.

The software processes experimental `.dat` files, extracts nonlinear transport coefficients, computes harmonic responses and frequency-mixing products, generates publication-quality visualizations, and automatically creates a comprehensive PDF report.

---

# Features

- Automated loading of experimental `.dat` datasets
- Extraction of nonlinear coefficients:
  - α₁ (Linear Response)
  - α₂ (Second-Order Response)
  - α₃ (Third-Order Response)
- Polynomial nonlinear model construction
- Harmonic response computation
- Frequency mixing analysis
- High-quality scientific plots
- Automatic PDF report generation
- Modular and extensible architecture

---

# Mathematical Model

The measured voltage is modeled as

\[
V(I)=\alpha_1I+\alpha_2I^2+\alpha_3I^3
\]

where

- α₁ represents the linear response
- α₂ represents the quadratic nonlinear response
- α₃ represents the cubic nonlinear response

The extracted coefficients are further used to compute harmonic voltages and frequency-mixing products.

---

# Project Structure

```
NLHE_Project/
│
├── data/
│   └── sample.dat
│
├── results/
│   ├── raw_data.png
│   ├── alpha1_fit.png
│   ├── alpha2_fit.png
│   ├── alpha3_fit.png
│   ├── model_prediction.png
│   ├── coefficients.png
│   ├── harmonic_response.png
│   ├── frequency_mixing.png
│   └── NLHE_Report.pdf
│
├── src/
│   ├── coefficient_extractor.py
│   ├── data_loader.py
│   ├── frequency_mixer.py
│   ├── harmonic_analyzer.py
│   ├── nonlinear_model.py
│   ├── project_controller.py
│   ├── report_generator.py
│   ├── visualization_manager.py
│   └── models.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

# Required Libraries

- numpy
- pandas
- matplotlib
- scipy
- reportlab

Install manually if required

```bash
pip install numpy pandas matplotlib scipy reportlab
```

---

# Running the Software

Place the experimental `.dat` file inside the `data` directory.

Run

```bash
python main.py
```

The software automatically performs the complete analysis pipeline.

---

# Generated Outputs

The software produces

### Figures

- Experimental Harmonic Data
- First Harmonic Fit
- Second Harmonic Fit
- Third Harmonic Fit
- Complete Nonlinear Polynomial Model
- Extracted Coefficients
- Harmonic Response
- Frequency Mixing Spectrum

### Report

A publication-style PDF report containing

- Extracted coefficients
- Goodness-of-fit metrics
- Harmonic analysis
- Frequency mixing analysis
- Scientific figures
- Summary

---

# Analysis Workflow

```
Experimental Data (.dat)

        │

        ▼

Data Loading

        │

        ▼

Coefficient Extraction

        │

        ▼

Nonlinear Polynomial Model

        │

        ▼

Harmonic Analysis

        │

        ▼

Frequency Mixing

        │

        ▼

Visualization

        │

        ▼

Automatic PDF Report
```

---

# Applications

This software can be used for

- Nonlinear Hall Effect experiments
- Harmonic transport analysis
- Nonlinear electronic devices
- Experimental condensed matter physics
- Semiconductor transport characterization
- Research data processing

---

# Future Enhancements

Planned improvements include

- Batch processing of multiple experimental `.dat` files
- Statistical analysis across repeated measurements
- Mean and standard deviation of extracted coefficients
- Confidence interval estimation
- Interactive graphical interface (GUI)
- Support for additional nonlinear transport models
- Export to CSV/Excel
- Advanced fitting and uncertainty analysis

---

# Author

**Aryan Yadav**

B.Tech. Electronics and VLSI Engineering

National Institute of Technology (NIT) Jalandhar

Research Internship – Indian Institute of Technology (IIT) Ropar


