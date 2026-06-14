# Laser-Induced Breakdown Spectroscopy (LIBS)

**Directory:** `/LIBS_Spectral_Analysis`

This pipeline processes raw emission spectra obtained from LIBS. It isolates sharp atomic emission lines superimposed on a large, slowly varying plasma continuum, matching the isolated peaks to known atomic elements.

## Workflow & Methodology

* **Data Ingestion & Interpolation:** Loads multiple raw spectra (wavelength vs. intensity) and maps them onto a unified master wavelength axis using NumPy vectorization.

* **Signal-to-Noise Enhancement:** Stacks and averages all interpolated spectra to suppress random detector shot noise.

* **High-Frequency Smoothing:** Applies a Savitzky-Golay filter (51-point window, 3rd-order polynomial) to iron out thermal noise without distorting peak geometries.

* **Plasma Continuum Removal (Baseline Correction):** Deploys a broad median filter to estimate the underlying thermal plasma continuum, subtracting it to isolate true atomic emission peaks.

* **Elemental Identification:** Cross-references detected peaks against a customizable NIST-style emission line database (`specline.csv`) within a strictly defined nanometer tolerance.

---

## Execution Guide

The LIBS engine operates via interactive cells for step-by-step signal verification.

1. Launch the Jupyter server from your root directory:
```bash
   jupyter notebook
```
2. Navigate to /LIBS_Spectral_Analysis and open main.ipynb.

3. Ensure your .csv spectral files are placed inside the Datas/ subfolder.

4. Run the cells sequentially (Shift + Enter) to process the baseline corrections and output the elemental identifications.